---
change_id: fix-openspec-archive-scaffold-warning-noise
title: 吸收 OpenSpec 归档英文脚手架兼容 warning 噪音任务
status: applied
source_bug: BUG-0119-openspec-archive-scaffold-warning-noise
created_at: 2026-08-06 10:39:32
updated_at: 2026-08-06 10:54:33
---

# 任务

- [x] 1. 定位 `scripts/archive-change.sh` 中 OpenSpec CLI stderr 收集、归档成功判定和最终说明输出逻辑。
- [x] 2. 实现已知英文脚手架兼容 warning 的窄匹配规则，仅匹配 `proposal.md` 缺少英文 `## Why` / `## What Changes` 的非阻塞提示。
- [x] 3. 在 OpenSpec CLI 成功且项目中文语言校验通过时，吸收唯一的已知兼容 warning，不再输出固定归档说明。
- [x] 4. 保留真实错误、未知 stderr、目录结构错误和中文语言校验失败的原有阻断或 warning 输出。
- [x] 5. 新增或更新脚本级测试，覆盖仅已知 warning 静默、未知 stderr 暴露、语言校验失败阻断三类场景。
- [x] 6. 运行相关脚本测试与 `python scripts/validate-openspec-language.py`。
- [x] 7. 复核不涉及 API、数据库、Web、小程序、管理端、Orval 或 Docker Compose。
- [x] 8. 若修复经验具备复用价值，归档前评估是否需要沉淀到 `docs/knowledge-base/incidents/`。
