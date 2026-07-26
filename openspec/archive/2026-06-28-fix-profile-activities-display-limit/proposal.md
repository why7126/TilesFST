## Why

REQ-0014 **v1.1** 修订（2026-06-28）：个人资料页右侧「最近操作记录」侧栏卡片展示 **20** 条 timeline 信息密度过高；产品定稿为 **最多 5 条** 轻量预览。`add-admin-profile-page` 已按 v1（limit 20）归档，本缺口 MUST 通过新 `fix-*` change 对齐 REQ-0014 v1.1 与 acceptance AC-024。原 BUG-0049 已驳回（非缺陷，属需求修订）。

## What Changes

- `GET /api/v1/profile/me/activities` 默认返回最近 **5** 条（`profile_service.list_activities` / repository limit）。
- `ProfilePage` timeline 展示 API 返回项（≤5）；记录不足 5 时展示实际条数。
- 更新 `test_profile.py` activities limit 用例；可选 vitest 断言最多 5 条。
- **不** 变更 `profile_activity_logs` 写入逻辑、表结构、timeline 样式、空态文案。
- **不** 新增「查看更多」或分页；完整审计仍存 DB，仅 API/展示截断。

## Capabilities

### New Capabilities

（无。）

### Modified Capabilities

- `admin-profile-page`：MODIFIED「个人资料操作记录 API」— 默认 limit **5**；MODIFIED「管理端个人资料页面」— timeline **最多 5** 条。

## Impact

| 影响面 | 说明 |
|---|---|
| 后端 | `profile_service.py`、`profile_activity_repository.py`（默认 limit） |
| Web 管理端 | `ProfilePage.tsx`（若仅后端改 limit，前端无 slice；仍验 API 条数） |
| API / Orval | 行为变更（响应条数上限）；OpenAPI 描述若含 limit 文案则同步 |
| 数据库 | 无 |
| 店主端 / 小程序 | 无 |
| 父需求 | REQ-0014-profile-page v1.1 |
| 测试 | pytest `test_profile_activities_limit_and_order`；可选 vitest |

## Rollback Plan

1. 恢复 `profile_service` limit=20 与相关测试。
2. 重新部署 backend；前端无需变更（若仅后端 limit）。
3. 运行 `pytest tests/test_profile.py -k activities` 确认。
