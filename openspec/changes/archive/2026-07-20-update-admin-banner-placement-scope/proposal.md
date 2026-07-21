## Why

当前 Banner 管理能力支持 Web 首页、小程序首页、专题页等多个展示端与位置，但当前产品投放范围已经收敛到微信小程序首页轮播和品牌列表页轮播。运营继续看到旧展示端和旧位置会增加误配置风险，品牌列表页也需要独立轮播数据来源，不能长期复用首页轮播。

## What Changes

- **BREAKING** 删除历史旧 Banner 数据：非小程序展示端、首页中部运营位、专题页 Banner 和其他无法映射到新范围的旧位置均清理删除。
- 管理端 Banner 展示端收敛为“小程序”，展示位置收敛为“首页轮播”和“品牌列表页轮播”。
- 后端 Banner 校验只接受小程序首页轮播和小程序品牌列表页轮播两个位置组合。
- 小程序首页只读取首页轮播；品牌列表页只读取品牌列表页轮播，不再互相兜底。
- 同步 API、OpenAPI、Orval、SQLite/MySQL schema、数据库文档和测试要求。
- 保留 Banner 图片上传和跳转类型能力，但回归管理端列表、弹窗宽度和上传链路横切验收。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `banner-management`: 收敛 Banner 展示端/展示位置合法组合，定义旧数据删除策略和品牌列表页轮播位置。
- `web-client`: 更新管理端 Banner 列表、筛选、弹窗展示端/展示位置选项和横切 UI 验收。
- `miniapp-home`: 明确小程序首页只读取首页轮播位置，不读取品牌列表页轮播。
- `database`: 要求 SQLite/MySQL 对 Banner 展示端、展示位置和旧数据删除迁移保持一致。

## Impact

- **backend/api:** 调整 Banner 创建/更新校验、列表默认范围、旧数据删除迁移、小程序轮播查询；同步 OpenAPI 和后端测试。
- **database:** 更新 SQLite schema/migration、MySQL schema 和数据库文档；迁移删除旧 Banner 业务记录，不物理删除 MinIO 对象。
- **web/admin:** 更新 `/admin/banners` 筛选、列表文案、新增/编辑弹窗默认值和选项；保留 DS confirm、fixed toast、分页和上传回显验收。
- **miniapp:** 首页与品牌列表页轮播查询分流，品牌列表页不能使用首页轮播兜底。
- **storage/media:** Banner 图片仍走后端鉴权和 MinIO 适配层；删除 Banner 记录不自动物理删除对象。
- **docs/tests:** 同步 API 文档、数据库文档、Orval、后端 pytest、前端 Vitest、小程序静态/查询测试和 Docker `:3000` 上传边界验收。
