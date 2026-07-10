#!/usr/bin/env python3
"""
文档用途：校验 API 标准合规性
文档内容：检查路由 OpenAPI 元数据、错误码引用等
内容来源：build-api-standard / initialize-project
"""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
API_DIR = ROOT / "src" / "backend" / "app" / "api"
OPENAPI_PATH = ROOT / "src" / "web" / "openapi.json"
HTTP_METHODS = {"get", "post", "put", "patch", "delete", "options", "head"}
KEBAB_CASE_TAG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

violations: list[str] = []


def check_router_file(path: Path) -> None:
    rel = path.relative_to(ROOT)
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text)

    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        # Heuristic: route handlers often have router decorator
        for dec in node.decorator_list:
            src = ast.get_source_segment(text, dec) or ""
            if "router." not in src and "app." not in src:
                continue
            if "get(" in src or "post(" in src or "put(" in src or "patch(" in src or "delete(" in src:
                body = ast.get_source_segment(text, node) or ""
                if "response_model" not in src and "response_model" not in body:
                    violations.append(
                        f"{rel}:{node.lineno} — 路由 {node.name} 缺少 response_model"
                    )
                if "summary=" not in src:
                    violations.append(f"{rel}:{node.lineno} — 路由 {node.name} 缺少 summary")
                break


def _operation_label(method: str, path: str, operation: dict[str, Any]) -> str:
    operation_id = operation.get("operationId")
    label = f"{method.upper()} {path}"
    if operation_id:
        label = f"{label} ({operation_id})"
    return label


def check_openapi_operation_tags() -> None:
    if not OPENAPI_PATH.exists():
        violations.append(f"缺少必需文件: {OPENAPI_PATH.relative_to(ROOT)}")
        return

    try:
        document = json.loads(OPENAPI_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        violations.append(f"{OPENAPI_PATH.relative_to(ROOT)} — JSON 解析失败: {exc}")
        return

    paths = document.get("paths", {})
    if not isinstance(paths, dict):
        violations.append(f"{OPENAPI_PATH.relative_to(ROOT)} — paths 必须是对象")
        return

    for path, path_item in paths.items():
        if not isinstance(path_item, dict):
            continue
        for method, operation in path_item.items():
            if method.lower() not in HTTP_METHODS or not isinstance(operation, dict):
                continue

            label = _operation_label(method, path, operation)
            tags = operation.get("tags")
            if not isinstance(tags, list) or not tags:
                violations.append(f"{label} — OpenAPI operation 缺少 tags")
                continue

            if len(tags) != 1:
                violations.append(f"{label} — OpenAPI operation tags 必须且只能有 1 个: {tags}")

            if len(tags) != len(set(tags)):
                violations.append(f"{label} — OpenAPI operation tags 存在重复值: {tags}")

            for tag in tags:
                if not isinstance(tag, str) or not KEBAB_CASE_TAG.fullmatch(tag):
                    violations.append(f"{label} — OpenAPI operation tag 非 kebab-case: {tag!r}")


def main() -> int:
    if not API_DIR.exists():
        print("API 目录不存在，跳过校验。")
        return 0

    for path in API_DIR.rglob("*.py"):
        if path.name.startswith("_"):
            continue
        try:
            check_router_file(path)
        except SyntaxError as e:
            violations.append(f"{path.relative_to(ROOT)} — 语法错误: {e}")

    required_docs = [
        "docs/standards/api-governance.md",
        "docs/standards/error-codes.md",
        "src/backend/app/core/error_codes.py",
        "src/backend/app/schemas/common.py",
    ]
    for doc in required_docs:
        if not (ROOT / doc).exists():
            violations.append(f"缺少必需文件: {doc}")

    check_openapi_operation_tags()

    if violations:
        print("API 标准校验失败：")
        for v in violations:
            print(f"  - {v}")
        return 1

    print("API 标准校验通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
