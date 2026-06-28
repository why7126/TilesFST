## 1. 准备与定位

- [x] 1.1 阅读 REQ-0014 v1.1（`requirement.md` §12、`acceptance.md` AC-024）
- [x] 1.2 对照 `profile_service.list_activities`、`profile_activity_repository.list_by_user` 当前 limit=20
- [x] 1.3 确认不涉及 DB migration、审计写入、timeline CSS

## 2. 后端

- [x] 2.1 `ProfileService.list_activities` 与 repository 默认 `limit=5`
- [x] 2.2 更新 `test_profile.py`：activities 响应最多 5 条、倒序
- [x] 2.3 若 OpenAPI 描述含「20 条」则改为「5 条」（无 schema 变更可跳过 Orval）

## 3. 前端（验证）

- [x] 3.1 确认 `ProfilePage` 渲染 API 返回项，无需额外 `slice(5)`（或文档说明依赖 API）
- [x] 3.2 可选：vitest mock 6 条 API 响应时页面仅 5 条（若后端已限 5，mock ≤5 断言条数）
- [x] 3.3 手动或 vitest：`/admin/profile` timeline ≤5 条

## 4. 验收与追溯

- [x] 4.1 对照 REQ-0014 AC-024、BUG-0049 驳回说明
- [x] 4.2 填写本 change `trace.md`（limit 5 验收结论）
- [x] 4.3 更新 `REQ-0014-profile-page/trace.md` 中 `fix-profile-activities-display-limit` 状态

## 5. 归档准备

- [x] 5.1 本文件全部 `[x]` 后执行 `/opsx-archive fix-profile-activities-display-limit`
