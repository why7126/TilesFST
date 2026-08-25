# BUG 评审通过根因 confirmed 门禁设计

## 现状

`/bug-review` 无 flag 默认通过，且 approve 后会进入 `approved` 并迁入 `issues/bugs/review/`。根因证据规则已经定义 `confirmed` 是唯一具备闭环证据、可作为修复与验收依据的状态，但当前脚本只把非法状态和 confirmed 缺证据作为 blocker，非 confirmed 状态仍可停留在 warning 层。

## 目标

在 BUG 进入 `approved` 前建立可执行门禁，使每个被确认修复的 BUG 都具备 confirmed 根因和证据链。

## 实现方案

1. 在 `scripts/validate-root-cause-evidence.py` 增加 `--require-confirmed` 参数。
2. 普通审计模式保持原有行为：非 confirmed 可作为 warning，用于探索和批量扫描。
3. `--require-confirmed` 模式用于 `/bug-review` approve 门禁：
   - 缺少 `root-cause.md` 为 blocker。
   - 缺少 `root_cause_status` 或“根因状态”为 blocker。
   - 状态不在允许集合为 blocker。
   - 状态不是 `confirmed` 为 blocker。
   - `confirmed` 但缺少证据链关键词仍为 blocker。
4. `/bug-review` 在写入评审结果、状态变更、目录迁移和 Workflow Sync 前运行该门禁。
5. 规则与入口文档只写摘要，详细事实源放在 `rules/root-cause-evidence.md` 和 `rules/bug-management.md`。

## 取舍

- 保留普通审计模式的 warning 行为，避免 `/explore` 或批量扫描因未确认根因的计划中 BUG 全量失败。
- 不新增独立 `bug-review` 脚本；当前项目以 Skill 驱动命令执行，门禁由 Skill 调用现有校验脚本承接。
- 不自动把 `probable` 升级为 `confirmed`；证据状态必须由 `/bug-complete` 或人工补证后更新。

## 验证

- 聚焦 pytest 覆盖 confirmed、probable、缺文件和默认模式兼容。
- 运行目标脚本真实命令验证 active BUG 中 probable 状态会被 `--require-confirmed` 阻断。
- 运行治理门禁：上下文预算、OpenSpec 语言、目录结构、OpenSpec validate 和文档卫生校验。
