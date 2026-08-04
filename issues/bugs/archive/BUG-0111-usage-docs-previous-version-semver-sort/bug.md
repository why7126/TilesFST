---
bug_id: BUG-0111-usage-docs-previous-version-semver-sort
title: usage docs 前置版本候选使用字符串排序可能选错版本
severity: medium
status: done
owner: null
discovered_at: 2026-08-03 23:11:28
environment: release usage docs generation workflow
related_requirement: REQ-0088-versioned-product-usage-docs
related_change: fix-usage-docs-previous-version-semver-sort
created_at: 2026-08-04 08:17:52
updated_at: 2026-08-04 09:30:26
---

# BUG-0111 usage docs 前置版本候选使用字符串排序可能选错版本

## 现象

`scripts/generate-usage-docs.py` 的 `previous_usage_docs_version()` 会扫描 `releases/` 下已生成 `usage-docs/` 的版本，并用字符串排序选择候选版本列表的最后一项作为继承来源。

在 `v0.3.4`、`v0.3.5` 这类同位数版本中结果通常符合预期；但当版本进入 `v0.10.0`、`v0.9.0` 等 SemVer 位数不同的场景时，字符串排序可能与语义版本顺序不一致，导致新版本继承错误的历史 usage docs 页面集合。

## 复现步骤

1. 准备多个 release 目录，其中至少包含 `releases/v0.9.0/usage-docs/` 与 `releases/v0.10.0/usage-docs/`。
2. 调用 `previous_usage_docs_version("v0.11.0")`。
3. 观察函数返回的 `source_version` 是否为 SemVer 语义上最新的已生成 usage docs 版本。
4. 再准备缺失相邻版本 usage docs 的场景，确认函数仍能继续向更早已生成 usage docs 的版本查找。

## 实际结果

当前实现按目录名字符串排序取最后一项。该策略在版本号位数变化时存在选错继承来源的风险，可能使 `source_version` 指向非 SemVer 最新的已生成 usage docs 版本。

## 期望结果

`previous_usage_docs_version()` 应按 SemVer 语义解析和排序候选版本，并选择当前版本之前最近的已生成 usage docs 版本。相邻版本没有 usage docs 时，应继续向更早版本查找；当前版本自身必须被排除。

## 影响范围

- `releases/vX.Y.Z/usage-docs/` 生成时的页面继承来源。
- `usage-docs/manifest.json` 的 `source_version`。
- `mintlify/docs/vX.Y.Z/` 与 `mintlify/docs/latest/` 的投影内容。
- usage docs 完整页面集继承校验与发布文档治理可信度。

## 严重等级说明

严重等级为 `medium`。该问题不会影响运行时业务功能，也不影响当前 `v0.3.x` 使用场景；但当版本号进入位数变化阶段后，可能造成发布使用文档继承错误，属于发布治理链路中的潜在缺陷。

## 建议修复方向

- 将 `previous_usage_docs_version()` 改为 SemVer 解析排序。
- 增加覆盖 `v0.9.0`、`v0.10.0`、缺失相邻 usage docs 版本、排除当前版本的测试。
- 明确带后缀版本的排序策略，避免 prerelease 或扩展后缀破坏既有发布流程。
