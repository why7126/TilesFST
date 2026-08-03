# 测试治理规范

## Purpose
定义后端 pytest、前端 Vitest、测试目录结构、变更测试映射、CI 工作流和回归校验要求，确保每个 OpenSpec Change 有可追踪的质量门禁。
## Requirements
### Requirement: Pytest 基线

Backend tests MUST be runnable from repository root via `./scripts/run-tests.sh` with shared configuration in `pytest.ini` and `tests/conftest.py`.

#### Scenario: 从仓库根目录运行测试

- **WHEN** a developer runs `./scripts/run-tests.sh` from the repository root
- **THEN** pytest MUST execute backend unit and integration tests
- **AND** MUST exit with code 0 on the repository baseline

#### Scenario: Pytest 配置存在

- **WHEN** a developer inspects repository test configuration
- **THEN** MUST find `pytest.ini` at repository root
- **AND** MUST find `tests/conftest.py` for shared fixtures

### Requirement: 测试目录结构

The repository MUST maintain a test pyramid with dedicated directories for unit, integration, and end-to-end tests documented in `docs/standards/testing-governance.md`.

#### Scenario: 核心测试目录存在

- **WHEN** a developer lists `tests/`
- **THEN** MUST find `tests/unit/`, `tests/integration/`, and `tests/e2e/`
- **AND** `tests/unit/` and `tests/integration/` MUST contain at least one `test_*.py` file each

#### Scenario: 后端模块测试保留

- **WHEN** a developer lists `src/backend/tests/`
- **THEN** MUST find at least one `test_*.py` for backend module-level tests

### Requirement: 测试映射

Each REQ-0000 infrastructure requirement MUST map to at least one automated test or validation script in `openspec/testing-mapping.md`.

#### Scenario: Sprint-000 mappings registered

- **WHEN** a developer reads `openspec/testing-mapping.md`
- **THEN** MUST find entries for `REQ-0000-build-design-system`, `REQ-0000-build-api-standard`, and `REQ-0000-build-test-standard`
- **AND** each entry MUST list at least one test path or validation script

### Requirement: Change 测试
New Services and Routers introduced in OpenSpec Changes MUST include corresponding automated tests before archive. Changes that modify existing Services, Routers, API schemas, user-facing UI, workflow automation, governance scripts, form validation contracts, workflow snapshot contracts, archive path contracts, or generated backend-owned fields MUST include focused regression tests for the modified behavior. Shared test fixtures and helpers MUST be updated in the same change when request payloads, validation rules, generated fields, archive path roots, or snapshot schemas change.

#### Scenario: 测试夹具跟随契约变更
- **WHEN** an API, form validation, generated-field, workflow snapshot, archive path, or release-governance contract changes
- **THEN** shared pytest/Vitest fixtures and helper payloads MUST be updated to use the current minimum valid contract
- **AND** tests MUST NOT keep submitting deprecated client-writable fields that are now backend-generated
- **AND** tests MUST cover the new fixture, path, or snapshot fields required by validators.

#### Scenario: OpenSpec Change 文件读取兼容归档路径
- **WHEN** automated tests need to read implementation evidence or task files from an OpenSpec Change
- **THEN** tests MUST resolve the file from `openspec/changes/<change-id>/...`, `openspec/archive/*-<change-id>/...`, or legacy `openspec/changes/archive/*-<change-id>/...`
- **AND** tests SHOULD prefer active path first, canonical archive path second, and legacy archive path only as compatibility fallback
- **AND** tests SHOULD reuse a shared resolver helper rather than hard-coding only the active Change path.

#### Scenario: 测试阻止 legacy archive 新写入
- **WHEN** workflow scripts, archive commands, release generation, Fact Sheet, AI usage, or readiness reports create or update Change archive facts
- **THEN** focused regression tests MUST assert generated paths use `openspec/archive/`
- **AND** tests MUST fail if newly generated facts use `openspec/changes/archive/` as the canonical archive path.

### Requirement: 测试框架校验脚本

The project MUST provide `scripts/validate-test-framework.py` to verify pytest configuration, governance documents, and baseline test directories exist.

#### Scenario: 基线校验通过

- **WHEN** `python scripts/validate-test-framework.py` runs on the repository baseline
- **THEN** it MUST exit with code 0
- **AND** MUST report that test framework validation passed

#### Scenario: 必需治理文档已检查

- **WHEN** the validation script runs
- **THEN** it MUST verify presence of `docs/standards/testing-governance.md`, `docs/standards/unit-test-standard.md`, `docs/standards/frontend-test-standard.md`, and `.coveragerc`

### Requirement: CI 测试工作流

The repository MUST include a GitHub Actions workflow that runs pytest and test framework validation on push and pull request.

#### Scenario: CI 中运行后端测试

- **WHEN** a pull request targets `main` or `master`
- **THEN** `.github/workflows/test.yml` MUST run backend pytest
- **AND** MUST run `python scripts/validate-test-framework.py`

### Requirement: 生产 MySQL 路径必须有集成验证

项目 MUST 提供至少一种 MySQL 集成验证路径，用于验证 MySQL schema 初始化、默认管理员 seed 和至少一条读写 API。该验证 MAY 作为 CI MySQL 8 service container job，也 MAY 作为 `@pytest.mark.mysql` optional pytest 与 documented manual smoke 组合。默认 SQLite pytest MUST 保持可从本地运行，不要求开发者本机安装 MySQL。

#### Scenario: MySQL 集成验证覆盖启动关键路径

- **WHEN** MySQL 集成验证运行
- **THEN** MUST 覆盖 MySQL schema 初始化
- **AND** MUST 覆盖默认管理员 seed
- **AND** MUST 覆盖至少一条 API 读写路径，如登录或 health + 简单 CRUD

#### Scenario: SQLite 默认 pytest 仍可运行

- **WHEN** 开发者在未安装 MySQL 的本地环境运行默认 pytest
- **THEN** 测试 MUST 使用 SQLite 默认路径
- **AND** MUST NOT 因缺少 MySQL 服务而失败

### Requirement: Swagger 入口回归测试

The BUG-0051 fix and REQ-0023 enhancement SHALL include focused regression coverage for the admin API docs Swagger entry, row-level Swagger operation links, and Web proxy behavior. Future API docs refinements, Swagger entry changes, and Web proxy changes MUST include automated tests or documented smoke verification for the Swagger Web proxy and production `Try It Out` checklist.

#### Scenario: Swagger main entry uses same-origin path

- **WHEN** frontend tests render the admin API docs page in non-production and production configurations
- **THEN** they SHALL verify the non-production Swagger action uses the expected same-origin Swagger path
- **AND** they SHALL verify the production read-only Swagger action still uses the expected same-origin Swagger path.

#### Scenario: Row-level Swagger operation link is generated

- **WHEN** frontend tests render an API docs route with `included_in_openapi=true` and a non-empty `operation_id`
- **THEN** they SHALL verify the row-level `查看` action links to a same-origin Swagger UI operationId deep link such as `/docs#/{tag}/{operationId}`
- **AND** they SHALL verify the PATH cell link, if present, uses the same safe deep link.

#### Scenario: Unavailable Swagger operation links stay disabled

- **WHEN** frontend tests render a route with `included_in_openapi=false` or a missing `operation_id`
- **THEN** they SHALL verify the row-level Swagger action is disabled or equivalently unavailable
- **AND** they SHALL verify the disabled state has no clickable href to `/docs` or an incorrect operationId.
- **AND** they SHALL verify the PATH cell does not expose a clickable Swagger detail href for unavailable routes.

#### Scenario: Row-level Swagger link security tested

- **WHEN** frontend tests inspect row-level Swagger links
- **THEN** they SHALL verify the link does not contain bearer tokens, session data, database DSNs, MinIO credentials, JWT secrets, or real environment variable values.

#### Scenario: Existing API docs regression remains covered

- **WHEN** API docs frontend regressions are updated
- **THEN** existing admin permission, employee forbidden, OpenAPI JSON, Swagger read-only policy, Orval method name, missing method state, route filtering, pagination, and API docs summary metric assertions SHALL continue to pass.

#### Scenario: Web 代理 smoke 验证 docs 路由

- **WHEN** proxy smoke verification requests `/docs` through the Web port
- **THEN** `/docs` SHALL return backend Swagger HTML or an equivalent backend docs response
- **AND** it SHALL NOT return the Web app homepage or React Router fallback shell.

#### Scenario: OpenAPI JSON smoke 验证无 fallback

- **WHEN** proxy smoke verification requests `/openapi.json` through the Web port
- **THEN** the response SHALL include OpenAPI JSON fields such as `openapi`, `info`, and `paths`
- **AND** it SHALL NOT return the Web app homepage or static HTML shell.

#### Scenario: Swagger checklist verification is recorded

- **WHEN** a future change modifies API docs refine behavior, Swagger entry behavior, or Web proxy configuration
- **THEN** its tasks, trace, acceptance report, or test output MUST record verification for local Web proxy, Docker Web proxy, and production-equivalent `Try It Out` policy
- **AND** if an item cannot be automated, the record MUST name the manual smoke method and environment.

### Requirement: 管理端接口文档摘要指标卡回归测试

The testing capability SHALL include focused frontend regression tests for `/admin/api-docs` summary metric card structure.

#### Scenario: 摘要指标卡 class 结构已测试

- **WHEN** frontend tests render `ApiDocsPage`
- **THEN** they SHALL verify the summary metric section contains metric value and description elements using `metric-value` and `metric-desc`
- **AND** the test SHOULD fail if the implementation regresses to summary cards that only expose bare `strong` and `span` styling hooks.

#### Scenario: 既有接口文档行为测试保留

- **WHEN** frontend tests are updated for this fix
- **THEN** existing assertions for Orval method display, the "未生成" state, route filtering, and production Swagger read-only behavior SHALL continue to pass.

#### Scenario: 无需后端或 Orval 回归

- **WHEN** this change is implemented without API contract changes
- **THEN** no backend aggregation endpoint tests or Orval regeneration SHALL be required for this fix.

### Requirement: 接口文档列表分页回归测试
The testing capability SHALL include focused frontend regression coverage for BUG-0053 on `/admin/api-docs`.

#### Scenario: 冗余标题已覆盖
- **WHEN** frontend tests render `/admin/api-docs`
- **THEN** they SHALL assert the route directory list does not render the redundant `系统接口` title.

#### Scenario: 分页 DOM 已覆盖
- **WHEN** frontend tests render enough API docs routes to paginate
- **THEN** they SHALL assert `page-summary`, `page-right`, page buttons, and page-size selector elements are present.

#### Scenario: 每页条数选项已覆盖
- **WHEN** frontend tests inspect the page-size selector
- **THEN** they SHALL verify the 10, 20, 50, and 100 options
- **AND** they SHOULD verify the default page size is 20.

#### Scenario: 页码切换已覆盖
- **WHEN** frontend tests switch route directory pages
- **THEN** they SHALL verify the table displays only the current page routes.

#### Scenario: 筛选重置页码
- **WHEN** frontend tests change Method, Tag, Auth, or keyword filters after navigating away from page 1
- **THEN** they SHALL verify the current page returns to page 1.

#### Scenario: 既有 API docs 回归保持覆盖
- **WHEN** BUG-0053 frontend tests are updated
- **THEN** existing admin permission, employee forbidden, OpenAPI JSON, Swagger read-only policy, Orval method name, missing method state, and route filtering assertions SHALL continue to pass.

### Requirement: 管理端内容区域布局回归测试

The testing capability SHALL include focused frontend regression coverage for BUG-0054 on the Web admin shell content padding and width strategy.

#### Scenario: Admin shell legacy padding is covered
- **WHEN** frontend tests or static style assertions inspect `admin-home.css`
- **THEN** they SHALL verify `.main-content` no longer uses the legacy `48px 56px 72px` desktop padding.

#### Scenario: Content-inner max width is covered
- **WHEN** frontend tests or static style assertions inspect admin shell styles
- **THEN** they SHALL verify `.content-inner` no longer uses `max-width: 1080px`
- **AND** they SHALL verify the chosen global strategy is `max-width: 100%` or `max-width: min(1440px, 100%)`.

#### Scenario: Page-level divergent width is covered
- **WHEN** frontend tests or static style assertions inspect admin page CSS
- **THEN** they SHALL verify SKU management does not keep a `1120px` `content-inner` override
- **AND** they SHALL verify system settings does not lock the full page content wrapper to `1080px`.

#### Scenario: Sidebar collapse behavior remains covered
- **WHEN** BUG-0054 tests are added or updated
- **THEN** existing `AdminSidebar.collapse.test.tsx` and `AdminLayout.test.tsx` assertions SHALL continue to pass
- **AND** sidebar width, collapsed state, and localStorage behavior SHALL not regress.

#### Scenario: Visual baseline pages are listed for manual validation
- **WHEN** implementation records validation results
- **THEN** it SHALL include `/admin/logs`, `/admin/tile-skus`, `/admin/users`, `/admin/dashboard`, and `/admin/settings`
- **AND** it SHOULD include 1440px, 1920px, collapsed, tablet, and mobile-smoke viewports.

### Requirement: 管理端接口文档后端测试
The testing capability SHALL include backend tests for any admin API docs aggregation endpoint introduced by this change.

#### Scenario: Admin can fetch route inventory
- **WHEN** the change introduces a backend route inventory endpoint
- **THEN** pytest SHALL verify an authenticated `admin` can fetch the inventory successfully.

#### Scenario: Employee cannot fetch route inventory
- **WHEN** the change introduces a backend route inventory endpoint
- **THEN** pytest SHALL verify an authenticated `employee` receives 403.

#### Scenario: Non-api routes are included
- **WHEN** the change introduces a backend route inventory endpoint
- **THEN** pytest SHALL verify `/health` and `/media/{object_key:path}` are represented in the inventory.

### Requirement: 管理端接口文档前端测试
The testing capability SHALL include frontend tests for `/admin/api-docs` navigation, permissions, filtering, and Orval display.

#### Scenario: Admin navigation visible
- **WHEN** frontend tests render admin navigation for an `admin` user
- **THEN** they SHALL assert the "接口文档" menu item is visible below "系统设置".

#### Scenario: Employee navigation hidden
- **WHEN** frontend tests render admin navigation for an `employee` user
- **THEN** they SHALL assert the "接口文档" menu item is not visible.

#### Scenario: Route page behavior
- **WHEN** frontend tests render the API docs page
- **THEN** they SHALL cover filtering and Orval method-name display, including the "未生成" state.

### Requirement: 生产 Swagger 调试禁用验证

The testing capability SHALL verify that production does not allow Swagger `Try It Out` from the admin API docs page. Future API docs and Swagger proxy changes MUST preserve this production read-only verification gate.

#### Scenario: Production disables Try It Out

- **WHEN** production or production-equivalent Swagger documentation is verified
- **THEN** automated or documented production-equivalent verification SHALL prove Swagger `Try It Out` is hidden or disabled.

#### Scenario: Non-production allows Try It Out

- **WHEN** non-production API docs behavior is verified
- **THEN** tests or documented verification SHALL prove the Swagger debugging policy is shown as allowed.

#### Scenario: Production read-only gate remains part of API docs checklist

- **WHEN** a future API docs refine, Swagger route, or Web proxy change is implemented
- **THEN** its acceptance or trace records MUST explicitly state that production `Try It Out` remains disabled, hidden, or read-only
- **AND** the records MUST NOT rely on frontend copy alone as the only enforcement mechanism.

### Requirement: Orval and OpenAPI regression

The testing capability SHALL include OpenAPI/Orval regression checks when the change adds or changes backend API contracts. Management admin form validation error contract changes SHALL include checks that exported OpenAPI and generated Orval output represent the unified validation error envelope and do not depend only on default `HTTPValidationError.detail`.

#### Scenario: Orval generated output updated

- **WHEN** API response contracts change
- **THEN** the OpenAPI export and Orval generated client SHALL be regenerated and reviewed.

#### Scenario: 管理端表单校验错误类型已检查

- **WHEN** API validation envelope governance is implemented
- **THEN** generated OpenAPI / Orval output SHALL expose or tolerate the unified validation error envelope for representative management admin form APIs
- **AND** review records SHALL confirm default `HTTPValidationError.detail` is not the only validation error type source.

### Requirement: 管理端列表页一致性回归测试

The testing capability SHALL include focused frontend regression coverage for BUG-0055 on Web admin list page layout order, filter/search behavior, sticky action columns, and pagination window behavior.

#### Scenario: Module order is covered

- **WHEN** frontend tests render affected Web admin list pages
- **THEN** they SHALL verify the DOM order is title module, metrics module, filter/search module, then list module
- **AND** they SHALL cover SKU, brand, category, spec, banner, user, log audit, and API docs pages where practical.

#### Scenario: Query buttons are removed

- **WHEN** frontend tests render affected filter/search modules
- **THEN** they SHALL verify no visible button named 「查询」 or 「搜索」 is rendered
- **AND** they SHALL verify a reset button remains available.

#### Scenario: Pagination window is covered

- **WHEN** frontend tests exercise pagination helpers or page components
- **THEN** they SHALL verify at most 5 clickable page number buttons are rendered
- **AND** they SHALL cover total page counts of 1, 5, and 6 or more
- **AND** they SHALL verify page size changes reset current page to 1.

#### Scenario: Filter reset behavior is covered

- **WHEN** frontend tests update filters or click reset
- **THEN** they SHALL verify current page returns to 1
- **AND** list result calculation or request parameters SHALL reflect the changed filters.

#### Scenario: Sticky action column contract is covered

- **WHEN** frontend tests render affected admin tables
- **THEN** they SHALL verify the last header and body cells use the sticky action column contract
- **AND** they SHALL verify existing action disabled states and confirmation flows remain test-covered where already present.

### Requirement: Sprint Archive Tasks Gate

The workflow tooling MUST provide an executable Sprint archive readiness gate that blocks `/sprint-archive` before any archive or Sprint close mutation when a Sprint-scoped OpenSpec Change has incomplete tasks.

#### Scenario: Incomplete active change blocks archive

- **WHEN** a Sprint references an active OpenSpec Change whose `tasks.md` contains one or more `- [ ]` items
- **THEN** the Sprint archive readiness gate MUST return a non-zero exit code
- **AND** the report MUST identify the blocked change and incomplete task count.

#### Scenario: Incomplete archived change blocks Sprint close

- **WHEN** a Sprint references an already archived OpenSpec Change whose archived `tasks.md` contains one or more `- [ ]` items
- **THEN** the Sprint archive readiness gate MUST return a non-zero exit code
- **AND** the report MUST NOT skip the change only because it is already under `openspec/changes/archive/`.

#### Scenario: Completed Sprint changes pass

- **WHEN** every Sprint-scoped OpenSpec Change has a present `tasks.md` with all checklist items marked `- [x]`
- **THEN** the Sprint archive readiness gate MUST return exit code 0
- **AND** the report MUST declare a PASS verdict.

#### Scenario: Missing tasks file blocks archive

- **WHEN** a Sprint-scoped OpenSpec Change has no `tasks.md`
- **THEN** the Sprint archive readiness gate MUST return a non-zero exit code
- **AND** the report MUST identify the missing tasks file as a blocker.

### Requirement: 品牌详情 Banner 保存修复必须有回归测试

The BUG-0075 fix SHALL include focused regression coverage for admin brand-detail Banner save, production MySQL schema compatibility, and public display read consistency.

#### Scenario: Admin 品牌详情 Banner 保存回归

- **WHEN** backend tests run for this change
- **THEN** tests SHALL cover `POST /api/v1/admin/banners` with `jump_type=BRAND_DETAIL` and a valid enabled brand
- **AND** tests SHALL cover editing an existing brand-detail Banner
- **AND** tests SHALL assert `brand_id`, `jump_type`, `image_source`, and `image_object_key` are persisted and returned.

#### Scenario: 品牌详情 Banner 失败场景回归

- **WHEN** backend tests run for this change
- **THEN** tests SHALL cover invalid brand id, disabled brand, missing brand logo, logo object key mismatch, and duplicate title where applicable
- **AND** tests SHALL assert unified error envelope responses with stable business errors or equivalent clear validation messages
- **AND** tests SHALL assert responses do not expose raw SQL, database DSNs, MinIO credentials, or internal stack traces.

#### Scenario: MySQL schema drift 修复回归

- **WHEN** database compatibility tests or validation scripts run for this change
- **THEN** they SHALL verify an existing MySQL `banners` table missing `brand_id` can be detected and safely remediated or blocked before production API traffic
- **AND** repeated execution SHALL remain idempotent
- **AND** default SQLite pytest SHALL remain runnable without a local MySQL service.

#### Scenario: 展示读取一致性回归

- **WHEN** tests or smoke verification read saved online brand-detail Banner data
- **THEN** admin list/detail and miniapp carousel query paths SHALL observe the same saved configuration
- **AND** homepage carousel and brand-list carousel queries SHALL remain separated by `position`.

### Requirement: Sprint close stale scan 回归测试
测试治理 SHALL 要求 Sprint close stale scan、Workflow Sync 四件套刷新和旧归档路径残留检查具备聚焦自动化回归覆盖。

#### Scenario: stale 中间态文案触发测试失败
- **WHEN** pytest 使用 fixture 构造一个目标 Sprint 四件套，其中已创建或已归档 Change 仍显示待 `/req-opsx`、待 `/bug-opsx` 或待 `/opsx-apply`
- **THEN** stale scan 测试 MUST 断言命令返回非零退出码
- **AND** 断言报告包含命中文件、关联对象、真实状态和建议修复动作

#### Scenario: legacy archive path 真实残留触发测试失败
- **WHEN** pytest 使用 fixture 构造 Sprint 四件套或新生成报告引用 `openspec/changes/archive/` 作为 canonical archive path
- **THEN** stale scan 或 residual 测试 MUST 断言该引用被标记为 blocker
- **AND** 断言建议改用 `openspec/archive/`

#### Scenario: 允许的 legacy 例外不触发失败
- **WHEN** pytest fixture、兼容读取 helper 或迁移脚本中包含 `openspec/changes/archive/` legacy 字符串
- **THEN** 测试 MUST 断言 stale scan 将其归类为允许例外或忽略
- **AND** 该例外 MUST NOT 造成 Sprint close gate 失败

#### Scenario: Workflow Sync 刷新后 stale scan 通过
- **WHEN** Workflow Sync 根据 `sprint.yaml`、Issue trace 和 Change 状态刷新 `sprint.md` Scope 派生块
- **THEN** 测试 MUST 断言刷新后的四件套不再保留由机器事实可确定的过期规划文案
- **AND** 再次运行 stale scan MUST 返回 0

#### Scenario: 测试保持路径解析兼容
- **WHEN** 测试需要读取 Change tasks、trace 或归档证据
- **THEN** 测试 MUST 继续兼容 active path、canonical archive path 和 legacy archive fallback
- **AND** 新断言 MUST 区分“兼容读取 legacy”与“生成 canonical legacy 路径”两种语义

