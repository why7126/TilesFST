"""Collector/fixture unit tests only; these are not live Agent acceptance."""
import importlib.util
import sys
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
spec=importlib.util.spec_from_file_location('apply_behavior_runner',ROOT/'scripts/run-apply-behavior.py')
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)


@pytest.mark.parametrize('expression',["__import__('os')",'a.__class__','[a,b]','a**b','open(a)','9'*81])
def test_expression_evaluator_cannot_execute_python(expression):
    with pytest.raises((ValueError,SyntaxError)):
        r.calculate(expression,2,3)


def test_manual_gate_and_known_answers_cannot_contradict(tmp_path):
    lab=r.Lab(tmp_path,'B2','opsx-apply','fixture','policy')
    plan=lab.call({'op':'inspect'})
    assert 'A-approved' not in plan['known_answers']
    assert 'B-approved' in plan['known_answers']
    result=lab.call({'op':'edit','task':'A','expression':'a-b'})
    assert result['error']=='blocked'
    assert (tmp_path/'A.expr').read_text()=='a+b'


def test_first_failure_requires_real_artifact_repair(tmp_path):
    lab=r.Lab(tmp_path,'B1','opsx-apply','fixture','policy')
    assert lab.call({'op':'test','task':'A'})['passed'] is False
    assert lab.call({'op':'complete','task':'A'})['error']=='test_not_passed'
    lab.call({'op':'edit','task':'A','expression':'a+b'})
    assert (tmp_path/'A.expr').read_text()=='a+b'
    assert lab.call({'op':'test','task':'A'})['passed'] is True


def test_remote_recovery_only_after_independent_task_verified(tmp_path):
    lab=r.Lab(tmp_path,'B5','opsx-apply','fixture','policy')
    assert lab.call({'op':'test','task':'A'})['passed'] is False
    lab.call({'op':'diagnose','task':'A'})
    assert (tmp_path/'candidate.cfg').exists()
    assert lab.call({'op':'test','task':'A'})['passed'] is False
    assert not (tmp_path/'resource.ready').exists()
    assert lab.call({'op':'complete','task':'B'})['error']=='test_not_passed'
    lab.call({'op':'test','task':'B'});lab.call({'op':'complete','task':'B'})
    assert (tmp_path/'resource.ready').exists()
    assert lab.call({'op':'test','task':'A'})['passed'] is True


def test_question_text_is_never_saved_in_normalized_events(tmp_path):
    lab=r.Lab(tmp_path,'B2','opsx-apply','fixture','policy')
    lab.call({'op':'ask','questions':['arbitrary private message']})
    assert lab.report['events'][-1]['tasks']==['invalid-task']
    assert 'private message' not in str(lab.report)


def test_stop_probe_has_single_inflight_task_to_avoid_presteer_batch_ambiguity(tmp_path):
    lab=r.Lab(tmp_path,'B4-stop','opsx-apply','fixture','policy')
    assert list(lab.tasks)==['A']


def test_existing_evidence_is_not_overwritten(tmp_path):
    target=tmp_path/'opsx-apply-B1.json';target.write_text('existing evidence')
    with pytest.raises(ValueError,match='fresh output'):
        r.run('opsx-apply','B1',tmp_path,1)
    assert target.read_text()=='existing evidence'
