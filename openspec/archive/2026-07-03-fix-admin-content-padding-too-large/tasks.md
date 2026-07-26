---
change_id: fix-admin-content-padding-too-large
title: 管理端全局内容区域间距与宽度收敛修复 - 任务
created_at: 2026-07-03 18:41:48
updated_at: 2026-07-03 23:36:41
source_bug: BUG-0054-admin-content-padding-too-large
status: proposed
---

# Tasks

## 1. Web 管理端 Shell 修复

- [x] 1.1 在 `admin-home.css` 将 desktop `.main-content` 调整为 `padding: 24px 24px 48px`。
- [x] 1.2 将 ≤1023px `.main-content` 调整到 `20px 16px 40px` 量级。
- [x] 1.3 将 ≤639px `.main-content` 调整到 `16px 12px 32px` 量级。
- [x] 1.4 将 `.content-inner` 从 1080px 硬上限改为 `max-width: min(1440px, 100%)` 或 `max-width: 100%`，并在 trace 记录最终选择。
- [x] 1.5 保持 `.main-content` 独立滚动、Sidebar 264px / 72px 宽度、collapsed localStorage 行为不变。

## 2. 页面级宽度分叉清理

- [x] 2.1 删除或改造 `tile-sku-management.css` 中 SKU 页 `content-inner` 1120px override。
- [x] 2.2 删除或改造 `system-settings.css` 中 `settings-content-inner` 1080px 页面级容器限制。
- [x] 2.3 检查 Web 管理端 CSS，确认无新增 `content-inner` / `settings-content-inner` divergent max-width。

## 3. 回归测试与静态断言

- [x] 3.1 更新或新增 `AdminLayout` 相关测试，覆盖 Shell 基础结构仍包含 `main-content` / `content-inner`。
- [x] 3.2 增加样式静态断言，确保旧值 `48px 56px 72px`、`.content-inner max-width: 1080px`、SKU 1120px override 不再出现。
- [x] 3.3 保持 `AdminSidebar.collapse.test.tsx` 通过，确认侧栏折叠行为不回归。
- [x] 3.4 视实现范围补充日志审计、SKU、用户、Dashboard 或系统设置页面 smoke 测试。

## 4. 视觉验收

- [ ] 4.1 在 1440px desktop expanded 下验收 `/admin/logs`、`/admin/tile-skus`、`/admin/users`、`/admin/dashboard`、`/admin/settings`。
- [ ] 4.2 在 1920px desktop expanded 下验收内容区不再被 1080/1120px 锁死。
- [ ] 4.3 验收 desktop collapsed sidebar 下内容区可用宽度增加且无横向错位。
- [ ] 4.4 验收 tablet / mobile 下内容不贴边、侧栏响应式行为不回归。

## 5. 验证与追溯

- [x] 5.1 运行相关 Vitest / Testing Library 测试。
- [x] 5.2 运行 `openspec validate fix-admin-content-padding-too-large --strict`。
- [x] 5.3 运行 `python scripts/validate-directory-structure.py`。
- [x] 5.4 确认不需要执行 Orval、后端 pytest、数据库迁移或 Docker Compose 验证，并在 trace 中记录原因。
- [x] 5.5 更新 BUG trace 与 OpenSpec trace。
- [x] 5.6 若修复过程发现可复用故障经验，补充 `docs/knowledge-base/incidents/`；若无复用价值，在验收记录中说明不沉淀。
