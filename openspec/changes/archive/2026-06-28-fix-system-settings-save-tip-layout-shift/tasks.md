## 1. 准备

- [x] 1.1 阅读 BUG-0047 acceptance；对照 `AdminLayout` / `AdminToast`

## 2. 修复

- [x] 2.1 保存/恢复成功改 AdminToast
- [x] 2.2 移除或停用文档流 `settings-save-tip`
- [x] 2.3 勾选 AC-001～AC-007

## 3. 测试

- [x] 3.1 vitest toast 断言
- [x] 3.2 `pnpm vitest run SystemSettingsPage`

## 4. 归档

- [x] 4.1 trace；`/opsx-archive fix-system-settings-save-tip-layout-shift`
