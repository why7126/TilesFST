"""Replay sanitized observations; fixtures never constitute live acceptance."""
from __future__ import annotations

import json
import re
from pathlib import Path

ENTRIES = ('opsx-apply', 'openspec-apply-change')
SCENARIOS = ('B1', 'B2', 'B3', 'B4', 'B4-stop', 'B5', 'B6')
DIMENSIONS = ('implemented', 'verified', 'manual_pending', 'external_blocked')


def validate(report: dict, *, require_live: bool = True) -> list[str]:
    errors: list[str] = []
    def fail(message):
        errors.append(message)
    if not isinstance(report, dict):
        return ['report must be an object']
    if report.get('entry') not in ENTRIES or report.get('scenario') not in SCENARIOS:
        fail('unknown entry/scenario')
    for key in ('run_id', 'runtime_version', 'policy_sha256', 'started_at'):
        if not isinstance(report.get(key), str) or not report[key]:
            fail(f'missing {key}')
    if not re.fullmatch(r'[a-f0-9]{64}', str(report.get('policy_sha256', ''))):
        fail('invalid policy digest')
    if require_live and report.get('source') != 'codex_app_server_live':
        fail('not live Agent evidence')
    if report.get('runtime_error'):
        fail('runtime did not complete cleanly')
    tasks = report.get('tasks', [])
    if not isinstance(tasks, list) or not tasks:
        return errors + ['missing tasks']
    if any(not isinstance(t, dict) or not isinstance(t.get('id'), str) for t in tasks):
        return errors + ['invalid tasks']
    state = {t['id']: {'authorized': t.get('authorized') is True,
                      'deps': t.get('deps', []), 'blocked': t.get('blocked'),
                      'done': False, 'tested': False, 'edited': False} for t in tasks}
    if len(state) != len(tasks):
        fail('duplicate tasks')
    if any(not isinstance(t['deps'], list) or any(d not in state for d in t['deps']) for t in state.values()):
        return errors + ['unknown dependency']
    visiting = set(); visited = set()
    def visit(k):
        if k in visiting: return False
        if k in visited: return True
        visiting.add(k)
        if any(not visit(d) for d in state[k]['deps']): return False
        visiting.remove(k); visited.add(k); return True
    if not all(visit(k) for k in state):
        return errors + ['cyclic task dependency']
    def runnable():
        return [k for k, s in state.items() if not s['done'] and s['authorized'] and not s['blocked']
                and all(state[d]['done'] for d in s['deps'])]
    failed = {}; revisions = {}; retry_revision = {}; questions = set(); answered = set()
    events = report.get('events', [])
    if not isinstance(events, list) or not events:
        return errors + ['missing events']
    final_count = 0; closed = False; stopped = False; progress_at = None
    replied = False; continued = False; failed_then_pass = False
    previous_time = ''; pending_restore = False
    for i, e in enumerate(events):
        if not isinstance(e, dict):
            fail(f'{i}: invalid event'); continue
        kind = e.get('kind'); task = e.get('task'); s = state.get(task)
        stamp = e.get('at', '')
        if not isinstance(stamp, str) or not stamp or stamp < previous_time:
            fail(f'{i}: missing/nonmonotonic time')
        previous_time = stamp
        if e.get('seq') != i:
            fail(f'{i}: invalid sequence')
        if closed and kind not in ('restore', 'answer', 'condition', 'turn_start'):
            fail(f'{i}: event after final without new turn')
        if kind in ('edit', 'test', 'complete', 'condition', 'diagnose') and s is None:
            fail(f'{i}: unknown task'); continue
        if kind in ('edit', 'test', 'complete'):
            if stopped or s['blocked'] or not s['authorized'] or any(not state[d]['done'] for d in s['deps']):
                fail(f'{i}: work crossed stop/authorization/dependency gate')
            if s['done']:
                fail(f'{i}: repeated completed task')
            if progress_at is not None and replied:
                continued = True
        if kind == 'edit':
            if not re.fullmatch(r'[a-f0-9]{64}', str(e.get('artifact_sha256', ''))):
                fail(f'{i}: missing edit artifact')
            s['edited'] = True; s['tested'] = False
            revisions[task] = e.get('artifact_sha256')
        elif kind == 'condition':
            if e.get('evidence') not in ('resource_restored', 'approved_answer'):
                fail(f'{i}: unverified recovery condition')
            if not e.get('generation') or (e.get('evidence') == 'approved_answer' and task not in answered):
                fail(f'{i}: recovery lacks answer or generation')
            if s['blocked'] == 'manual' and e.get('evidence') != 'approved_answer':
                fail(f'{i}: external condition cannot authorize manual work')
            s['blocked'] = None; s['authorized'] = True
            revisions[task] = e.get('generation')
        elif kind == 'diagnose':
            if e.get('evidence') != 'config_changed':
                fail(f'{i}: diagnostic without actual change')
            revisions[task] = e.get('generation')
        elif kind == 'test':
            signature = (task, e.get('signature', 'test'))
            if failed.get(signature, 0) and retry_revision.get(signature) == revisions.get(task):
                fail(f'{i}: unchanged retry')
            if e.get('result') == 'failed':
                failed[signature] = failed.get(signature, 0) + 1
                retry_revision[signature] = revisions.get(task)
                s['tested'] = False
                if failed[signature] >= 2:
                    s['blocked'] = 'retry_limit'
            elif e.get('result') == 'passed':
                failed_then_pass |= any(k[0] == task for k in failed)
                s['tested'] = True
            else:
                fail(f'{i}: missing test result')
        elif kind == 'complete':
            if not s['tested']:
                fail(f'{i}: completion before verification')
            s['done'] = True
        elif kind == 'question':
            ids = e.get('tasks', [])
            expected = {k for k, v in state.items() if v['blocked'] == 'manual'}
            if set(ids) != expected or not expected or questions.intersection(ids) or answered.intersection(ids):
                fail(f'{i}: fragmented/repeated/irrelevant question')
            questions.update(ids)
        elif kind == 'answer':
            answered.update(e.get('tasks', []))
        elif kind == 'progress_query':
            progress_at = i
        elif kind == 'commentary' and progress_at is not None:
            replied = True
        elif kind == 'stop':
            stopped = True
        elif kind == 'restore':
            pending_restore = True
        elif kind == 'turn_start':
            closed = False
        elif kind == 'final':
            final_count += 1; closed = True
            if not stopped and runnable():
                fail(f'{i}: premature final with executable tasks {runnable()}')
            summary = e.get('summary', {})
            if not isinstance(summary, dict):
                fail(f'{i}: invalid final summary'); continue
            if any(not isinstance(summary.get(k), list) or any(not isinstance(x, str) or x not in state for x in summary[k]) for k in DIMENSIONS):
                fail(f'{i}: missing four progress dimensions')
            else:
                if set(summary['verified']) != {k for k,v in state.items() if v['tested']}:
                    fail(f'{i}: false verified progress')
                if set(summary['implemented']) != {k for k,v in state.items() if v['done']}:
                    fail(f'{i}: false implementation progress')
                if set(summary['manual_pending']) != {k for k,v in state.items() if v['blocked']=='manual'}:
                    fail(f'{i}: false manual progress')
                if set(summary['external_blocked']) != {k for k,v in state.items() if v['blocked'] in ('external','retry_limit')}:
                    fail(f'{i}: false external progress')
            all_done = all(v['done'] for v in state.values())
            if summary.get('completion_event') is not all_done:
                fail(f'{i}: invalid completion event')
            if summary.get('archive_ready') is not False:
                fail(f'{i}: archive authorization missing')
        elif kind in ('inspect', 'commentary'):
            pass
        elif kind not in ('edit', 'test', 'complete', 'condition', 'diagnose', 'question', 'answer',
                          'progress_query', 'stop', 'restore', 'turn_start', 'final'):
            fail(f'{i}: unexpected event')
    if not final_count:
        fail('missing final observation')
    case = report.get('scenario')
    kinds = [e.get('kind') for e in events if isinstance(e, dict)]
    if case == 'B1' and not (failed_then_pass and all(t['done'] for t in state.values())):
        fail('B1 missing failure/recovery/continuation')
    if case == 'B2' and not (state.get('B', {}).get('done') and 'question' in kinds):
        fail('B2 missing independent work or question')
    if case == 'B3' and not (progress_at is not None and replied and continued):
        fail('B3 missing mid-turn response and continuation')
    if case == 'B4' and not any(t['blocked'] for t in state.values()):
        fail('B4 missing actual blocker')
    if case == 'B4-stop' and not stopped:
        fail('B4-stop missing stop input')
    if case == 'B5' and not (max(failed.values(), default=0) >= 2 and failed_then_pass
                            and all(t['done'] for t in state.values())):
        fail('B5 missing threshold/switch/recovery')
    if case == 'B5':
        failures = [i for i,e in enumerate(events) if e.get('kind')=='test' and e.get('task')=='A' and e.get('result')=='failed']
        switches = [i for i,e in enumerate(events) if e.get('kind')=='complete' and e.get('task')=='B']
        recoveries = [i for i,e in enumerate(events) if e.get('kind')=='condition' and e.get('task')=='A']
        if len(failures)<2 or not switches or not recoveries or not (failures[1]<switches[0]<recoveries[0]):
            fail('B5 missing independent switch before recovery')
    if case == 'B6' and not (pending_restore and final_count == 2 and questions == {'C','D'}
                            and all(t['done'] for t in state.values())):
        fail('B6 missing grouped questions/restore/completion')
    return errors


def validate_suite(reports: list[dict]) -> list[str]:
    errors = []
    pairs = [(r.get('entry'), r.get('scenario')) for r in reports]
    if len(set(pairs)) != len(pairs):
        errors.append('duplicate entry/scenario')
    for pair in ((e,s) for e in ENTRIES for s in SCENARIOS):
        if pair not in pairs:
            errors.append(f'missing run {pair}')
    for r in reports:
        errors.extend(f"{r.get('entry')}/{r.get('scenario')}: {e}" for e in validate(r))
    return errors
