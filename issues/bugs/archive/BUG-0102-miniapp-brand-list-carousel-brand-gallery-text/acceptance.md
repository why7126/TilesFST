---
bug_id: BUG-0102-miniapp-brand-list-carousel-brand-gallery-text
acceptance_status: passed
created_at: 2026-08-02 11:49:32
updated_at: 2026-08-02 19:32:35
related_requirement: REQ-0060-brand-list-page
source_change: fix-miniapp-brand-list-carousel-text
source_sprint: sprint-017
---

# 回归验收标准

> 本 BUG 修复范围限定为小程序品牌列表页轮播图展示文案清理。必须删除多余说明文案，同时保持现有品牌页轮播图能力。

## AC-001 轮播图 MUST NOT 显示 BRAND GALLERY

**Given** 用户打开微信小程序品牌列表页  
**When** 查看品牌列表页轮播图区域  
**Then** 页面 MUST NOT 显示 `BRAND GALLERY` 文案  
**And** DOM / WXML 渲染结果中不应存在面向用户可见的该文案

## AC-002 轮播图 MUST NOT 显示中文说明文案

**Given** 用户打开微信小程序品牌列表页  
**When** 查看品牌列表页轮播图区域  
**Then** 页面 MUST NOT 显示 `轮播图保持现有品牌页能力` 文案  
**And** 该说明不得以标题、副标题、浮层、占位文字或图片覆盖层形式出现

## AC-003 轮播图现有能力 MUST 保持

**Given** 品牌列表页存在可展示的轮播图数据  
**When** 用户进入品牌列表页  
**Then** 轮播图图片 MUST 正常加载和展示  
**And** 轮播切换能力 MUST 保持  
**And** 既有点击、跳转或品牌页关联行为 MUST 保持不变

## AC-004 删除文案后布局 MUST 稳定

**Given** 修复已完成  
**When** 在小程序开发者工具或真机查看品牌列表页  
**Then** 轮播图区域 MUST 不出现因文案移除导致的空白占位  
**And** MUST 不出现遮挡、错位、高度异常或内容重叠  
**And** 品牌列表内容与轮播图区块之间的间距应保持自然

## AC-005 品牌列表页其他内容 MUST NOT 回归

**Given** 修复已完成  
**When** 浏览品牌列表页  
**Then** 品牌列表、品牌卡片、品牌名称、类目汇总和进入品牌详情页能力 MUST 保持可用  
**And** 不应引入新的 Mock 文案、调试文案或开发提示文案

## AC-006 修复范围 MUST 不涉及 API / DB / Orval

**Given** 修复已完成  
**When** 检查变更范围  
**Then** 默认 MUST 仅涉及小程序品牌列表页展示层或相关静态测试  
**And** MUST NOT 修改后端 API  
**And** MUST NOT 修改 SQLite / MySQL 表结构  
**And** MUST NOT 重新生成 Orval 客户端

## 验证记录

| 时间 | 类型 | 命令 / 证据 | 结果 |
|---|---|---|---|
| 2026-08-02 12:22:10 | static_check | `rg -n "BRAND GALLERY\|轮播图保持现有品牌页能力" src/miniapp tests/test_miniapp_static.py` | 仅剩 `tests/test_miniapp_static.py` 中的 negative assertions；`src/miniapp` 无命中 |
| 2026-08-02 12:22:10 | static_test | `uv run pytest tests/test_miniapp_static.py -k brand_list` | 1 passed, 30 deselected |
| 2026-08-02 12:22:10 | scope_check | Implementation changed miniapp brand-list WXML/WXSS and static test assertions only for this BUG; no backend API, DB schema, Orval generated client, Web admin, or Docker Compose implementation changes were made for this Change. | pass |

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-02 19:32:35
accepted_by: workflow-sync
source_change: fix-miniapp-brand-list-carousel-text
source_sprint: sprint-017
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

