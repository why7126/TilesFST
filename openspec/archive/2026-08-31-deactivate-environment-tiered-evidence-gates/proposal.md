---
created_at: 2026-08-31 10:23:00
updated_at: 2026-08-31 10:23:00
---

# 降级证据来源诊断门禁

## 背景

本项目发布治理已经收敛为单一项目发布语义，不再区分 development / production 发布目标。原“环境分层 evidence / 生产证据后置”门禁仍在 release、opsx archive 和 sprint archive 默认链路中自动应用，容易让操作者误以为生产发布目标分叉仍然存在。

## 变更内容

- 保留 `validate-environment-tiered-evidence.py` 及共享检测能力，作为手动诊断工具。
- 从 release、opsx archive、sprint archive 默认工作流中移除自动应用，不再作为阻断门禁。
- 将长期文案从“生产发布目标分层 / 生产证据后置”收敛为“证据来源声明 / 证据来源诊断”。
- 新流程不再推荐 `production_only_pending`，仅兼容历史记录或手动诊断输出。
- 更新相关 Skill、规则、脚本、测试和治理日志。

## 边界

- 不修改业务 `src/`。
- 不删除诊断脚本。
- 不引入新的发布目标维度。
- 不改写历史归档事实，仅更新当前治理入口和默认校验链路。
