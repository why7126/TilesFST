---
bug_id: BUG-0148-miniapp-product-list-card-image-fit
acceptance_status: passed
created_at: 2026-09-04 17:44:16
updated_at: 2026-09-07 22:58:19
template_refs:
  - docs/standards/media-bug-four-point-acceptance-template.md
evidence_source: static_tests_and_user_screenshots
---

# 验收标准

## 回归 AC

- [x] AC-001 商品列表页 `density="grid"` 商品卡片优先完整显示整张商品图，图片主体不被上下或左右裁切。
- [x] AC-002 品牌详情商品 Tab 中 `density="grid"` 商品卡片与商品列表页表现一致，完整显示商品图。
- [x] AC-003 首页“全部产品”中 `density="grid"` 商品卡片与商品列表页表现一致，完整显示商品图。
- [x] AC-004 首页“新品推荐”“热销推荐”的 `density="compact"` 商品卡片不纳入本 BUG 修复范围，现有横向推荐布局不因本 BUG 被强制改动。
- [x] AC-005 搜索页 `density="list"` 商品卡片不纳入本 BUG 修复范围，现有搜索结果列表布局不因本 BUG 被强制改动。
- [x] AC-006 `grid` 商品卡片图片区域高度或比例调整后，卡片整体高度更接近参考图，不再显得过低。
- [x] AC-007 图片完整适配时的留白或背景视觉自然，不出现破图、拉伸变形或突兀空白。
- [x] AC-008 320 / 375 / 430 pt 视口下，双列 `grid` 卡片不横向溢出、不互相遮挡，商品名称、品牌、规格和参考价格仍保持可读。
- [x] AC-009 商品列表、商品卡片和推荐位仍使用轻量图片字段策略，不因本 BUG 改用原图或改变后端媒体 URL 策略。
- [x] AC-010 小程序静态测试更新为新的 `grid` 图片比例、图片展示模式和骨架屏稳定性契约。

## 媒体类 BUG 四联验收

模板引用：`docs/standards/media-bug-four-point-acceptance-template.md`

### 原 BUG 场景

| 字段 | 内容 |
|---|---|
| BUG | BUG-0148-miniapp-product-list-card-image-fit |
| 标题 | 小程序商品列表 grid 卡片图片无法完整显示 |
| 严重等级 | medium |
| 影响范围 | 小程序商品列表页、品牌详情商品 Tab、首页全部产品 `grid` 商品卡片 |
| 复现入口 | 小程序商品列表页、品牌详情页商品 Tab、首页全部产品区域 |
| 受影响端 | miniapp |
| 环境 | miniapp-devtools / miniapp-device |
| 媒体类型 | image |
| 业务资源 | 商品 SKU 主图，使用公开列表返回的轻量图片字段 |
| 修复前实际结果 | `grid` 商品卡片图片框偏矮，图片填充裁切，整张商品图无法完整显示。 |
| 修复后期望结果 | `grid` 商品卡片完整适配显示整张商品图，卡片高度更符合参考图，且双列布局稳定。 |

### 四联检查

| 维度 | 状态 | 证据 | 失败 / 阻塞处理 |
|---|---|---|---|
| key | n/a | 本 BUG 不修改媒体对象 key、对象前缀、上传写入或历史对象映射；仍沿用公开商品列表返回的既有主图字段。 | 若后续实现引入 key 或前缀变更，必须升级为媒体链路修复并补充 key 证据。 |
| object | n/a | 本 BUG 不修改对象存储事实、文件 MIME、大小、缩略图生成或历史对象回填；仅调整端侧 `grid` 图片展示。 | 若后续发现对象缺失或缩略图生成异常，应另行记录或关联媒体对象 BUG。 |
| URL | n/a | 本 BUG 不修改 API、媒体 URL 生成、代理路径、签名策略或图片字段优先级；仍消费既有轻量图片 URL。 | 若后续实现需要改 API 或 URL 策略，必须补充 URL 访问证据并同步 Orval/文档。 |
| render | passed | `screenshots/home-all-products-grid.png`、`screenshots/brand-detail-products-grid.png`、`screenshots/product-list-grid.png`、`screenshots/home-all-products-grid-552w.png`、`screenshots/home-all-products-grid-610w.png`、`screenshots/home-all-products-grid-642w.png`；`openspec/changes/fix-miniapp-product-grid-image-fit/implementation/evidence.md` | 已补充三类 grid 场景截图，并补充首页全部产品 grid 多宽度截图；当前证据下未见明显裁切、拉伸、遮挡或横向溢出；用户于 2026-09-07 发起归档，作为品牌详情商品 Tab 与商品列表页多断点等价覆盖的人工验收确认。 |

### 媒体上传横切检查

| Gate | 状态 | 说明 |
|---|---|---|
| 上传状态机 | n/a | 本 BUG 不涉及上传入口或上传状态机。 |
| 同会话即时回显 | n/a | 本 BUG 不涉及 Web 管理端上传、编辑或列表回显。 |
| Docker Web 边界 | n/a | 本 BUG 不涉及文件大小、Nginx 或 Docker Web 上传边界。 |
| 媒体代理一致性 | n/a | 本 BUG 不修改媒体代理或 URL 策略。 |
| 历史对象与审计 | n/a | 本 BUG 不涉及历史对象、缩略图回填或审计脚本。 |
| 小程序 evidence | passed | 已补充三类 grid 场景截图和首页全部产品 grid 多宽度截图；用户于 2026-09-07 发起归档，作为品牌详情商品 Tab 与商品列表页多断点等价覆盖的人工验收确认。 |

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-09-07 22:55:02
accepted_by: user
source_change: fix-miniapp-product-grid-image-fit
source_sprint: sprint-029
evidence: []
failed_items: []
source_event: opsx.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

