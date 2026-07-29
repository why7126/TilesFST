## 1. Data Model and Backend Contract

- [x] 1.1 设计并实现证书图片存储结构或等价兼容层，支持文件引用、受控读取 URL、文件名、MIME、大小、`is_main`、`sort_order`。
- [x] 1.2 为 SQLite/MySQL 增加 migration 或兼容转换逻辑，并更新 `docs/04-database-design.md` 对应表结构。
- [x] 1.3 扩展品牌证书 Pydantic Schema，支持图片数组、主图、排序和旧单文件 fallback。
- [x] 1.4 在后端保存逻辑中校验主图唯一性、图片数量上限和文件引用合法性。
- [x] 1.5 在列表和详情服务层统一组装 `images`、`main_image` 和 PDF/旧单文件兼容展示模型。

## 2. API, OpenAPI, and Orval

- [x] 2.1 更新管理端品牌证书创建、更新、详情和列表 API 请求/响应，返回图片列表和主图信息。
- [x] 2.2 同步 API 文档、错误码说明和上传边界说明。
- [x] 2.3 重新生成 OpenAPI 和 Orval 客户端，并检查前端调用不手写重复类型。
- [x] 2.4 回归未认证、无权限、非法文件引用、多主图和无主图异常 payload 的错误响应。

## 3. Admin Web UI

- [x] 3.1 更新 `/admin/brand-certificates` 列表证书列，优先使用主图缩略图，缺失或加载失败时展示稳定占位。
- [x] 3.2 更新新增/编辑证书弹窗，支持多张图片上传、上传状态、失败提示、删除图片和设置主图。
- [x] 3.3 实现第一张图片默认主图、设置主图前置、删除主图兜底和删除全部图片空状态。
- [x] 3.4 保持弹窗 Computed width 为 760px，矮视口 body 可滚动，底部保存按钮可达。
- [x] 3.5 保持 fixed toast、DS confirm、分页 DOM、指标卡 DOM 和 semantic token 约束不回归。
- [x] 3.6 管理端品牌证书列表操作列移除“预览”按钮，仅保留编辑、显示/隐藏、删除等管理操作。
- [x] 3.7 证书图片上传空态文案改为网格下方 `.sku-help` 提示，避免占用图片格，并与 SKU 图片上传提示样式一致。

## 4. Storage and Upload Verification

- [x] 4.1 复用后端鉴权上传与对象存储适配层，禁止前端直连未授权对象存储。
- [x] 4.2 确认证书图片上传 MIME、扩展名和大小限制与前端提示、后端校验、部署代理配置一致。
- [x] 4.3 通过 Docker Web 入口 `http://localhost:3000` 验证合法小图成功、超限图片返回业务错误而非 Nginx 413。
- [x] 4.4 确认新上传不写入 `data/uploads/`，删除图片仅解除业务关联，不物理删除对象。

## 5. Tests and Acceptance

- [x] 5.1 增加后端测试覆盖多图保存、主图唯一性、图片顺序回填、旧单文件兼容和非法文件引用拒绝。
- [x] 5.2 增加前端测试覆盖上传成功回显、上传失败、设置主图、删除非主图、删除主图兜底和删除全部图片。
- [x] 5.3 回归品牌证书列表缩略图、编辑弹窗回填、PDF/文档占位兼容和权限可见性。
- [x] 5.4 运行相关 pytest 与 Vitest；若 API contract 变化，确认 Orval 生成物和测试夹具同步。
- [x] 5.5 回归小程序证书列表/品牌证书 Tab 主图 URL、证书卡片样式和 tabbar 激活态静态合同。

## 6. Documentation and Trace

- [x] 6.1 更新 `docs/03-api-index.md`、`docs/04-database-design.md`、上传/对象存储相关文档和 `.env.example`（如新增配置）。
- [x] 6.2 在 apply 输出中记录 prototype conflict resolution：静态 HTML 的 880px 不作为最终弹窗宽度，实际保持 760px。
- [x] 6.3 完成后运行 Workflow Sync，确保 REQ、Change 和 Sprint 派生状态一致。
- [x] 6.4 补充 follow-up 文档记录：小程序公开证书主图展示、证书卡片高度、tabbar 激活态和管理端证书图片上传文案一致性。
