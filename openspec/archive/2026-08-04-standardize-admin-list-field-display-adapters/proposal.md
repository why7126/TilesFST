## 背景

管理端品牌、证书、SKU、Banner 等列表页都依赖图片、名称和兜底字段帮助运营快速识别对象，但当前展示口径分散在各页面和局部 helper 中，容易出现无图态、加载失败态、空值文案、关联对象缺失和长名称截断不一致。

Sprint 018 复盘已将 “Admin display cell adapters” 标记为可复用抽象方向，本变更用于把 image / name / fallback adapter 检查表纳入 Design System 管理端列表治理契约，作为后续设计、实现、验收和回归的固定依据。

## 变更内容

- 在 `design-system` 能力中补充管理端列表字段展示 adapter 检查表要求。
- 明确检查表必须覆盖 `image adapter`、`name adapter`、`fallback adapter` 三类规则。
- 明确首批覆盖品牌列表、证书列表、SKU 列表和 Banner 列表。
- 明确检查表必须包含适用列表、检查项、期望表现、验证方式、强制/推荐/N/A 标记和现状盘点。
- 将 `admin-list` knowledge-base 横切 AC 纳入后续实现与验收门禁。
- 不直接修改业务源码，不新增 API、数据库字段、对象存储策略或上传链路。

## 能力

### 新增能力

- 无。

### 修改能力

- `design-system`：补充管理端列表字段展示 adapter 检查表与回归验收要求。

## 影响

```yaml
impact:
  backend: false
  web: true
  miniapp: false
  admin: true
  database: false
  storage: false
  api: false
capabilities:
  new: []
  modified:
    - design-system
```

本 Change 主要影响 OpenSpec 规范、Design System 文档/验收约束和后续管理端列表治理任务。若 `/opsx-apply` 阶段仅落检查表或设计系统文档，不需要 OpenAPI、Orval、数据库迁移或 Docker Compose 验证；若后续实现扩展到接口响应字段或 Schema，必须另行同步 API 契约与测试。
