---
purpose: 证据来源声明规格收敛治理日志
content: 记录 OpenSpec 正式规格旧环境分层标题重命名与 media/miniapp 证据来源声明收敛
source: /spec-opt rename-evidence-source-specs
update_method: 本日志记录单次治理事实，后续如有返修在对应 Change 或新日志中记录
created_at: 2026-08-31 14:06:32
updated_at: 2026-08-31 14:06:32
---

# 证据来源声明规格收敛治理日志

## 迭代目标

清理正式 OpenSpec 中仍残留的“环境分层”“生产证据后置”“强脚本门禁”等旧命名，将 media 与 miniapp 历史规格收敛为“证据来源声明 / 证明边界 / 手动诊断”语义。

## 变更摘要

- 创建 `rename-evidence-source-specs` OpenSpec Change，并纳入 `sprint-029`。
- 在 delta spec 中移除旧环境分层 requirement，新增证据来源声明与诊断相关 requirement。
- 将 media 与 miniapp 模板规格中的生产后置和目标环境分层语义收敛为证据来源、不可验证原因、后续承接方式或 N/A 理由。
- 保留 `production_only_pending` 为历史兼容字段，不作为新流程推荐分类。

## 影响范围

- OpenSpec delta：`agent-workflow-tooling`、`testing`、`media-acceptance-template`、`miniapp-device-evidence-template`。
- 迭代治理：`sprint-029` scope。
- 规范工程日志：`docs/spec-logs/CHANGELOG.md` 与本日志。

## 更新文件

- `openspec/changes/rename-evidence-source-specs/`
- `iterations/change/sprint-029/sprint.yaml`
- `docs/spec-logs/CHANGELOG.md`
- `docs/spec-logs/20260831140632-governance-evidence-source-specs.md`

## 关键决策

- 已采纳：使用 OpenSpec delta 表达正式规格标题重命名，归档时再合并到 `openspec/specs/`。
- 未采纳：不直接修改 `openspec/specs/`，避免绕过 OpenSpec 归档合并流程。
- 替代方案：保留手动诊断脚本和历史兼容字段，由文案明确其边界。
- 验证责任：本次通过 OpenSpec、目录结构、上下文预算、Sprint scope 与文档卫生聚焦校验确认。
- 后续触发条件：若归档后仍检出正式规格旧标题，应走 `/opsx-archive rename-evidence-source-specs` 合并 delta 或执行返修。

## 影响声明

- API：不影响。
- DB：不影响。
- Web：不影响。
- 小程序：不修改运行时代码，仅调整小程序证据模板规格语义。
- 管理端：不影响。
- Orval：不需要。
- Docker Compose：不需要。

## 验证结果

OpenSpec、目录结构、上下文预算和文档卫生聚焦校验通过；文档卫生仅返回启发式 warning，未发现阻断项。Sprint scope 在同步 `sprint.md` 目标编号列表后通过。

## 后续建议

执行 `/opsx-archive rename-evidence-source-specs`，将 delta 合并进正式规格并关闭该治理 Change。
