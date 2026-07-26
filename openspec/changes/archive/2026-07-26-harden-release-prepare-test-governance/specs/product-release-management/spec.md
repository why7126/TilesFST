## MODIFIED Requirements

### Requirement: 发布前校验门禁
发布流程 SHALL 在必填发布就绪检查通过前阻断发布确认；若某项不适用，必须明确标记不适用并说明理由。测试门禁失败时，发布准备流程 SHALL classify failures before reporting blockers so governance drift can be fixed at the right layer.

#### Scenario: 测试失败分类
- **WHEN** release preparation runs automated tests and any test fails
- **THEN** the release preparation output SHALL classify representative failures as archived path residual, fixture/schema drift, helper payload invalid, product regression, or environment blocker
- **AND** governance-drift failures SHALL include a concrete remediation such as updating shared test helpers, archived Change path resolution, or fixture schema
- **AND** the release object SHALL NOT mark the tests gate as pass until the focused regression and relevant suite pass.
