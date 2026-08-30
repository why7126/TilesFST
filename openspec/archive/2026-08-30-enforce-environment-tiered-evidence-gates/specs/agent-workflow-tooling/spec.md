## ADDED Requirements

### Requirement: 环境证据强脚本门禁

workflow 归档命令 SHALL 运行环境分层 evidence 校验脚本，阻断开发证据冒充生产通过、DevTools evidence 冒充体验版或真机通过，以及生产专属证据未按目标环境后置或重新判定的情况。

#### Scenario: 单 Change 归档执行环境证据门禁
- **WHEN** 团队执行 `/opsx-archive <change-id>`
- **THEN** 归档流程 SHALL 校验目标 Change 的环境证据语义
- **AND** 发现开发 evidence 被写作生产通过、体验版通过或真机通过时 SHALL 阻断归档
- **AND** `production_only_pending` 若缺少目标环境、阶段或阻塞范围上下文 SHALL 阻断归档。

#### Scenario: Sprint 归档聚合环境证据门禁
- **WHEN** 团队执行 `/sprint-archive <sprint-id>` 或 Sprint archive readiness
- **THEN** readiness SHALL 聚合检查 Sprint 四件套和 scope 内 Change 文档的环境证据语义
- **AND** 任一目标文档存在环境证据强门禁 blocker 时 SHALL 阻断 Sprint close。

#### Scenario: 强门禁报告可定位
- **WHEN** 环境证据校验发现 blocker
- **THEN** 报告 SHALL 包含文件路径、行号或段落摘要、分类、消息和修复建议
- **AND** 报告 SHALL 不输出密钥、token、Cookie、Authorization header、`.env` 内容、真实客户数据或完整网络日志。
