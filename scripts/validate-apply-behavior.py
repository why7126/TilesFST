#!/usr/bin/env python3
"""Validate normalized live evidence; --suite requires all entry/scenario pairs."""
import argparse
import json
from pathlib import Path
from apply_behavior import validate, validate_suite

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('paths', nargs='+', type=Path)
    p.add_argument('--suite', action='store_true')
    a = p.parse_args()
    try:
        reports = [json.loads(path.read_text()) for path in a.paths]
        errors = validate_suite(reports) if a.suite else [e for r in reports for e in validate(r)]
    except (OSError, ValueError, TypeError, KeyError) as exc:
        errors = [f'invalid evidence input: {type(exc).__name__}']
    print(json.dumps({'status':'failed' if errors else 'passed', 'runs':len(a.paths), 'errors':errors}, ensure_ascii=False))
    raise SystemExit(bool(errors))
