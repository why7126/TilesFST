---
bug_id: BUG-0111-usage-docs-previous-version-semver-sort
title: usage docs 前置版本候选使用字符串排序可能选错版本
root_cause_status: completed
category: code
created_at: 2026-08-04 08:20:02
updated_at: 2026-08-04 08:20:02
---

# Root Cause

## 直接原因

`scripts/generate-usage-docs.py` 的 `previous_usage_docs_version()` 使用 `sorted(candidates)[-1]` 从候选版本目录名中选择前一个 usage docs 来源版本。该排序按字符串字典序执行，不理解 SemVer 的 major、minor、patch 数值含义。

## 根本原因

usage docs 生成治理在实现时只覆盖了当前 `v0.3.x` 的连续小版本场景，没有把版本号位数变化纳入排序契约和测试夹具。函数名称表达的是“前一个 usage docs 版本”，但代码缺少 SemVer 解析层，导致业务语义依赖目录名字典序。

## 触发条件

- `releases/` 下存在多个已生成 `usage-docs/` 的版本。
- 候选版本号出现位数变化，例如 `v0.9.0` 与 `v0.10.0`。
- 新版本生成 usage docs 时没有显式指定 `usage_docs.source_version`，而是依赖自动选择。

## 缺陷分类

| 维度 | 结论 |
|---|---|
| 分类 | code |
| 根因类型 | 排序契约与版本解析缺失 |
| 影响链路 | release usage docs generation |
| 是否涉及数据迁移 | 否 |
| 是否涉及运行时业务功能 | 否 |

## 证据

- 现有函数按目录名字符串排序选择候选版本。
- `v0.10.0` 与 `v0.9.0` 的字典序和 SemVer 语义顺序可能不一致。
- usage docs 治理规则要求继承前一个已生成版本的完整页面集，因此错误来源会影响后续版本文档基线。
