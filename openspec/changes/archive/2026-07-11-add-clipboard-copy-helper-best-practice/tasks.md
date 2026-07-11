## 1. Shared Clipboard Helper

- [x] 1.1 Add a shared Web frontend Clipboard copy helper with structured results for `success`, `failed`, `unavailable`, and `empty`.
- [x] 1.2 Support an optional fallback selector callback and guard against fallback callback failures.
- [x] 1.3 Ensure the helper does not log copied text or know business toast, dialog, or telemetry event names.

## 2. Representative Caller Migration

- [x] 2.1 Migrate `/admin/logs` request id copy to the shared helper or equivalent normalized pattern while preserving fixed toast feedback and successful `copy_request_id` telemetry.
- [x] 2.2 Migrate the reset-password result dialog copy flow to the shared helper or equivalent normalized pattern while preserving input focus/select manual fallback.
- [x] 2.3 Preserve existing user-facing copy semantics for request id and generated password copy states.

## 3. Documentation And Design System Notes

- [x] 3.1 Document the helper usage boundary in Web README, Design System notes, or implementation design notes: helper owns copy result normalization; callers own UI and telemetry.
- [x] 3.2 Confirm no new raw Hex, one-off toast/dialog system, backend API, database change, Orval output, Docker config, or miniapp Clipboard path is introduced.

## 4. Tests And Verification

- [x] 4.1 Add helper unit tests for success, empty input, Clipboard API unavailable, write rejection, fallback invocation, and fallback throwing without crashing.
- [x] 4.2 Update logs page tests for request id copy success, unavailable fallback, write failure fallback, empty request id, and pagination structure.
- [x] 4.3 Update reset-password dialog tests for copy success, unavailable fallback, write failure fallback, input focus/select, and sensitive value non-telemetry.
- [x] 4.4 Run the focused Web test suite for helper, logs page, and reset-password dialog.
- [x] 4.5 Record AC-XCUT verification for fixed toast no layout shift and reset-password modal width/body-scroll stability.

## 实现记录

- 新增 `src/web/src/shared/lib/clipboard.ts`，迁移 `/admin/logs` 与 `ResetPasswordDialog`。
- `copyTextToClipboard` 不直接触发 toast、dialog、埋点，也不记录复制内容；调用方仍负责业务文案和成功埋点。
- 本 Change 未新增后端 API、数据库、Orval、Docker、小程序路径、裸 Hex 或新 toast/dialog 体系。
- AC-XCUT：日志审计继续使用 fixed `AdminToast`；未改分页 DOM；重置密码弹窗未改容器 class/宽度，modal width/body-scroll 验收为 N/A — 未触达容器宽度与滚动样式。
- 已运行 `pnpm --dir src/web test -- src/shared/lib/clipboard.test.ts src/pages/admin/LogAuditPage.test.tsx src/features/admin/components/ResetPasswordDialog.test.tsx`。
