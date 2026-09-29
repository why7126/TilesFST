from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('apply_behavior', ROOT/'scripts/apply_behavior.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


def report(case='B1'):
    return {'entry':'opsx-apply','scenario':case,'run_id':'fixture','runtime_version':'fixture',
            'started_at':'2026-09-10T00:00:00+00:00','policy_sha256':'a'*64,'source':'fixture',
            'tasks':[{'id':k,'authorized':True,'deps':[]} for k in ('A','B')], 'events':[]}


def emit(r, kind, **kwargs):
    r['events'].append({'kind':kind,'seq':len(r['events']),'at':'2026-09-10T00:00:00+00:00',**kwargs})


def final(r, done=('A','B'), manual=(), external=(), complete=True):
    emit(r,'final',summary={'implemented':list(done),'verified':list(done),'manual_pending':list(manual),
                           'external_blocked':list(external),'completion_event':complete,'archive_ready':False})


def finish(r, task):
    emit(r,'test',task=task,result='passed',signature='assertion')
    emit(r,'complete',task=task)


def b1():
    r=report();emit(r,'turn_start');emit(r,'test',task='A',result='failed',signature='assertion')
    emit(r,'edit',task='A',artifact_sha256='b'*64);finish(r,'A');finish(r,'B');final(r)
    return r


def test_valid_fixture_does_not_claim_live_acceptance():
    r=b1();assert v.validate(r,require_live=False)==[]
    assert 'not live Agent evidence' in v.validate(r)


@pytest.mark.parametrize('event', ['test','complete','edit'])
def test_gate_prevents_unapproved_or_blocked_work(event):
    r=report('B2');r['tasks'][0].update(authorized=False,blocked='manual')
    emit(r,event,task='A',result='passed',artifact_sha256='a'*64)
    assert any('gate' in e for e in v.validate(r,require_live=False))


def test_independent_task_must_continue_despite_manual_blocker():
    r=report('B2');r['tasks'][0].update(authorized=False,blocked='manual')
    emit(r,'question',tasks=['A']);final(r,done=(),manual=['A'],complete=False)
    assert any('premature final' in e for e in v.validate(r,require_live=False))
    r['events'].pop();finish(r,'B');final(r,done=['B'],manual=['A'],complete=False)
    assert v.validate(r,require_live=False)==[]


def test_final_cannot_trust_claimed_blockers():
    r=report('B4');final(r,done=(),external=['A','B'],complete=False)
    assert any('premature final' in e for e in v.validate(r,require_live=False))


def test_all_blocked_is_legal():
    r=report('B4')
    for t in r['tasks']:t['blocked']='external'
    final(r,done=(),external=['A','B'],complete=False)
    assert v.validate(r,require_live=False)==[]


def test_dependency_and_false_completion():
    r=report();r['tasks'][1]['deps']=['A'];finish(r,'B');final(r)
    es=v.validate(r,require_live=False)
    assert any('dependency' in e for e in es)
    assert any('false implementation' in e for e in es)


def test_unchanged_retry_fails_even_before_threshold():
    r=report();emit(r,'test',task='A',result='failed');emit(r,'test',task='A',result='failed')
    assert any('unchanged retry' in e for e in v.validate(r,require_live=False))


def test_two_failures_require_switch_and_verified_new_condition():
    r=report('B5');emit(r,'test',task='A',result='failed',signature='resource')
    emit(r,'diagnose',task='A',evidence='config_changed',generation='v2')
    emit(r,'test',task='A',result='failed',signature='resource');finish(r,'B')
    emit(r,'condition',task='A',evidence='resource_restored',generation='v3')
    emit(r,'test',task='A',result='passed',signature='resource');emit(r,'complete',task='A');final(r)
    assert v.validate(r,require_live=False)==[]
    bad=copy.deepcopy(r);bad['events'][5]['evidence']='new wording'
    assert any('unverified recovery' in e for e in v.validate(bad,require_live=False))


def test_progress_question_needs_real_continuation_after_reply():
    r=report('B3');emit(r,'progress_query');emit(r,'commentary');finish(r,'A');finish(r,'B');final(r)
    assert v.validate(r,require_live=False)==[]
    r['events']=[e for e in r['events'] if e['kind']!='commentary']
    assert any('B3' in e for e in v.validate(r,require_live=False))


def test_explicit_stop_does_not_allow_further_tool_work():
    r=report('B4-stop');emit(r,'stop');final(r,done=(),complete=False)
    assert v.validate(r,require_live=False)==[]
    r['events'].pop();finish(r,'A');final(r,done=['A'],complete=False)
    assert any('gate' in e for e in v.validate(r,require_live=False))


def test_questions_are_grouped_and_existing_answers_not_reasked():
    r=report('B6')
    r['tasks'] += [{'id':k,'authorized':False,'deps':[],'blocked':'manual'} for k in ('C','D')]
    emit(r,'question',tasks=['C'])
    assert any('fragmented' in e for e in v.validate(r,require_live=False))
    r['events']=[];emit(r,'question',tasks=['C','D']);finish(r,'A');finish(r,'B')
    final(r,done=['A','B'],manual=['C','D'],complete=False)
    emit(r,'restore');emit(r,'answer',tasks=['C','D'])
    for k in ('C','D'):emit(r,'condition',task=k,evidence='approved_answer',generation='a1')
    emit(r,'turn_start');finish(r,'C');finish(r,'D');final(r,done=['A','B','C','D'])
    assert v.validate(r,require_live=False)==[]


@pytest.mark.parametrize('key',['events','tasks','policy_sha256','runtime_version'])
def test_missing_required_evidence_fails_closed(key):
    r=b1();del r[key];assert v.validate(r,require_live=False)


def test_missing_final_four_dimensions_or_completion_sync_fails():
    r=b1();del r['events'][-1]['summary']['manual_pending']
    assert any('four progress' in e for e in v.validate(r,require_live=False))
    r=b1();r['events'][-1]['summary']['completion_event']=False
    assert any('completion event' in e for e in v.validate(r,require_live=False))


def test_suite_requires_both_entries_every_scenario():
    assert len(v.validate_suite([]))==len(v.ENTRIES)*len(v.SCENARIOS)


def test_unknown_event_or_missing_result_rejected():
    r=b1();r['events'][1]['result']='unknown';emit(r,'unverified_summary')
    assert any('missing test result' in e for e in v.validate(r,require_live=False))
    assert any('unexpected event' in e for e in v.validate(r,require_live=False))


def test_cycle_cannot_be_used_as_legal_pause():
    r=report('B4');r['tasks'][0]['deps']=['B'];r['tasks'][1]['deps']=['A']
    final(r,done=(),complete=False)
    assert 'cyclic task dependency' in v.validate(r,require_live=False)


def test_resource_restoration_cannot_grant_manual_authorization():
    r=report('B2');r['tasks'][0].update(authorized=False,blocked='manual')
    emit(r,'condition',task='A',evidence='resource_restored',generation='v1')
    assert any('cannot authorize' in e for e in v.validate(r,require_live=False))


def test_answer_must_precede_manual_condition():
    r=report('B2');r['tasks'][0].update(authorized=False,blocked='manual')
    emit(r,'condition',task='A',evidence='approved_answer',generation='v1')
    assert any('lacks answer' in e for e in v.validate(r,require_live=False))


def test_runtime_error_never_passes_suite():
    r=b1();r.update(source='codex_app_server_live',runtime_error='timeout')
    assert 'runtime did not complete cleanly' in v.validate(r)


def test_non_task_final_values_fail_closed():
    r=b1();r['events'][-1]['summary']['implemented']=[{'unexpected':'object'}]
    assert any('four progress' in e for e in v.validate(r,require_live=False))


def test_retry_case_cannot_skip_independent_switch():
    r=report('B5');emit(r,'test',task='A',result='failed',signature='resource')
    emit(r,'diagnose',task='A',evidence='config_changed',generation='v2')
    emit(r,'test',task='A',result='failed',signature='resource')
    emit(r,'condition',task='A',evidence='resource_restored',generation='v3')
    emit(r,'test',task='A',result='passed',signature='resource');emit(r,'complete',task='A')
    finish(r,'B');final(r)
    assert any('independent switch' in e for e in v.validate(r,require_live=False))
