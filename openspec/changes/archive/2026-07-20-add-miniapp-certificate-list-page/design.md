## Context

REQ-0057 `certificate-list-page` 已完成 capture、generate、complete 和 review，当前状态为 `approved`，物理阶段为 `issues/requirements/review/`。需求文档位于 `issues/requirements/archive/REQ-0057-certificate-list-page/`。

现有 `brand-certificate-management` 能力已提供管理端证书主数据、上传、展示控制、列表筛选和通用证书展示组件。小程序侧已有 `pages/certificates/index` 作为 TabBar 占位页，且 `miniapp-home` spec 明确证书聚合页曾不进入首页首期；`miniapp-search` 已能在搜索结果中包含证书分区，但不等同于证书 Tab 的公开聚合列表。

## Goals / Non-Goals

**Goals:**

- 将小程序「证书」Tab 从占位页升级为公开证书聚合列表页。
- 复用后台品牌证书主数据和前台展示控制，公开端仅只读展示。
- 提供分页/加载更多、空/错/加载状态；证书列表页不提供搜索或筛选功能。
- 图片证书与 PDF 证书均有稳定缩略图/占位和受控预览策略。
- 覆盖小程序自定义导航、胶囊 reserve、页面 offset 和 320/375/430 pt evidence。
- API、OpenAPI/Orval、小程序服务层和测试同步闭环。

**Non-Goals:**

- 不新增管理端证书维护能力，不改管理端证书页交互。
- 不实现完整证书详情页。
- 不实现 OCR、电子签章、证书真伪校验、证书审批流。
- 不实现证书与 SKU 单独绑定。
- 不新增文件上传链路或对象存储策略。

## Decisions

### D1. 新增独立公开证书列表 API

实现阶段 SHOULD 新增 `GET /api/v1/miniapp/certificates` 或等价公开接口，而不是复用管理端 `/admin/brand-certificates`。公开接口只返回小程序展示所需字段，并在后端过滤隐藏、软删除和不可公开品牌证书。

Alternatives considered:

- 直接调用管理端 API：拒绝。该 API 需要管理权限且包含管理端筛选、指标和内部语义。
- 仅复用搜索 API 的证书分区：拒绝作为主方案。搜索 API 适合关键词结果，不适合作为 Tab 聚合页的默认分页列表事实源。

### D2. 复用证书主数据，不新增业务表

证书列表页 SHOULD 基于 `brand_certificates` 与 `brands` 查询公开数据。v1 不新增证书聚合表、详情表或证书与 SKU 绑定表。如性能需要，可增加索引或查询优化，但必须同步 DB 文档和测试。

### D3. 小程序页面负责列表状态机

`pages/certificates/index` 负责首屏加载、刷新、触底加载更多、空状态、错误态和重复请求防护。证书卡片只负责展示和触发预览/点击，不内置 API 查询或全局状态。

### D4. 文件预览使用受控 URL

图片证书优先使用小程序图片预览能力；PDF 使用受控 URL 打开、复制提示或项目确认的等价方式。任何预览路径不得暴露 MinIO 原始 object key、密钥、本机路径或未授权直连地址。

### D5. 原型冲突决议

原型位于 `issues/requirements/archive/REQ-0057-certificate-list-page/prototype/miniapp/`，优先级为 HTML > context.md > acceptance.md > `rules/ui-design.md` > OpenSpec specs。

- HTML 原型仅作为移动端信息架构和视觉密度参考，实际实现必须转换为 WXML/WXSS。
- PNG Golden Reference 暂未导出，不阻塞 Change 创建；实现阶段可补 DevTools 截图或设计截图作为 evidence。
- 若现有 `pages/certificates/index.*` 仍是占位页，必须以本 Change spec 作为目标状态。

### D6. 小程序导航与设备 evidence

实现阶段 MUST 引用 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md`，覆盖状态栏、胶囊 reserve、页面 offset、TabBar 遮挡、320/375/430 pt DevTools evidence；真机不可用时必须标记 blocked 或 follow_up，不得写作真机通过。

## Risks / Trade-offs

- [Risk] 公开接口误返回隐藏证书或内部字段 → Mitigation: 后端过滤作为唯一安全边界，测试覆盖隐藏、软删除、不可公开品牌和内部字段排除。
- [Risk] PDF 在小程序中预览能力受限 → Mitigation: design 中确认受控打开/复制提示策略，预览失败时稳定降级。
- [Risk] 与搜索证书结果口径不一致 → Mitigation: 公开列表与搜索证书分区均由后端过滤隐藏、软删除和禁用品牌证书。
- [Risk] 自定义导航和 TabBar 遮挡首屏 → Mitigation: 采用全局 `custom-navigation`，补 320/375/430 pt evidence。
- [Risk] API/Orval 遗漏导致前后端契约漂移 → Mitigation: tasks 明确 OpenAPI、Orval、docs 和测试同步。

## Migration Plan

1. 新增或确认公开证书列表 API 契约、字段和分页。
2. 实现后端公开查询，复用品牌证书数据与展示控制。
3. 同步 OpenAPI、Orval 和小程序服务层。
4. 将小程序证书 Tab 占位页替换为真实列表页。
5. 实现图片/PDF 预览、空/错/加载状态、刷新和加载更多。
6. 补充后端、小程序静态/单元测试和设备 evidence。
7. 运行 Workflow Sync，确保 REQ、Change 与 Sprint 状态一致。

Rollback 策略：如公开接口或页面验收未完成，应保留或恢复证书 Tab 的稳定占位页，不能暴露半成品列表、错误数据或未授权文件 URL。

## Open Questions

- PDF 证书在目标微信版本中采用 `wx.openDocument`、复制受控链接还是 WebView 预览，需要实现阶段技术验证后固定。
- 所属品牌“允许公开”的具体字段或状态需与现有品牌公开规则对齐；若当前没有品牌公开字段，默认使用未删除/启用品牌并在实现中说明。
