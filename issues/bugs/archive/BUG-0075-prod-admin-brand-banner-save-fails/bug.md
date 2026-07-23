---
bug_id: BUG-0075-prod-admin-brand-banner-save-fails
title: 生产环境管理端品牌类型 Banner 配置无法保存
severity: high
status: done
owner:
discovered_at: 2026-07-21 10:17:39
environment: 生产环境 Web 管理端
related_requirement: REQ-0062-admin-banner-placement-scope
related_change: fix-prod-admin-brand-banner-save
created_at: 2026-07-21 15:00:10
updated_at: 2026-07-22 08:59:18
---

# 现象

生产环境 Web 管理端中，配置品牌类型 Banner 后无法保存。

该问题发生在已有 Banner 管理与品牌类型投放能力下。当前缺少生产环境保存接口响应体、错误码和后端日志，尚不能确认失败是前端表单校验、后端业务校验、生产 MySQL 表结构漂移、品牌数据异常，还是前后端版本不一致导致。

# 复现步骤

1. 登录生产环境 Web 管理端。
2. 进入 Banner 管理页面。
3. 新建或编辑一条 Banner。
4. 将跳转类型配置为品牌详情或品牌类型。
5. 选择一个已启用品牌。
6. 配置 Banner 图片：使用品牌 Logo 或自定义上传运营图。
7. 填写标题、展示位置、排序、有效期和备注等字段。
8. 点击保存 Banner。
9. 观察页面错误提示、Network 响应和后端日志。

# 期望结果

- 合法的品牌类型 Banner 可以创建或编辑保存成功。
- 保存后 `jump_type`、`brand_id`、`image_source`、`image_object_key` 等字段正确持久化。
- 保存成功的 Banner 能在管理端列表和详情中回显，并可按状态与有效期继续上线/下线。
- 如果配置不合法，系统应返回明确错误码和可理解提示，例如品牌不存在、品牌未启用、品牌无 Logo、图片来源不匹配或标题重复。

# 实际结果

生产环境配置品牌类型 Banner 后无法保存。当前尚未取得保存请求的 HTTP 状态码、响应 JSON、错误码、请求 payload 和后端日志。

本地后端新库路径已存在品牌类型 Banner API 测试覆盖，并可通过创建用例；因此生产失败更倾向于生产环境差异、生产数据差异或生产库结构漂移。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 | 运营人员无法维护品牌类型 Banner，影响品牌运营位配置 |
| Banner 管理 | 品牌详情跳转、品牌列表页轮播或首页轮播中的品牌投放能力不可用 |
| 小程序展示端 | 依赖品牌类型 Banner 的入口可能无法上线或无法更新 |
| 品牌主页流量 | 品牌 Banner 无法保存会影响品牌详情页/主页导流 |
| 生产发布质量 | 若根因是生产 MySQL schema drift，可能暴露发布前数据库兼容性校验不足 |

# 严重等级说明

严重等级：`high`。

理由：问题发生在生产环境，且直接阻断品牌类型 Banner 的保存闭环。Banner 是运营展示和品牌导流入口，保存失败会影响线上内容配置与投放更新；若根因是生产数据库结构或版本差异，还可能影响后续 Banner 编辑、上线和回归验证。

# 初步分析

本地代码链路显示品牌类型 Banner 保存需要满足以下条件：

- 前端提交 `jump_type: BRAND_DETAIL`、`brand_id`、`image_source`、`image_object_key` 等字段。
- 后端要求品牌存在且状态为 `ENABLED`。
- 当 `image_source` 为 `brand_logo` 时，提交的 `image_object_key` 必须与该品牌 `logo_object_key` 一致。
- 后端持久化会写入 `banners.brand_id`。

结合 `/bug-explore` 结果，优先怀疑生产 MySQL `banners` 表结构与当前 `schema.mysql.sql` 不一致，尤其是缺少 `brand_id` 字段或相关约束未同步。MySQL 初始化当前使用 `CREATE TABLE IF NOT EXISTS`，不会自动对既有生产表执行 `ALTER`，如果生产库在品牌类型 Banner 能力上线前已创建 `banners` 表，保存品牌类型 Banner 时可能在写入 `brand_id` 环节失败。

次要可能原因：

- 所选品牌在生产环境不是 `ENABLED` 状态。
- 所选品牌没有 `logo_object_key`，但前端或用户选择了使用品牌 Logo。
- 前端提交的 `image_object_key` 与生产数据库中的品牌 Logo key 不一致。
- 生产前端与后端版本不一致，导致枚举值或 payload 字段不匹配。
- 标题在同一展示端与展示位置下重复，触发唯一性校验。

# 待补充信息

| 信息 | 说明 |
|---|---|
| Network 响应 | 保存接口 URL、HTTP 状态码、响应 JSON、错误码和请求 payload |
| 后端日志 | FastAPI/SQLAlchemy/MySQL 错误堆栈，重点看 `brand_id`、约束、外键和 30052 业务错误 |
| 生产表结构 | `banners` 表是否包含 `brand_id`、`sku_gallery_asset_id`、`image_source`、`jump_type` 约束和外键 |
| 品牌数据 | 所选品牌是否 `ENABLED`，是否有 `logo_object_key`，Logo key 是否可读 |
| 前后端版本 | 当前生产 Web bundle 与后端镜像是否来自同一发布版本 |

# 回归关注点

- 品牌类型 Banner 新增保存成功。
- 品牌类型 Banner 编辑保存成功。
- 使用品牌 Logo 与自定义上传两种图片来源均按规则保存。
- 品牌未启用、品牌无 Logo、Logo 引用不一致、标题重复等错误场景返回明确提示。
- 保存成功后管理端列表、详情、小程序对应展示入口读取到同一配置。
