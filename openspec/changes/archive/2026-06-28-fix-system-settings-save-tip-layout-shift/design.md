## Context

- **BUG**: BUG-0047（medium）
- **Reference**: `fix-admin-list-status-toast-layout`、BUG-0015

## Decisions

### D1：采用 AdminToast（推荐）

- 通过 `AdminLayout` outlet context 或等价机制触发 toast
- 移除文档流 `settings-save-tip`

### D2：文案保持不变

- 「设置已保存并立即生效」「已恢复默认配置」

## Test Plan

- vitest：`.admin-toast-region` 出现；主内容无 layout shift（可选 ref 断言）
