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

New Services and Routers introduced in OpenSpec Changes MUST include corresponding automated tests before archive. Changes that modify existing Services, Routers, API schemas, user-facing UI, workflow automation, or governance scripts MUST include focused regression tests for the modified behavior. For password-policy feedback changes, tests MUST cover both backend policy failure detail and frontend user-facing error rendering.

#### Scenario: 治理文档声明测试要求

- **WHEN** a developer reads `docs/standards/testing-governance.md`
- **THEN** MUST find a rule that OpenSpec Change implementations MUST add matching tests
- **AND** MUST NOT allow implementation-only changes without test coverage for new Services or Routers

#### Scenario: 修改密码策略失败详情已测试

- **WHEN** backend tests run for this change
- **THEN** tests MUST assert password change policy failures expose distinguishable failure details for length, uppercase, lowercase, digit, and special-character requirements
- **AND** tests MUST assert failures do not update `password_hash`
- **AND** tests MUST assert responses do not include plaintext passwords

#### Scenario: 修改密码弹窗具体错误提示已测试

- **WHEN** frontend tests run for this change
- **THEN** tests MUST assert policy failure details render as concrete user-facing messages
- **AND** tests MUST assert new-password policy failures are not displayed under the old-password field
- **AND** tests MUST assert old-password, weak-password, same-as-old, protected-account, and success paths do not regress

#### Scenario: Orval 与 API 契约已检查

- **WHEN** this change modifies OpenAPI response schemas
- **THEN** generated client types MUST include the password policy failure detail shape
- **AND** generated files MUST NOT be hand-edited

#### Scenario: workflow-sync 归档时间漂移已测试

- **WHEN** a Change modifies workflow-sync archived Change timestamp derivation
- **THEN** regression tests MUST cover an archived Change whose related issue or change trace frontmatter `updated_at` is newer than the stable archive fact
- **AND** the rendered archive timestamp MUST come from lifecycle, archive records, or archive directory date rather than mutable `updated_at`

#### Scenario: workflow-sync Markdown 持久化幂等已测试

- **WHEN** a Change modifies workflow-sync Markdown persistence behavior
- **THEN** regression tests MUST cover a Markdown document whose rendered content is identical to the current file
- **AND** persistence MUST NOT rewrite the file or refresh frontmatter `updated_at`
- **AND** consecutive `python scripts/sync-workflow-status.py --check` runs MUST remain no delta after a normal sync.

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

The BUG-0051 fix and REQ-0023 enhancement SHALL include focused regression coverage for the admin API docs Swagger entry, row-level Swagger operation links, and Web proxy behavior.

#### Scenario: 前端链接行为已测试

- **WHEN** frontend tests run for `ApiDocsPage`
- **THEN** they SHALL verify the non-production Swagger action uses the expected same-origin Swagger path
- **AND** they SHALL verify the production read-only Swagger action still uses the expected same-origin Swagger path.

#### Scenario: Row-level operationId link tested

- **WHEN** frontend tests render an API docs route with `included_in_openapi=true` and a non-empty `operation_id`
- **THEN** they SHALL verify the row-level `查看` action links to a same-origin Swagger UI operationId deep link such as `/docs#/{tag}/{operationId}`
- **AND** they SHALL verify the PATH cell can use the same deep link when it is available
- **AND** they SHALL verify tag and operationId values are URL-safe encoded where needed.

#### Scenario: Row-level disabled state tested

- **WHEN** frontend tests render a route with `included_in_openapi=false` or a missing `operation_id`
- **THEN** they SHALL verify the row-level `查看` action is disabled or equivalently unavailable
- **AND** they SHALL verify the disabled state has no clickable href to `/docs` or an incorrect operationId.
- **AND** they SHALL verify the PATH cell does not expose a clickable Swagger detail href for unavailable routes.

#### Scenario: Row-level Swagger link security tested

- **WHEN** frontend tests inspect row-level Swagger links
- **THEN** they SHALL verify enabled links open in a new tab or window with a safe rel attribute such as `noreferrer`
- **AND** they SHALL verify the href and rendered text do not contain token, Bearer, Cookie, user, password, database, MinIO, or environment-secret content.

#### Scenario: 既有接口文档回归保持覆盖

- **WHEN** frontend tests are updated for REQ-0023
- **THEN** existing admin permission, employee forbidden, OpenAPI JSON, Swagger read-only policy, Orval method name, missing method state, route filtering, pagination, and API docs summary metric assertions SHALL continue to pass.
- **AND** they SHALL verify the pagination summary count updates to the filtered route count after filters change.

#### Scenario: 固定操作列已测试

- **WHEN** frontend tests render the API docs table
- **THEN** they SHALL verify the ACTION header and row action cells expose the sticky action-column class or equivalent stable selector.

#### Scenario: Web 代理 smoke 验证 docs 路由

- **WHEN** proxy smoke verification is performed for the Web port
- **THEN** `/docs` SHALL return backend Swagger HTML or an equivalent backend docs response
- **AND** it SHALL NOT return the Web SPA homepage.

#### Scenario: OpenAPI JSON smoke 验证无 fallback

- **WHEN** proxy smoke verification requests `/openapi.json` through the Web port
- **THEN** the response SHALL include OpenAPI JSON fields such as `openapi`, `info`, and `paths`
- **AND** it SHALL NOT return Web SPA HTML.

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
The testing capability SHALL verify that production does not allow Swagger `Try It Out` from the admin API docs page.

#### Scenario: Production disables Try It Out
- **WHEN** the app is configured as production
- **THEN** automated or documented production-equivalent verification SHALL prove Swagger `Try It Out` is hidden or disabled.

#### Scenario: Non-production allows Try It Out
- **WHEN** the app is configured as local, development, or demo
- **THEN** tests or documented verification SHALL prove the Swagger debugging policy is shown as allowed.

### Requirement: Orval and OpenAPI regression
The testing capability SHALL include OpenAPI/Orval regression checks when the change adds or changes backend API contracts.

#### Scenario: Orval generated output updated
- **WHEN** a backend aggregation endpoint or API contract changes
- **THEN** the OpenAPI export and Orval generated client SHALL be regenerated and reviewed.

#### Scenario: API governance validation
- **WHEN** a backend endpoint is added for admin API docs
- **THEN** API governance validation SHALL pass or known unrelated failures SHALL be documented.

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

