"""隔离Git仓库中的知识生命周期与语义反例。"""
import copy
import json
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from knowledge_model.core import KnowledgeError, Model, safe_load, path_in, matches
from knowledge_model.store import Store

CHANGE = 'add-knowledge-model-lifecycle-sync'

def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False))

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.DEVNULL).decode().strip()

def commit(root):
    git(root, 'add', '.')
    git(root, 'commit', '-qm', 'isolated fixture')
    return git(root, 'rev-parse', 'HEAD')

@pytest.fixture
def repo(tmp_path):
    shutil.copytree(ROOT / 'knowledge-model', tmp_path / 'knowledge-model', ignore=shutil.ignore_patterns('generations', 'current.yaml'))
    mapping = safe_load((tmp_path / 'knowledge-model/mappings/pilot.yaml').read_bytes())
    for src in mapping['sources']:
        target = tmp_path / src['path']; target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / src['path'], target)
    for model_path in (tmp_path / 'knowledge-model').rglob('*.yaml'):
        document = safe_load(model_path.read_bytes())
        for item in document.get('elements', []) + document.get('relation_types', []):
            if item.get('source'):
                target=tmp_path/item['source']['path'];target.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(ROOT/item['source']['path'],target)
    archive = tmp_path / ('openspec/archive/2026-09-10-' + CHANGE)
    archive.mkdir(parents=True)
    for name in ('proposal', 'design', 'tasks', 'validation', 'trace'):
        (archive / (name + '.md')).write_text('---\ncreated_at: 2026-09-10 00:00:00\nupdated_at: 2026-09-10 00:00:00\n---\n\n- [x] Isolated lifecycle rehearsal\n')
    write(tmp_path / 'releases/v9.9.9/release.json', {'version': 'v9.9.9', 'changes': [CHANGE], 'sprints': ['sprint-030']})
    git(tmp_path, 'init', '-q'); git(tmp_path, 'config', 'user.email', 'fixture@example.invalid'); git(tmp_path, 'config', 'user.name', 'Fixture')
    commit(tmp_path)
    return tmp_path


def test_complete_lifecycle(repo):
    store = Store(repo)
    assert store.check([CHANGE])['status'] == 'blocked'
    assert store.sync(CHANGE, dry_run=True)['status'] == 'dry_run'
    assert not (repo / 'data').exists()
    first = store.sync(CHANGE)
    assert store.sync(CHANGE)['idempotent']
    assert store.check([CHANGE])['status'] == 'pass'
    assert store.snapshot('v9.9.9', prepare=True)['status'] == 'prepared'
    assert store.snapshot('v9.9.9', prepare=True)['status'] == 'pass'
    assert store.bind('v9.9.9')['status'] == 'bound'
    manifest = store.read('knowledge-model/snapshots/v9.9.9/manifest.yaml')
    assert manifest['included_changes'] == [CHANGE]
    assert manifest['included_sprints'] == ['sprint-030']
    assert store.read('knowledge-model/snapshots/v9.9.9/rules.yaml')
    assert store.current()[1] == first['generation']

@pytest.mark.parametrize('phase', ['before_commit', 'after_commit'])
def test_failure_retry(repo, phase):
    store = Store(repo)
    old = store.sync(CHANGE)['generation']
    with pytest.raises(KnowledgeError, match='injected'):
        store.sync(CHANGE, fail_at=phase)
    assert store.current()[1] == old
    assert store.sync(CHANGE)['idempotent']
    assert store.read('data/knowledge-model/runs/' + CHANGE + '.json')['status'] == 'synced'


def test_concurrent_idempotence(repo):
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda _: Store(repo).sync(CHANGE), range(4)))
    assert len({r['generation'] for r in results}) == 1
    assert sum(not r['idempotent'] for r in results) == 1


def test_dirty_source_preserves_model(repo):
    store = Store(repo); old = store.sync(CHANGE)['generation']
    src = repo / 'src/backend/app/api/v1/admin_tile_skus.py'
    src.write_text(src.read_text() + '\n# dirty\n')
    with pytest.raises(KnowledgeError, match='source_revision_pending'): store.sync(CHANGE)
    assert store.current()[1] == old
    assert store.check([CHANGE])['status'] == 'blocked'


def test_source_symbol_removed(repo):
    store = Store(repo); store.sync(CHANGE)
    src = repo / 'src/backend/app/api/v1/admin_tile_skus.py'
    src.write_text(src.read_text().replace('publish_tile_sku', 'renamed_publish'))
    commit(repo)
    with pytest.raises(KnowledgeError, match='missing_locator'): Store(repo).sync(CHANGE)


def test_generated_tamper(repo):
    store = Store(repo); key = store.sync(CHANGE)['generation']
    (repo / ('knowledge-model/generated/generations/' + key + '/entities.yaml')).write_text('[]')
    with pytest.raises(KnowledgeError, match='generated_drift'): store.check([CHANGE])


def test_snapshot_tamper_and_limit(repo):
    store = Store(repo); store.sync(CHANGE); store.snapshot('v9.9.9', prepare=True)
    (repo / 'knowledge-model/snapshots/v9.9.9/entities.yaml').write_text('[]')
    with pytest.raises(KnowledgeError, match='snapshot_content_drift'): store.bind('v9.9.9')
    with pytest.raises(KnowledgeError, match='snapshot_limit'): store.limits({'x': b'x' * 2097153})

@pytest.mark.parametrize('raw', ['a: 1\na: 2', 'a: !!python/object:builtins.object {}', 'a: &a [*a]', 'a: .nan'])
def test_unsafe_yaml(raw):
    with pytest.raises(KnowledgeError): safe_load(raw)

@pytest.mark.parametrize('path', ['../outside', '/tmp/file', '.git/config', 'a/../../escape', 'a\\b'])
def test_path_boundary(tmp_path, path):
    with pytest.raises(KnowledgeError): path_in(tmp_path, path)


def test_symlink_boundary(tmp_path):
    (tmp_path / 'link').symlink_to(tmp_path)
    with pytest.raises(KnowledgeError): path_in(tmp_path, 'link/file')


def test_semantic_failures(repo):
    model = Model(repo)
    elements = copy.deepcopy(list(model.elements.values()))
    for mutation, code in [
        (lambda x: x.append(copy.deepcopy(x[0])), 'duplicate_id'),
        (lambda x: x[0].update(type='missing:Type'), 'unknown_type'),
        (lambda x: x[0].update(layer='fact'), 'layer_mismatch'),
        (lambda x: x[0].update(premise_refs=['unknown']), 'missing_premise'),
    ]:
        sample = copy.deepcopy(elements); mutation(sample)
        with pytest.raises(KnowledgeError, match=code): model.validate_elements(sample, domain=True)


def test_rule_conflict(repo):
    store = Store(repo); store.sync(CHANGE)
    state, _ = store.current()
    rule = next(e for e in state['entities'] if e.get('effect'))
    opposite = copy.deepcopy(rule); opposite.update(id='rule:opposite', effect='allow')
    with pytest.raises(KnowledgeError, match='rule_conflict'): store.model.validate_graph(state['entities'] + [opposite], state['relations'])
    opposite['review_status'] = 'candidate'
    store.model.validate_graph(state['entities'] + [opposite], state['relations'])
    assert matches(rule['condition'], {}) is None
    assert matches(rule['condition'], {'status': 'PUBLISHED'}) is True


def test_out_of_scope_no_writes(repo):
    store = Store(repo)
    assert store.sync('uncovered-change')['status'] == 'out_of_scope'
    assert not (repo / 'data').exists()
    assert store.check(['uncovered-change'])['status'] == 'pass'


def test_readonly_snapshot_no_runtime_write(repo):
    with pytest.raises(KnowledgeError): Store(repo).snapshot('v9.9.9')
    assert not (repo / 'data').exists()


def test_historical_snapshot_independent_of_current(repo):
    store = Store(repo); store.sync(CHANGE); store.snapshot('v9.9.9', prepare=True); store.bind('v9.9.9')
    data, _ = store.release_data('v9.9.9'); data['publish_confirmation'] = {'status': 'confirmed'}
    write(repo / 'releases/v9.9.9/release.json', data)
    src = repo / 'src/backend/app/api/v1/admin_tile_skus.py'; src.write_text('changed after release')
    assert store.snapshot('v9.9.9')['status'] == 'pass'
    manifest_path = repo / 'knowledge-model/snapshots/v9.9.9/manifest.yaml'
    manifest = safe_load(manifest_path.read_bytes()); manifest['versions']['domain'] = '9.0.0'; write(manifest_path, manifest)
    with pytest.raises(KnowledgeError, match='snapshot_content_drift'): store.snapshot('v9.9.9')


def test_unresolved_risk_gate(repo):
    store = Store(repo); store.sync(CHANGE)
    item = dict(id='issue:manual', change=CHANGE, risk='low', status='open', reason='incomplete description', source='openspec/specs/tile-sku-management/spec.md')
    path = repo / 'knowledge-model/unresolved/review.yaml'; write(path, {'items':[item]})
    assert store.check([CHANGE])['status'] == 'pass'
    item['risk'] = 'high'; write(path, {'items':[item]})
    assert store.check([CHANGE])['status'] == 'blocked'
    item['status'] = 'resolved'; write(path, {'items':[item]})
    assert store.check([CHANGE])['status'] == 'pass'


def test_frozen_trace_recovery_and_cleanup(repo):
    import os, time
    store = Store(repo); store.sync(CHANGE)
    write(repo / 'iterations/archive/sprint-030/sprint.yaml', {'changes':[CHANGE]})
    trace = repo / ('openspec/archive/2026-09-10-' + CHANGE + '/trace.md'); before=trace.read_bytes()
    store.sync(CHANGE)
    assert trace.read_bytes() == before
    receipt = repo / ('data/knowledge-model/runs/' + CHANGE + '.json')
    os.utime(receipt, (time.time()-31*86400,)*2)
    assert store.cleanup()['records_removed'] == 1
    assert store.current()[1]


def test_binding_and_owner_types(repo):
    model=Model(repo); elements=copy.deepcopy(list(model.elements.values()))
    action=next(e for e in elements if e['id']=='model:PublishTileSKU')
    action['refs']['ownerEntity']=['model:ManageTileSKU']
    with pytest.raises(KnowledgeError, match='reference_type'): model.validate_elements(elements,domain=True)
    action['refs']['ownerEntity']=['model:TileSKU']
    scenario=next(e for e in elements if e['type']=='meta:Scenario')
    scenario['attributes']['bindings']={'tile_id':'string'}
    with pytest.raises(KnowledgeError, match='binding_contract'): model.validate_elements(elements,domain=True)


def test_multi_type_and_namespace(repo):
    store=Store(repo);store.sync(CHANGE);state,_=store.current()
    entity=copy.deepcopy(state['entities'][0]);entity['id']='other:same-name';entity['type']=[entity['type'],'pd:Artifact']
    store.model.validate_graph([entity],[])
    second=copy.deepcopy(entity);second['id']='different:same-name'
    store.model.validate_graph([entity,second],[])


def test_relation_type_cardinality_and_cycle(repo):
    store=Store(repo);store.sync(CHANGE);state,_=store.current();source=state['entities'][0]['source']
    def entity(id, type, **attrs): return dict(id=id,type=type,layer='fact',attributes=dict(name=id,**attrs),source=source,review_status='confirmed')
    def edge(id,pred,a,b):return dict(id=id,predicate=pred,subject=a,object=b,source=source)
    sku=entity('sku:1','tiles:TileSKU'); brand=entity('brand:1','tiles:Brand'); cat=entity('cat:1','tiles:TileCategory'); spec=entity('spec:1','tiles:TileSpec')
    with pytest.raises(KnowledgeError,match='cardinality'):store.model.validate_graph([sku],[])
    entities=[sku,brand,cat,spec]
    edges=[edge('e:1','tiles:belongsToBrand','sku:1','brand:1'),edge('e:2','tiles:belongsToCategory','sku:1','cat:1'),edge('e:3','tiles:usesSpec','sku:1','spec:1')]
    store.model.validate_graph(entities,edges)
    wrong=copy.deepcopy(edges);wrong[0]['object']='cat:1'
    with pytest.raises(KnowledgeError,match='relation_type'):store.model.validate_graph(entities,wrong)
    with pytest.raises(KnowledgeError,match='relation_cycle'):store.model.validate_graph(entities,edges+[edge('e:4','tiles:hasParent','cat:1','cat:1')])
    sku['attributes']['legacy']=True
    store.model.validate_graph(entities,edges[:2])


def test_override_stale_and_candidate(repo):
    store=Store(repo);store.sync(CHANGE)
    write(repo/'knowledge-model/overrides/reviewed.yaml',{'overrides':[{'change':CHANGE,'target':'api:sku-publish','review_status':'confirmed','reviewed_source_hash':'0'*64,'attributes':{'name':'curated'}}]})
    commit(repo)
    with pytest.raises(KnowledgeError,match='override_stale'):Store(repo).sync(CHANGE)


def test_increment_removal_and_reverse_reference(repo):
    store=Store(repo);store.sync(CHANGE)
    path=repo/'knowledge-model/mappings/pilot.yaml';data=safe_load(path.read_bytes())
    data['entities']=[e for e in data['entities'] if e['type']!='pd:Artifact'];write(path,data);commit(repo)
    result=Store(repo).sync(CHANGE)
    assert 'artifact:sku-publish-router' in result['diff']['removed']
    state,_=Store(repo).current();assert not any(e['object']=='artifact:sku-publish-router' for e in state['relations'])


def test_archive_hook_and_sprint_gate(repo):
    import importlib.util
    from knowledge_model.hooks import archive_sync
    results=archive_sync(repo,[CHANGE,'direct-out-of-scope'])
    assert [r['status'] for r in results]==['synced','out_of_scope']
    module_spec=importlib.util.spec_from_file_location('km_readiness',ROOT/'scripts/validate-sprint-archive-readiness.py')
    module=importlib.util.module_from_spec(module_spec);sys.modules[module_spec.name]=module;module_spec.loader.exec_module(module)
    sprint=repo/'iterations/change/sprint-030';write(sprint/'sprint.yaml',{'changes':[CHANGE], 'status':'in_progress'})
    for name in ('sprint','release-note','acceptance-report'):(sprint/(name+'.md')).write_text('# Isolated fixture\n')
    report=module.evaluate_sprint(repo,'sprint-030')
    assert not any('knowledge-model' in (r.blocker or '') for r in report.changes)
    path=repo/'knowledge-model/unresolved/high.yaml';write(path,{'items':[dict(id='risk:1',change=CHANGE,risk='high',status='open',reason='conflict',source='known-spec')]})
    report=module.evaluate_sprint(repo,'sprint-030')
    assert any('high_risk_unresolved' in (r.blocker or '') for r in report.changes)
    assert json.loads(module.readiness_to_json(report,force=True))['verdict']=='blocked'
    assert module.main(['--root',str(repo),'--sprint','sprint-030','--force','--json'])==1


def test_self_change_rehearsal(repo):
    # Real Change documents in an isolated copy; only task marks are simulated.
    target=repo/('openspec/archive/2026-09-10-'+CHANGE)
    for name in ('proposal','design','tasks','trace'):
        text=(ROOT/'openspec/changes'/CHANGE/(name+'.md')).read_text().replace('- [ ]','- [x]')
        (target/(name+'.md')).write_text(text)
    source=next((ROOT/'issues/requirements/review').glob('REQ-0138*'))
    shutil.copytree(source,repo/'issues/requirements/archive'/source.name)
    commit(repo)
    store=Store(repo);assert store.sync(CHANGE)['status']=='synced'
    assert store.sync(CHANGE)['idempotent']
    assert store.check([CHANGE])['status']=='pass'
    assert store.snapshot('v9.9.9',prepare=True)['status']=='prepared'


def test_concurrent_distinct_changes_preserve_both(repo):
    second='second-covered-change'
    archive=repo/('openspec/archive/2026-09-10-'+second)
    shutil.copytree(repo/('openspec/archive/2026-09-10-'+CHANGE),archive)
    mapping_path=repo/'knowledge-model/mappings/pilot.yaml';mapping=safe_load(mapping_path.read_bytes())
    for entity in mapping['entities']:entity['id']+=':second'
    for edge in mapping['relations']:edge['id']+=':second';edge['subject']+=':second'
    write(repo/'knowledge-model/mappings/second.yaml',mapping)
    path=repo/'knowledge-model/registry.yaml';registry=safe_load(path.read_bytes())
    registry['mapping_files'].append('mappings/second.yaml');registry['coverage'][second]={'mapping':'mappings/second.yaml','reason':'isolated concurrency test'};write(path,registry);commit(repo)
    with ThreadPoolExecutor(max_workers=2) as pool:
        results=list(pool.map(lambda c:Store(repo).sync(c),[CHANGE,second]))
    state,_=Store(repo).current();assert set(state['parts'])=={CHANGE,second}
    assert Store(repo).check([CHANGE,second])['status']=='pass'


def test_failed_new_generation_preserves_bytes(repo):
    store=Store(repo);old=store.sync(CHANGE)['generation'];before=store.current()[0]
    path=repo/'knowledge-model/mappings/pilot.yaml';mapping=safe_load(path.read_bytes());mapping['entities'][0]['attributes']={'name':'changed'};mapping['entities'][0]['review_status']='candidate';write(path,mapping);commit(repo)
    with pytest.raises(KnowledgeError,match='injected_before_commit'):Store(repo).sync(CHANGE,fail_at='before_commit')
    assert Store(repo).current()==(before,old)
    result=Store(repo).sync(CHANGE);assert result['generation']!=old


def test_version_compatibility_and_unknown_attribute(repo):
    path=repo/'knowledge-model/registry.yaml';registry=safe_load(path.read_bytes());registry['versions']['domain']='0.2.0';write(path,registry)
    with pytest.raises(KnowledgeError,match='incompatible_versions'):Model(repo)
    registry['versions']['domain']='0.1.0';write(path,registry)
    model=Model(repo);elements=copy.deepcopy(list(model.elements.values()));elements[0]['attributes']['undeclared']='bad'
    with pytest.raises(KnowledgeError,match='undefined_attribute'):model.validate_elements(elements,domain=True)


def test_template_event_and_required_reference(repo):
    model=Model(repo);base=copy.deepcopy(list(model.elements.values()));source=base[0]['source']
    page=dict(id='model:TestPage',type='meta:UIPage',layer='domain',attributes={'name':'fixture','bindings':{}},source=source,review_status='candidate',refs={'template':['model:MissingTemplate']})
    with pytest.raises(KnowledgeError,match='reference_type'):model.validate_elements(base+[page],domain=True)
    action=next(e for e in base if e['id']=='model:PublishTileSKU');action['refs']['ownerEntity']=[]
    with pytest.raises(KnowledgeError,match='missing_required_reference'):model.validate_elements(base,domain=True)


def test_snapshot_limits_exact(repo):
    store=Store(repo)
    store.limits({str(i):b'x'*2097152 for i in range(5)})
    with pytest.raises(KnowledgeError,match='snapshot_limit'):store.limits({str(i):b'x'*2097152 for i in range(6)})
    store.limits({str(i):b'x' for i in range(100)})
    with pytest.raises(KnowledgeError,match='snapshot_limit'):store.limits({str(i):b'x' for i in range(101)})


def test_rules_missing_provenance_and_conditions(repo):
    store=Store(repo);store.sync(CHANGE);state,_=store.current();rule=next(e for e in state['entities'] if e.get('effect'))
    broken=copy.deepcopy(rule);broken['source'].pop('sha256')
    with pytest.raises(KnowledgeError,match='missing_revision'):store.model.validate_graph([broken],[])
    broken=copy.deepcopy(rule);broken.pop('condition')
    with pytest.raises(KnowledgeError,match='missing_condition'):store.model.validate_graph([broken],[])
    with pytest.raises(KnowledgeError,match='unsupported_condition'):matches({'op':'python','field':'x'}, {})


def test_snapshot_old_model_can_be_invalid(repo):
    store=Store(repo);store.sync(CHANGE);store.snapshot('v9.9.9',prepare=True);store.bind('v9.9.9')
    data,_=store.release_data('v9.9.9');data['publish_confirmation']={'status':'confirmed'};write(repo/'releases/v9.9.9/release.json',data)
    (repo/'knowledge-model/registry.yaml').write_text('invalid current configuration')
    assert Store(repo,load_model=False).snapshot('v9.9.9')['status']=='pass'


def test_receipt_io_failure_recovers_committed_generation(repo, monkeypatch):
    store=Store(repo)
    with monkeypatch.context() as patch:
        def fail(*args, **kwargs): raise OSError('private exception must not be persisted')
        patch.setattr(store,'receipt',fail)
        with pytest.raises(OSError):store.sync(CHANGE)
    generation=store.current()[1];assert generation
    result=store.sync(CHANGE);assert result['idempotent'] and result['generation']==generation
    assert store.check([CHANGE])['status']=='pass'
    assert 'private exception' not in json.dumps(store.read('data/knowledge-model/runs/'+CHANGE+'.json'))


def test_cross_change_reference_and_partial_release(repo):
    second='second-dependent-change'
    shutil.copytree(repo/('openspec/archive/2026-09-10-'+CHANGE),repo/('openspec/archive/2026-09-10-'+second))
    mapping=safe_load((repo/'knowledge-model/mappings/pilot.yaml').read_bytes())
    mapping['entities']=[]
    mapping['relations']=[dict(id='edge:second-evidence',predicate='pd:evidencedBy',subject='change:'+second,object='artifact:sku-publish-router',source_index=1)]
    write(repo/'knowledge-model/mappings/second.yaml',mapping)
    path=repo/'knowledge-model/registry.yaml';registry=safe_load(path.read_bytes());registry['mapping_files'].append('mappings/second.yaml');registry['coverage'][second]={'mapping':'mappings/second.yaml','reason':'isolated reference test'};write(path,registry)
    commit(repo)
    store=Store(repo);store.sync(CHANGE);store.sync(second)
    assert store.check([CHANGE,second])['status']=='pass'
    data,_=store.release_data('v9.9.9');data['changes']=[second];write(repo/'releases/v9.9.9/release.json',data)
    with pytest.raises(KnowledgeError,match='relation_type'):store.snapshot('v9.9.9',prepare=True)


def test_event_payload_contract(repo):
    model=Model(repo);elements=copy.deepcopy(list(model.elements.values()));source=elements[0]['source']
    event=dict(id='model:FixtureEvent',type='meta:Event',layer='domain',attributes={'name':'fixture only','payload':{'tile_id':'integer'}},source=source,review_status='candidate')
    action=next(e for e in elements if e['id']=='model:PublishTileSKU');action['refs']['event']=[event['id']];action['attributes']['bindings']={'tile_id':'string'}
    with pytest.raises(KnowledgeError,match='binding_contract'):model.validate_elements(elements+[event],domain=True)
    action['attributes']['bindings']['tile_id']='integer'
    model.validate_elements(elements+[event],domain=True)
