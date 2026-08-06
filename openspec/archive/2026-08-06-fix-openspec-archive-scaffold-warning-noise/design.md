---
change_id: fix-openspec-archive-scaffold-warning-noise
title: 吸收 OpenSpec 归档英文脚手架兼容 warning 噪音设计
status: applied
source_bug: BUG-0119-openspec-archive-scaffold-warning-noise
created_at: 2026-08-06 10:39:32
updated_at: 2026-08-06 10:54:33
---

# 设计

## 根因摘要

归档封装层没有结构化区分“上游 CLI 英文脚手架兼容 warning”和“项目真实归档风险”。OpenSpec CLI 对 `proposal.md` 英文标题的提示与项目中文优先规则存在已知兼容差异；当前流程虽将其标记为非阻塞，但仍在最终归档说明中反复暴露。

## 修复方案

1. 在归档封装层定义稳定的已知 warning 判定规则，匹配 `proposal.md` 缺少英文 `## Why` / `## What Changes` 的 OpenSpec CLI 兼容提示。
2. 收集 OpenSpec CLI stderr 后，先区分已知兼容 warning 与未知 stderr。
3. 当满足以下条件时静默吸收固定提示：
   - OpenSpec CLI 退出码表示归档成功。
   - stderr 仅包含已知英文脚手架兼容 warning。
   - `python scripts/validate-openspec-language.py` 通过。
4. 当存在未知 stderr、CLI 失败、目录结构错误或中文语言校验失败时，保留原有失败或 warning 输出。
5. 保持 Change 文档中文优先，不通过增加英文标题规避上游 CLI 提示。

## 测试策略

- 增加脚本级单元或集成测试，模拟仅已知 CLI warning 且语言校验通过的归档结果，确认最终输出不再包含固定非阻塞说明。
- 增加未知 stderr 场景，确认输出仍保留未知 warning 或 error。
- 增加中文语言校验失败场景，确认归档流程仍阻断。
- 运行 `python scripts/validate-openspec-language.py` 校验本 Change 文档语言规范。

## 边界说明

- API：不新增或修改接口，不需要 OpenAPI / Orval。
- 数据库：不修改 schema 或迁移。
- Web / 小程序 / 管理端：不修改运行时功能。
- 部署：不修改 Docker Compose 或环境变量。

## 风险

- 过滤规则过宽可能吞掉真实 stderr。测试必须覆盖未知 stderr，并要求匹配规则足够窄。
- 过滤规则过窄可能继续暴露噪音。测试应包含当前 BUG 中记录的固定提示文本或等价片段。
