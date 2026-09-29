"""知识模型命令入口。所有错误只输出固定错误码。"""
import argparse
import json
from pathlib import Path
from .core import KnowledgeError, Model, matches
from .store import Store


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('model')
    sync = sub.add_parser('sync')
    sync.add_argument('--change', required=True)
    sync.add_argument('--revision', default='HEAD')
    sync.add_argument('--dry-run', action='store_true')
    check = sub.add_parser('check')
    group = check.add_mutually_exclusive_group(required=True)
    group.add_argument('--change', action='append')
    group.add_argument('--sprint')
    for name in ('prepare', 'snapshot', 'bind'):
        sub.add_parser(name).add_argument('--release', required=True)
    sub.add_parser('cleanup')
    args = parser.parse_args(argv)
    try:
        store = Store(args.root, load_model=args.command not in {"snapshot", "bind", "prepare"})
        if args.command == 'model':
            cases = store.model.read('validation/test-cases.yaml').get('cases', [])
            for case in cases:
                if case.get('rule'):
                    rule = store.model.elements[case['rule']]
                    matched = matches(rule['condition'], case['input'])
                    actual = 'unknown' if matched is None else rule['effect'] if matched else 'not_applicable'
                    if actual != case['expect']: raise KnowledgeError('competency_case_failed', case['id'])
            result = dict(status='pass', types=len(store.model.types), elements=len(store.model.elements), relations=len(store.model.relations))
        elif args.command == 'sync': result = store.sync(args.change, args.revision, dry_run=args.dry_run)
        elif args.command == 'check':
            changes = args.change
            if args.sprint:
                paths = [store.path('iterations/' + stage + '/' + args.sprint + '/sprint.yaml') for stage in ('change', 'archive')]
                paths = [p for p in paths if p.exists()]
                if len(paths) != 1: raise KnowledgeError('sprint_missing_or_ambiguous')
                from .core import safe_load
                changes = safe_load(paths[0].read_bytes())['changes']
                changes = [x if isinstance(x, str) else x['id'] for x in changes]
            result = store.check(changes)
        elif args.command == 'prepare': result = store.snapshot(args.release, prepare=True)
        elif args.command == 'snapshot': result = store.snapshot(args.release)
        elif args.command == 'bind': result = store.bind(args.release)
        else: result = store.cleanup()
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 1 if result.get('status') == 'blocked' else 0
    except (KnowledgeError, OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'status': 'blocked', 'reason': exc.code if isinstance(exc, KnowledgeError) else 'invalid_input_or_io', 'location': exc.location if isinstance(exc, KnowledgeError) else '', 'details': exc.details if isinstance(exc, KnowledgeError) else None}, ensure_ascii=False))
        return 1
