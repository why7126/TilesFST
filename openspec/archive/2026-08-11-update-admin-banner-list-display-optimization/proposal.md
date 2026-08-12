# 提案：优化管理端 Banner 列表显示内容

## 背景

REQ-0108 已评审并纳入 `sprint-022`。当前 Banner 管理列表仍在 Banner 列中展示内部识别/标题等非运营核心信息，而跳转目标主要以类型和对象 ID 形式存在。运营需要更快地通过主图和可读跳转对象判断 Banner 配置。

## 变更目标

- Banner 列只显示主图或缩略图，不再显示标题、内部识别或其他文本。
- 保留展示位置、展示端、跳转类型、状态、有效期、排序、更新时间和操作列。
- 新增独立“跳转对象”列，按跳转类型显示品牌名称、SKU 名称、专题名称、外部链接地址或 `-`。
- 管理端 Banner 列表 API 新增只读展示字段，例如 `jump_target_label`，前端不按行额外请求对象详情。
- 同步 Pydantic Schema、OpenAPI、Orval、接口文档和测试。

## 非目标

- 不修改 Banner 新增/编辑表单字段、保存流程或跳转校验规则。
- 不修改小程序前台 Banner 展示。
- 不新增跳转类型。
- 不展示 SKU 编码。
- 不删除数据库或 API 中既有 `title` 字段。
- 不改变数据库表结构、MinIO、上传链路、Docker 或 Nginx 配置。

## 影响范围

```yaml
impact:
  backend: true
  web: true
  miniapp: false
  admin: true
  database: false
  storage: false
  api: true
capabilities:
  new: []
  modified:
    - banner-management
    - web-client
```

## 风险

- 后端查询需关联品牌、SKU、专题表，需避免列表 N+1 查询。
- 新增列可能挤压操作列，需保持 sticky action cell 和横向滚动可用。
- 关联对象不存在、禁用或名称为空时需有稳定兜底文案。
- API 响应字段变化必须同步 OpenAPI/Orval，避免前端类型漂移。
