## ADDED Requirements

### Requirement: Web 主题切换与偏好持久化

The Web client MUST provide theme switching for `system`, `dark_flagship`, `comfort_dark`, and `light` on management-side and supported store-owner Web surfaces. The active mode MUST persist locally and, for authenticated users, synchronize with the account-level theme preference API. Switching themes MUST apply immediately without losing current page state.

#### Scenario: 登录前主题偏好

- **WHEN** an unauthenticated user changes theme on the login page
- **THEN** the selected mode SHALL persist locally
- **AND** the login page SHALL update immediately without requiring reload.

#### Scenario: 登录后账号偏好合并

- **WHEN** a user logs in successfully
- **THEN** the Web client SHALL load the account-level `theme_mode`
- **AND** the account-level value SHALL become authoritative when present
- **AND** the active local theme SHALL remain visually stable while synchronization completes.

#### Scenario: 主题切换失败可恢复

- **WHEN** an authenticated user changes theme and the backend persistence request fails
- **THEN** the Web client SHALL keep the local visual selection
- **AND** it SHALL show a recoverable error message using the existing toast or equivalent Design System feedback.

### Requirement: 管理端主题舒适度首批验收矩阵

The Web admin implementation MUST validate theme comfort across login, one list page, one form page/state, one modal, and `/design-system`, with tile SKU management as the representative business workflow.

#### Scenario: 登录页主题验收

- **WHEN** a user opens the admin login page in any supported theme mode
- **THEN** background, material composition, form controls, validation/error state, language controls, and theme switcher SHALL remain readable and visually comfortable
- **AND** the existing login page brand composition SHALL not regress.

#### Scenario: 瓷砖 SKU 列表主题验收

- **WHEN** a user opens `/admin/tile-skus` in any supported theme mode
- **THEN** page hero, metrics, filters, table, sticky action column, pagination, and fixed toast SHALL remain readable, aligned, and free of layout shift
- **AND** the page SHALL continue to reuse the established admin list template or equivalent Design System composition.

#### Scenario: 瓷砖 SKU 表单与弹窗主题验收

- **WHEN** a user opens a tile SKU create/edit form or modal in any supported theme mode
- **THEN** labels, inputs, validation errors, dirty state, modal width, modal scroll behavior, modal footer actions, and confirmation dialogs SHALL remain readable and usable
- **AND** the SKU media upload area SHALL show `idle`, `uploading`, `uploaded`, and `failed` states clearly.

### Requirement: 店主 Web 舒适主题边界

Store-owner Web pages outside brand display pages MUST support comfortable theme modes. Brand display pages MAY remain in `dark_flagship` when preserving the flagship brand expression is a product decision.

#### Scenario: 品牌展示页可保持暗色旗舰

- **WHEN** a store-owner Web brand display page is opened
- **THEN** the page MAY remain in `dark_flagship`
- **AND** this exception SHALL be documented in the page or route-level theme strategy.

#### Scenario: 非品牌展示页支持舒适主题

- **WHEN** a store-owner Web catalog, detail, or inquiry page is opened
- **THEN** it SHALL support the active comfortable theme mode
- **AND** it SHALL continue to use semantic tokens rather than page-local raw Hex values.
