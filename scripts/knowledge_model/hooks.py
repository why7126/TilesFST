"""现有工作流调用边界：只处理注册覆盖范围。"""
from pathlib import Path
from .core import KnowledgeError, safe_load
from .store import Store


def enabled(root):
    return (Path(root) / 'knowledge-model/registry.yaml').exists()


def archive_sync(root, changes):
    if not enabled(root): return []
    store = Store(Path(root))
    results = []
    for change in changes:
        try:
            result = store.sync(change)
        except (KnowledgeError, OSError, ValueError, KeyError) as exc:
            result = {'change': change, 'status': 'failed', 'reason': exc.code if isinstance(exc, KnowledgeError) else 'invalid_input_or_io'}
        results.append(result)
    return results


def release_check(root, version):
    if not enabled(root): return {'status': 'out_of_scope'}
    return Store(Path(root), load_model=False).snapshot(version)
