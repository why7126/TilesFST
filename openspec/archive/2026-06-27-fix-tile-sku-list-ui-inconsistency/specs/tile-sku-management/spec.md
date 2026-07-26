## MODIFIED Requirements

### Requirement: SKU 管理视觉验收 Gate

SKU 管理页视觉对齐 MUST 通过 **HTML 原型**并排验收 gate。`prototype/images/*.png` 为可选 Golden Reference；有则纳入 sprint acceptance-report，无则不阻塞 archive。弹窗验收 MUST 包含矮视口下主体可滚动与头尾固定可见。列表页验收 MUST 包含分页 DOM 与用户管理页一致及表格卡片内无重复标题行。

#### Scenario: 列表页并排验收

- **WHEN** 团队在 1440×1024 视口并排对比 `/admin/tile-skus` 与 `tile-sku-management-list.html`
- **THEN** diff checklist（Shell、Sidebar active、4 指标卡、五维筛选、表格列、素材 badge、分页）MUST 全部 pass
- **AND** 分页左侧 MUST 为「共 N 条」、右侧为页码与每页条数，DOM MUST 对齐用户管理页（`page-summary` + `page-right`）
- **AND** `table-card` 内 MUST NOT 出现原型未定义的卡片内标题行
- **AND** 结果 MUST 记录在 change `trace.md`

#### Scenario: 弹窗并排验收

- **WHEN** 打开新增/编辑弹窗并排 `tile-sku-create-modal.html`
- **THEN** checklist（880px、字段顺序、无状态字段、多图主图、多视频、三按钮底栏、参考价格（元））MUST pass

#### Scenario: 弹窗矮视口滚动验收

- **WHEN** 在视口高度 ≤900px 打开新增/编辑 SKU 弹窗
- **THEN** 用户 MUST 可通过弹窗主体滚动访问全部字段与 footer 按钮
- **AND** 验收结果 MUST 记录在 fix change `trace.md`
