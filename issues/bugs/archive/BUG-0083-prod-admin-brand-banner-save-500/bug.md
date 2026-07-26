---
bug_id: BUG-0083-prod-admin-brand-banner-save-500
title: 生产环境创建品牌类型 Banner 保存接口返回 500
severity: high
status: done
owner:
discovered_at: 2026-07-23 10:35:53
environment: 生产环境管理端
related_requirement: REQ-0062-admin-banner-placement-scope
related_change: fix-admin-banner-create-schema-drift
created_at: 2026-07-23 10:46:22
updated_at: 2026-07-23 22:59:48
---

# 现象

生产环境管理端创建品牌类型 Banner 时，点击保存仍然失败。

本次已明确观测到保存接口返回 `500 Internal Server Error`：

- 请求方法：`POST`
- 请求地址：`https://tilesfst.wjoyhappy.site/api/v1/admin/banners`
- HTTP 状态：`500 Internal Server Error`

该缺陷与已归档缺陷 `BUG-0075-prod-admin-brand-banner-save-fails` 高度相关。`BUG-0075` 已针对“生产环境管理端品牌类型 Banner 配置无法保存”完成修复并归档，但当前生产环境创建路径仍返回 500，倾向为回归或残留缺陷。

# 复现步骤

1. 登录生产环境管理端。
2. 进入 Banner 管理或 Banner 配置页面。
3. 新建一条 Banner。
4. 将跳转类型配置为品牌详情或品牌类型。
5. 选择一个品牌。
6. 配置 Banner 图片，可使用品牌 Logo 或自定义上传运营图。
7. 填写标题、展示位置、排序、有效期、备注等字段。
8. 点击保存 Banner。
9. 在浏览器 Network 中观察 `POST /api/v1/admin/banners` 的响应状态。

# 期望结果

- 合法的品牌类型 Banner 可以创建保存成功。
- 保存成功响应应为统一 envelope，并返回 `jump_type = BRAND_DETAIL`、正确 `brand_id`、`image_source`、`image_object_key` 等字段。
- 保存后的 Banner 能在管理端列表、详情和编辑弹窗中稳定回显。
- 如果配置不合法，系统应返回明确 4xx 错误码和可理解提示，例如品牌不存在、品牌未启用、品牌无 Logo、品牌 Logo 引用不一致或标题重复。
- 接口不应对可预期业务错误或数据库结构漂移返回裸 500。

# 实际结果

生产环境创建品牌类型 Banner 时，保存接口返回 `500 Internal Server Error`，导致 Banner 无法保存。

目前尚未取得完整请求 payload、响应 body、request_id 和后端异常日志，因此还不能最终确认具体 SQL 异常或运行时异常类型。

# 影响范围

| 范围 | 影响 |
|---|---|
| 生产管理端 | 运营人员无法创建品牌类型 Banner |
| Banner 管理 | 品牌详情跳转 Banner 的创建链路被阻断 |
| 小程序展示端 | 依赖品牌类型 Banner 的首页轮播或品牌列表页轮播无法上线或更新 |
| 品牌导流 | 品牌主页/品牌详情页入口投放受影响 |
| 发布质量 | 已归档修复后再次失败，暴露生产回归验证或数据库迁移闭环不足风险 |

# 严重等级说明

严重等级：`high`。

理由：

- 缺陷发生在生产环境。
- 保存接口返回 500，属于用户不可恢复的服务端错误。
- 直接阻断运营创建品牌类型 Banner，影响品牌运营位配置和线上导流。
- 该问题与已修复归档的 `BUG-0075` 相同能力域相关，存在回归风险。

# 初步分析

当前后端创建 Banner 的持久化链路会向 `banners` 表写入：

- `title`
- `display_client`
- `position`
- `image_object_key`
- `image_source`
- `sku_gallery_asset_id`
- `jump_type`
- `sku_id`
- `external_url`
- `topic_id`
- `brand_id`
- `sort_order`
- `valid_from`
- `valid_to`
- `status`
- `remark`
- `created_at`
- `updated_at`

本地后端新库路径已有品牌详情 Banner 创建、编辑、品牌 Logo、自定义上传图和失败场景测试覆盖，说明当前代码与全新 schema 基本匹配。生产返回 500 更倾向于生产环境差异，优先怀疑生产 MySQL `banners` 表仍与 `schema.mysql.sql` 存在 drift。

历史 `BUG-0075` 的修复重点是 MySQL 兼容迁移补齐 `banners.brand_id`、相关索引和外键。但如果生产旧表缺失的不止 `brand_id`，例如缺少 `image_source`、`sku_gallery_asset_id`、`topic_id`、`valid_from`、`valid_to` 或 `remark`，当前创建 SQL 仍可能触发 `Unknown column` 等数据库异常并返回 500。

次要可能原因：

- 生产后端未部署包含 MySQL 兼容迁移的镜像版本。
- 应用启动时未执行或未成功执行 MySQL 兼容迁移。
- 生产 Web bundle 与后端镜像版本不一致，导致 payload 字段或枚举值漂移。
- 所选品牌在生产环境不是 `ENABLED` 状态，或品牌 Logo key 与提交的 `image_object_key` 不一致；这类业务问题按设计应返回 400 / `30052`，不是 500。
- 同一展示端与展示位置下标题重复、外键约束失败或数据长度超限。

# 待补充信息

| 信息 | 说明 |
|---|---|
| 请求 payload | 保存失败时 `POST /api/v1/admin/banners` 的完整 JSON 请求体 |
| 响应 body | 500 响应体、request_id、错误码或网关错误内容 |
| 后端日志 | FastAPI / SQLAlchemy / MySQL 异常堆栈，重点关注 `Unknown column`、外键失败、唯一约束失败、数据长度错误 |
| 生产表结构 | 运行 MySQL schema drift 检查，确认 `banners` 是否缺列 |
| 部署版本 | 生产后端镜像与 Web bundle 是否来自同一修复版本 |
| 品牌数据 | 所选品牌状态、`logo_object_key`、提交 `image_object_key` 是否一致 |

# 建议复现与验证

1. 在生产环境抓取失败请求的 payload、响应 body 和 request_id。
2. 对应 request_id 查询后端日志，定位未捕获异常。
3. 对生产 MySQL 执行只读 schema drift 检查：

```bash
python scripts/check-mysql-schema-drift.py --database-url "$DATABASE_URL"
```

4. 重点确认 `missing_columns.banners` 是否包含 `image_source`、`sku_gallery_asset_id`、`topic_id`、`brand_id`、`valid_from`、`valid_to`、`remark` 等字段。
5. 分别验证品牌类型 Banner 新增、编辑、品牌 Logo、自定义上传图、非品牌类型 Banner 保存是否正常。

# 回归关注点

- 品牌类型 Banner 新增保存成功。
- 品牌类型 Banner 编辑保存成功。
- `brand_logo` 和 `custom_upload` 两种图片来源均可按规则保存。
- 品牌不存在、品牌未启用、品牌无 Logo、Logo 引用不一致、标题重复等失败场景返回明确 4xx 错误码，不返回裸 500。
- 保存成功后管理端列表、详情、上线/下线操作和小程序对应展示入口读取到同一配置。
- 修复需验证生产 MySQL `banners` 表与 `schema.mysql.sql` 无阻塞 drift。
