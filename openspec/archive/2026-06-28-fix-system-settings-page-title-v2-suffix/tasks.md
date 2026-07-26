## 1. 准备

- [x] 1.1 阅读 BUG-0042 acceptance.md
- [x] 1.2 定位 `SystemSettingsPage.tsx` L798

## 2. 修复

- [x] 2.1 眉标改为 `SYSTEM / SYSTEM SETTINGS`
- [x] 2.2 同步 5 份 prototype HTML eyebrow
- [x] 2.3 勾选 BUG-0042 AC-001～AC-006

## 3. 测试

- [x] 3.1 Vitest 断言眉标无 `/ V2`
- [x] 3.2 `pnpm vitest run SystemSettingsPage`

## 4. 追溯

- [x] 4.1 填写 change `trace.md`；更新 BUG trace
- [x] 4.2 评估 `docs/knowledge-base/incidents/`（不需要）

## 5. 归档

- [x] 5.1 全部 `[x]` 后 `/opsx-archive fix-system-settings-page-title-v2-suffix`
