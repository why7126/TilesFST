---
created_at: 2026-08-22 14:12:50
updated_at: 2026-08-22 14:12:50
---

# 设计说明

## 规则归属

详细规则归属到 `rules/iterations-lifecycle.md`，`AGENTS.md` 只保留摘要，`sprint-propose` 技能承接命令执行步骤。

## Sprint 选择门禁

新增 `scripts/validate-sprint-selection.py` 作为轻量门禁：

- 统计 `iterations/change/sprint-[0-9]{3}/` active Sprint。
- 同时扫描 `iterations/change/` 和 `iterations/archive/` 的目录名与 `sprint.yaml:sprint_id`，计算下一个允许 Sprint ID。
- 未指定 Sprint 时根据 active Sprint 数量决定默认选择或阻断。
- 指定 Sprint 时校验格式、是否为已有 active Sprint、或是否为下一个连续编号；两个 active Sprint 时禁止再新建第三个。

## 容量取舍

保留现有容量策略：

- `estimated_person_days <= capacity_person_days`：正常通过。
- `capacity_person_days < estimated_person_days <= capacity_person_days * 1.2`：允许继续，但必须写容量风险。
- `estimated_person_days > capacity_person_days * 1.2`：硬阻断；若用户仍要继续，只能拆分范围或指定下一个连续 Sprint 重新规划。

## 归档冻结边界

归档冻结面向开发链路写入命令，防止已闭环事实被反向改写。允许命令仅可消费归档事实生成复盘、发布、镜像或升级材料。若发现归档路径残留、敏感信息或状态漂移，必须通过明确治理命令和校验处理，不得借普通开发命令修改归档对象。
