## MODIFIED Requirements

### Requirement: 产品版本常量与 Web 端展示

Web 客户端 MUST 在 `src/shared/` 维护单一产品版本常量（如 `PRODUCT_VERSION = 'v0.0.1'`），管理端与店主端 MUST 引用同一导出。产品版本 MUST 由发版时人工更新该常量；MUST NOT 从 `package.json`、`pyproject.toml`、FastAPI `version`、OpenAPI 版本、CI/Git 构建信息或其他自动版本源读取。Web 客户端 MUST NOT 在登录页、页脚或关于页展示产品版本（本期 Out）。Web 客户端 MUST NOT 展示 API / OpenAPI / 后端版本号作为产品版本。产品发布流程 MUST 校验 `src/shared/product-version.ts` 中的 `PRODUCT_VERSION` 与产品版本发布对象和公开发布公告版本一致；若一次发布不改变 `PRODUCT_VERSION`，发布材料 MUST 记录原因。

#### Scenario: 单一事实源

- **WHEN** 开发者查看产品版本定义
- **THEN** MUST 存在且仅存在一处 `src/shared/` 产品版本常量导出
- **AND** 管理端 `AdminSidebar` 与店主端 `Sidebar` MUST import 同一常量

#### Scenario: 禁止自动版本源

- **WHEN** 实现读取展示用版本号
- **THEN** MUST NOT 使用 npm package version、FastAPI app version、OpenAPI version、git sha 或 CI build number 作为 `PRODUCT_VERSION` 展示值

#### Scenario: 发布版本一致性校验

- **WHEN** 产品发布流程准备或确认公开发布公告
- **THEN** MUST compare the release version against `src/shared/product-version.ts` `PRODUCT_VERSION`
- **AND** MUST block release confirmation or record an explicit no-version-change rationale when the values do not match
