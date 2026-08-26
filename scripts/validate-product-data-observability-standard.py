#!/usr/bin/env python3
"""
文档用途：校验通用产品数据采集与链路观测规范
文档内容：检查标准文档、docs 索引和相关 standards 交叉引用是否存在
内容来源：REQ-0126 / add-product-data-collection-observability-standard
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

STANDARD = "docs/standards/product-data-collection-observability.md"
REQUIRED_FILES = [
    STANDARD,
    "docs/README.md",
    "docs/standards/task-trace-coverage.md",
    "docs/standards/api-governance.md",
]

REQUIRED_REFERENCES = {
    "docs/README.md": [STANDARD],
    "docs/standards/task-trace-coverage.md": [STANDARD],
    "docs/standards/api-governance.md": [STANDARD],
}

REQUIRED_STANDARD_TERMS = [
    "usage_events",
    "request_logs",
    "task_traces",
    "task_trace_spans",
    "标准数据结构",
    "behavior_trace_id",
    "behavior_event_id",
    "parent_behavior_event_id",
    "request_id",
    "client_request_id",
    "parent_request_id",
    "Task Trace 分级覆盖",
    "最小标准字段",
    "可空与关联规则",
    "产品扩展规则",
    "建议索引",
    "request_logs` 明细 | 90 天",
    "usage_events` 明细 | 180 天",
    "task_traces` / `task_trace_spans` 明细 | 90 天",
    "聚合数据 | 1 年",
    "Authorization",
    "Cookie",
    "Token",
    "MinIO AccessKey",
    "完整请求体",
    "完整响应体",
    "本机绝对路径",
    "真实客户敏感数据",
]


def _read_rel(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main() -> int:
    errors: list[str] = []

    for path in REQUIRED_FILES:
        if not (ROOT / path).exists():
            errors.append(f"缺少必需文件: {path}")

    if not errors:
        standard_text = _read_rel(STANDARD)
        for term in REQUIRED_STANDARD_TERMS:
            if term not in standard_text:
                errors.append(f"{STANDARD} 缺少关键内容: {term}")

    for path, refs in REQUIRED_REFERENCES.items():
        if not (ROOT / path).exists():
            continue
        text = _read_rel(path)
        for ref in refs:
            if ref not in text and Path(ref).name not in text:
                errors.append(f"{path} 缺少引用: {ref}")

    if errors:
        print("通用产品数据采集与链路观测规范校验失败：")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("通用产品数据采集与链路观测规范校验通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
