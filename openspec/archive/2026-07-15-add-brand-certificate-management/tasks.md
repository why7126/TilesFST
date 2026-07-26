## 1. 数据模型与后端基础

- [x] 1.1 新增 `brand_certificates` SQLite/MySQL schema、migration / 初始化脚本，并同步 `docs/04-database-design.md`。
- [x] 1.2 新增品牌证书 Pydantic schemas，覆盖列表查询、创建、更新、响应、summary、有效状态和错误响应。
- [x] 1.3 新增 repository/service，支持分页筛选、详情、创建、更新、显示、隐藏、软删除、同品牌名称唯一性和有效状态计算。
- [x] 1.4 增加品牌删除前证书约束，存在未删除证书时阻止删除或要求先迁移/删除。
- [x] 1.5 增加品牌证书权限点和审计记录写入，覆盖新增、编辑、显示、隐藏、删除。

## 2. API、上传与文档同步

- [x] 2.1 新增 `/api/v1/admin/brand-certificates` 列表、创建、详情、更新、show、hide、delete API。
- [x] 2.2 新增或扩展证书文件上传端点，支持 JPG、PNG、WebP、PDF，单文件最大 20MB，并返回 `file_url` / `file_key` / 文件元数据。
- [x] 2.3 确保证书文件经后端鉴权、MIME/大小校验、对象 Key 校验和 MinIO 单桶写入，前端不直连未授权对象存储。
- [x] 2.4 同步错误码、OpenAPI、Orval 客户端、`docs/03-api-index.md` 和相关 API governance 文档。
- [x] 2.5 补充后端 pytest 集成测试，覆盖权限、筛选、创建/更新校验、显示隐藏、软删除、品牌删除约束和上传错误。

## 3. Web 管理端实现

- [x] 3.1 新增 `/admin/brand-certificates` 路由、左侧导航入口和品牌列表页“证书”快捷筛选入口。
- [x] 3.2 实现品牌证书列表页，复用 `AdminListPage` / shared UI，覆盖指标、即时筛选、URL Query、列表、空态、错态和分页。
- [x] 3.3 实现新增/编辑证书弹窗，宽 760px，头尾固定，body 可滚动，支持长期有效联动和服务端错误保留。
- [x] 3.4 实现证书文件上传控件，覆盖 `idle → uploading → done / failed` 状态、图片/PDF 回显、重新上传和移除。
- [x] 3.5 实现预览、显示/隐藏、删除 DS confirm、fixed toast 和权限控制，不使用 `window.confirm`。
- [x] 3.6 使用 semantic token 与 `cn()`，不得复制原型裸 Hex；必要时同步 Design System 预览。

## 4. 前端测试与视觉验收

- [x] 4.1 增加 Vitest / Testing Library 测试，覆盖列表筛选、URL Query、分页结构、弹窗字段、长期有效联动和权限入口。
- [x] 4.2 增加上传组件测试，覆盖成功回显、失败原因、重新上传、移除和 PDF 文件卡片。
- [x] 4.3 完成 1440x1024 列表页一致性验收，确认分页 DOM、指标卡结构和 fixed toast 无 layout shift。
- [x] 4.4 完成弹窗 Computed width 760px、无 `modal-card` 双挂载、矮视口 body scroll 验收。
- [x] 4.5 完成 Docker Web `http://localhost:3000` 上传边界文件验收，确认超限文件返回业务错误而非 413。

## 5. 工作流、追溯与校验

- [x] 5.1 更新 Change `trace.md`，记录实现证据、原型冲突处理、PNG/HTML 参考结论和 knowledge-base 横切 AC 验收结果。
- [x] 5.2 运行 OpenSpec validate、后端测试、前端测试、Orval 生成校验和必要 Docker Compose 验证。
- [x] 5.3 运行 Workflow Sync，确保 `REQ-0038`、Change、Sprint 范围和 registry 状态一致。
- [x] 5.4 若实现涉及新增环境变量或上传边界配置，同步 `.env.example`、部署文档和文件上传标准文档。
