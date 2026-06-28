---
review_id: REV-REQ-0017-001
date: 2026-06-28
participants: []
result: approved
created_at: 2026-06-28 11:26:02
updated_at: 2026-06-28 11:26:02
---

# 评审结论

**REQ:** REQ-0017-system-settings  
**结果:** approved  
**评审日期:** 2026-06-28

## 摘要

管理后台系统设置需求文档完整（PRD v1）。交付范围含：侧栏 `/admin/settings` 路由、5 分组 Tab Shell、`system_settings` 持久化与 env merge、分 Phase P0–P3（基础/媒体 → 安全 → 审计 → 通知开关）。探索阶段决策已落入 PRD 与 acceptance（仅 `admin` 可访问、runtime 生效、audit 与 REQ-0014 统一、通知不发信）。5 Tab HTML + context 齐全；PNG Golden 待导出（非阻塞）。建议 OpenSpec `add-system-settings`。准予 `/req-opsx` 与 Sprint 纳入。

## 评审检查清单

- [x] 范围清晰，Out of Scope 明确（无发信引擎、无运维面板、无 `.env` 在线改桶/密钥）
- [x] 验收标准可测试（AC-001～AC-045，含 P0–P3 Phase 标记）
- [x] 优先级与依赖合理（P1；父 REQ-0004；关联 REQ-0012/0014/0015；不宜 sprint-003）
- [x] UI 类：5×HTML + context 已决；`SystemSettingsPage` 策略已写入 requirement；PNG 待导出
- [x] 无与现有 REQ 重复未说明（与用户管理/个人资料边界在 user-stories / business-flow 已对比）

## 亮点

- Phase 切分清晰，可先 P0 闭环侧栏占位再迭代安全/审计/通知。
- 媒体 Tab 桶/Key 只读与 REQ-0012 对齐，避免与对象存储 change 冲突。
- 通知 Tab 明确「仅配置、不发信」，控制 scope 膨胀。

## 风险与备注

| 项 | 说明 |
|---|---|
| 体量 | 全量 P0–P3 约 10–14 人日；建议独立 Sprint |
| REQ-0014 审计 | `audit_logs` 与 profile 活动须统一模型；opsx design 定迁移/双写 |
| REQ-0015 联动 | P1 安全策略须在改密/建用户/重置密码统一 enforcement |
| effective settings | upload/auth 须 runtime 读 DB，非进程 snapshot |
| PNG | 5 Tab Golden 待导出；opsx-apply 前 HTML 优先验收 |

## 条件通过项

- [ ] OpenSpec `design.md` 声明 prototype 优先级（HTML > PNG > context > acceptance）
- [ ] OpenSpec `tasks.md` 按 P0→P3 分任务块；P1b 登录锁定标为可选
- [ ] `design.md` 定案 Tab 切换 dirty 行为（confirm 或 discard）
- [ ] opsx-apply 前导出 `prototype/web/system-settings-*.png`（Golden 并排验收）

## 下一步

1. `/req-opsx REQ-0017-system-settings`
2. `/sprint-propose` 纳入迭代（建议 sprint-004 或独立包）
3. `/opsx-apply add-system-settings`
