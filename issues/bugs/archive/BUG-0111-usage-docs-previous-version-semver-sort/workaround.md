---
bug_id: BUG-0111-usage-docs-previous-version-semver-sort
title: usage docs 前置版本候选使用字符串排序可能选错版本
workaround_status: available
created_at: 2026-08-04 08:20:02
updated_at: 2026-08-04 08:20:02
---

# Workaround

## 临时规避方案

在正式修复前，生成新版本 usage docs 时如果版本号已经进入可能触发字符串排序偏差的区间，应在 `releases/<version>/release.json` 的 `usage_docs.source_version` 中显式指定正确的继承来源版本。

## 操作要点

1. 先确认目标版本前最近一个已生成 usage docs 的版本。
2. 在目标版本 `release.json` 中显式设置 `usage_docs.source_version`。
3. 再运行 `python scripts/generate-usage-docs.py <version>`。
4. 生成后检查 `releases/<version>/usage-docs/manifest.json` 的 `source_version` 是否符合预期。
5. 运行 `python scripts/validate-usage-docs.py --release-dir releases/<version>` 确认完整页面集继承未丢失。

## 限制

- 该规避依赖人工识别正确来源版本，容易遗漏。
- 只能避免单次生成选错来源，不能修复脚本默认行为。
- 如果已经基于错误来源生成了文档，需要重新生成或人工更正文档快照，并保留维护记录。

## 长期修复建议

将 `previous_usage_docs_version()` 改为 SemVer 解析排序，并补充自动化测试覆盖版本位数变化、缺失相邻 usage docs 版本和当前版本排除场景。
