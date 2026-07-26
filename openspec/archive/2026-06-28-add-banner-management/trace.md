---
change_id: add-banner-management
requirement_id: REQ-0016-banner-management
status: applied
created_at: 2026-06-28 11:25:53
updated_at: 2026-06-28 15:50:00
---

# Change Trace — add-banner-management

## 关联

| 字段 | 值 |
|---|---|
| REQ | REQ-0016-banner-management |
| Sprint | sprint-003 |
| 依赖 | add-admin-home、add-brand-management、add-tile-sku-management、update-object-storage-key-layout（Key 前缀） |
| MODIFIED | admin-dashboard、web-client、object-storage |
| NEW | banner-management |

## PNG / HTML 并排验收 Checklist

| # | 检查项 | prototype | 实现 | Pass |
|---|---|---|---|---|
| 1 | Shell + Sidebar「Banner 管理」active | banner-management-list.html | `/admin/banners` + admin-nav path | ✓ |
| 2 | 四指标卡 | banner-management-list.html | BannerManagementPage summary-grid | ✓ |
| 3 | 筛选四列（展示端/状态/时间状态） | banner-management-list.html | banner-filter-grid | ✓ |
| 4 | 表格跳转类型列 + 缩略图 86×38 | banner-management-list.html | banner-mgmt-table + banner-thumb | ✓ |
| 5 | 上线/下线确认 | acceptance AC-016 | status confirm modal | ✓ |
| 6 | 删除 ONLINE 置灰 | banner-management-list.html | disabled delete + title tooltip | ✓ |
| 7 | 分页 10/20/50 + 范围文案 | banner-management-list.html | banner-pagination 1-10 / N | ✓ |
| 8 | 弹窗 640px 无状态块 | modal-*.html | BannerFormModal banner-modal-card | ✓ |
| 9 | SKU 详情：SKU 选图 + image_source | modal-sku-detail.html | jump_type SKU_DETAIL branch | ✓ |
| 10 | 外部链接：HTTPS 字段 | modal-external-link.html | jump_type EXTERNAL_LINK branch | ✓ |
| 11 | 专题页：topic 下拉 | modal-topic-page.html | jump_type TOPIC_PAGE + topics-api | ✓ |
| 12 | 无跳转：禁用目标 | modal-no-jump.html | banner-jump-disabled | ✓ |
| 13 | Dashboard 新增 Banner 快捷 | acceptance AC-023 | DashboardPage → ?action=create | ✓ |
| 14 | 无裸 Hex | — | banner-management.css semantic tokens | ✓ |
| 15 | 列表 PNG | banner-management-list.png | 实现已 CSS Port；1440 并排待人工复核 | ○ |
| 16 | 四套 modal PNG | modal-*.png | 单弹窗 jump_type 分支；并排待人工复核 | ○ |

## 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-28 15:50:00 | Docker 冒烟 | `scripts/smoke-banner-docker.sh` 通过（pytest 14、6 routes、API 200、SPA 200、Dashboard shortcut） |
| 2026-06-28 15:40:00 | `/sprint-apply` | 实现 backend + frontend + tests + docs |
| 2026-06-28 11:25:53 | `/req-opsx` | 创建 change add-banner-management |
