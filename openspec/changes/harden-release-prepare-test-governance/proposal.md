# harden-release-prepare-test-governance

## 背景

`/release-prepare v0.0.5` 暴露 5 个测试失败，根因集中在测试治理漂移：AI usage snapshot fixture 缺少新字段、测试硬编码 active OpenSpec Change 路径、共享 helper 仍提交已废弃或非法的类目 payload。

## 目标

- 为测试读取 OpenSpec Change 文件提供 active / archive 兼容 helper。
- 在测试规则中明确契约变更必须同步测试夹具和共享 helper。
- 在 release-prepare 技能中要求对测试失败做分类，并对治理漂移输出可执行修复建议。

## 非目标

- 不新增业务功能。
- 不修改 API、数据库结构、权限或对象存储策略。
- 不替代后续真实生产 smoke、Mintlify preview 或小程序真机 evidence。

## 影响范围

- `rules/testing.md`
- `.agents/skills/release-prepare/SKILL.md`
- `tests/path_helpers.py`
- 相关回归测试 fixture
