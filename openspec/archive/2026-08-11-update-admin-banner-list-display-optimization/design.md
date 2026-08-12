# 设计：管理端 Banner 列表主图与跳转对象列

## 1. 需求来源

- REQ：`REQ-0108-admin-banner-list-display-optimization`
- Sprint：`sprint-022`
- 父能力：`REQ-0016-banner-management`
- 相关体验前提：`REQ-0106-admin-banner-title-hidden`
- 知识库引用：
  - `docs/knowledge-base/best-practices/admin-list-page-consistency.md`
  - `docs/knowledge-base/retrospectives/sprint-020-retrospective.md`

## 2. 方案概述

采用“后端一次性计算展示字段 + 前端表格直接渲染”的方案。

后端 Banner 列表项新增只读字段 `jump_target_label`。服务端根据 `jump_type` 和关联目标生成展示文案：

| jump_type | jump_target_label |
|---|---|
| `BRAND_DETAIL` | 品牌名称 |
| `SKU_DETAIL` | SKU 名称 |
| `TOPIC_PAGE` | 专题名称 |
| `EXTERNAL_LINK` | 外部链接地址 |
| `NO_JUMP` | `-` |

前端 `/admin/banners` 表格新增“跳转对象”列；Banner 列仅保留 `FallbackListImage` 或等价图片展示，不再渲染内部标题、内部识别或其他文字。

## 3. 后端与 API 设计

### 3.1 Schema

`BannerAdminItem` 增加：

```python
jump_target_label: str | None = None
```

该字段仅用于响应展示，不进入 `BannerCreateRequest` 或 `BannerUpdateRequest`。

### 3.2 查询策略

优先在 Banner 列表查询中通过 `LEFT JOIN` 或等价批量查询带出名称，避免前端按行请求对象详情：

- `brands.name` 用于 `BRAND_DETAIL`
- `tiles.name` 用于 `SKU_DETAIL`
- `topics.title` 用于 `TOPIC_PAGE`
- `banners.external_url` 用于 `EXTERNAL_LINK`
- `NO_JUMP` 返回 `-`

对象不存在、不可用或名称为空时，最终展示值应稳定为 `-` 或“对象不可用”。实现阶段推荐先采用 `-`，避免暴露内部 ID。

### 3.3 API 与 Orval

该变更修改管理端 Banner 列表响应结构，必须同步：

- Pydantic Schema
- OpenAPI 导出
- Orval generated client
- Web 前端类型引用
- 后端接口测试和前端列表测试

请求体、错误码、数据库 schema 不变。

## 4. Web 管理端 UI Contract

### 4.1 事实源优先级

```text
prototype/admin/context.md
→ acceptance.md
→ rules/ui-design.md
→ openspec/specs/banner-management/spec.md
→ openspec/specs/web-client/spec.md
```

本需求没有 HTML/PNG 高保真原型；`prototype/admin/context.md` 是字段布局合同。

### 4.2 页面与入口

- 页面：Web 管理后台 Banner 管理列表页
- 路由：`/admin/banners`
- 权限：沿用现有管理端权限，`admin` 与 `employee` 可访问，未授权角色不可访问

### 4.3 信息架构

保留现有页面结构：

```text
标题模块
→ 指标卡模块
→ 筛选/搜索模块
→ 表格列表模块
→ 分页
```

表格列目标：

| 列 | 策略 |
|---|---|
| Banner | 仅主图/缩略图 |
| 展示位置 | 保留 |
| 展示端 | 保留 |
| 跳转类型 | 保留 |
| 跳转对象 | 新增独立列 |
| 状态 / 有效期 / 排序 / 更新时间 / 操作 | 保留 |

### 4.4 视觉 token 与布局

- 继续使用现有管理端暗色旗舰风和 semantic token。
- 不新增裸 Hex。
- Banner 图片使用稳定尺寸，行高不得异常膨胀。
- 跳转对象长文本单行截断，外部链接不得撑宽表格。
- 除有效期列保留起止时间换行展示外，Banner 表格所有表头和其他字段均不得换行显示。
- 操作列保持 sticky action cell 可见、可点击。

### 4.5 交互状态

- loading、empty、error 状态沿用现有列表。
- 上线、下线、删除继续使用 DS confirm modal。
- 成功/失败反馈继续使用 fixed toast。
- 筛选变更和分页重置语义不回退。

### 4.6 图标与文案

- 新列标题使用“跳转对象”。
- `NO_JUMP` 展示 `-`。
- SKU 只显示 SKU 名称，不显示 SKU 编码。

### 4.7 Mock/API 边界

本 Change 接入真实管理端 Banner 列表 API，不使用 Mock 数据作为最终验收。测试可使用 fixture 构造 `jump_target_label`，但必须覆盖真实 API schema 与 Orval 类型同步。

### 4.8 一致性参照

- `docs/knowledge-base/best-practices/admin-list-page-consistency.md`
- `/admin/users` 分页 DOM 基准
- 现有 `/admin/banners` 表格、toast、confirm、fallback image 行为

## 5. 验证策略

- 后端 pytest 覆盖 `jump_target_label` 生成规则。
- Web Vitest 覆盖 Banner 列只显示图片、跳转对象列、长链接截断语义、表头/非有效期字段不换行契约、分页 DOM、confirm/toast 不回退。
- 运行 OpenAPI/Orval 生成。
- 运行 `python scripts/validate-openspec-language.py`。
