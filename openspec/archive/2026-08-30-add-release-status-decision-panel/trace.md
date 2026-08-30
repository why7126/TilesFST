---
created_at: 2026-08-30 10:25:00
updated_at: 2026-08-30 11:13:00
---

# 追踪

## 来源

- 命令：`/spec-opt 固化发布流程 Release Status 决策面板、blocker 分类、默认 upgrade 路径提示与 image input hash 边界`
- 用户决策：本 Change 不包含发布编排能力。

## 影响

- 仅影响治理资产。
- 不涉及后端 API、数据库 schema、Web、小程序或管理端业务实现变更。

## 验证计划

- `python scripts/validate-release.py --release-dir releases/v1.2.1 --status`
- 聚焦 release status 测试。
- image build 校验测试。
- OpenSpec 与目录治理检查。
