## ADDED Requirements

### Requirement: Dialog Modal 外部点击关闭治理

Design System SHALL define the default close interaction for Web standard Dialog / Modal components: clicking the backdrop, overlay, or outside empty area SHALL NOT close the dialog. Dialog / Modal components SHALL keep explicit close affordances and SHALL preserve existing semantic token styling, width strategy, scroll strategy, and accessibility semantics.

#### Scenario: 共享 Dialog 默认禁用外部点击关闭

- **WHEN** developers use the shared Web Dialog / Modal component or equivalent Design System wrapper
- **THEN** clicking the backdrop, overlay, or outside empty area SHALL NOT close the dialog by default
- **AND** the component SHALL expose or document an explicit exception path only for reviewed use cases

#### Scenario: 明确关闭入口保持可用

- **WHEN** a standard Dialog / Modal is rendered
- **THEN** it SHALL provide a visible close icon, cancel button, back button, or business-completion close path
- **AND** keyboard close behavior such as Esc MAY remain available when documented by the consuming feature
- **AND** disabling outside click close SHALL NOT trap users in a dialog with no visible exit

#### Scenario: 弹窗样式和宽度策略不回退

- **WHEN** a Web admin Dialog / Modal implementation is added or modified
- **THEN** it SHALL use existing semantic token classes, CSS variables, or existing admin modal classes
- **AND** it SHALL NOT add raw Hex colors or one-off hardcoded design colors in production Web UI
- **AND** wide admin dialogs SHALL NOT combine generic `modal-card` with a feature-specific modal card class in a way that reintroduces CSS cascade width overrides

#### Scenario: 轻量浮层边界清晰

- **WHEN** developers implement Popover, Dropdown, Tooltip, Select dropdown, date picker, or equivalent lightweight overlay components
- **THEN** this Dialog / Modal outside click policy SHALL NOT automatically apply
- **AND** those lightweight overlays SHALL keep their component-specific close behavior unless a reviewed requirement explicitly changes it
