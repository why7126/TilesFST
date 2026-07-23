---
purpose: 全局规则
content: 团队研发规范和AI约束
source: AI自动生成初稿，项目团队确认
update_method: 项目初始化后由人工确认；后续由AI辅助更新并经人工Review
note: 适用于瓷砖信息管理平台项目模板
created_at: 2026-06-13 00:00:00
updated_at: 2026-07-22 13:11:58
---

# 测试规范

后端使用 pytest；前端使用 Vitest/Testing Library；接口变更必须补充集成测试。

## 契约变更与测试夹具

- API / Schema / 表单校验 / Workflow snapshot / 发布治理契约变更时，MUST 同步更新测试夹具、helper 与最小合法 payload，禁止测试继续提交已废弃或后端生成字段。
- 共享测试 helper SHOULD 使用最小合法输入；例如类目创建只提交 `name`、`sort_order` 等客户端仍可写字段，不提交由后端生成的 `code`。
- 测试读取 OpenSpec Change 文件时 MUST 兼容 active 与 archive 路径；优先复用 `tests/path_helpers.py` 的 `resolve_change_file()`，禁止只硬编码 `openspec/changes/<change-id>/...`。
- `/opsx-archive`、`/sprint-archive` 或发布准备前，SHOULD 运行相关 pytest，优先发现 archived path residual、fixture/schema drift 和测试 helper payload invalid。
