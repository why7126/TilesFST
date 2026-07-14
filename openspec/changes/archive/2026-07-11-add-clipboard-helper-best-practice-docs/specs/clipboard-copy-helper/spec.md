## ADDED Requirements

### Requirement: Clipboard helper best-practice 文档

系统 MUST 为 Web 管理端 Clipboard helper 调用方提供长期可发现的 best-practice 文档，用于沉淀复制提示文案、fallback 策略、敏感值边界、调用方 checklist、示例与反例。该文档 MUST 服务于后续新增复制入口的开发、评审和 QA 验收，不得替代 Clipboard helper 本体实现要求。

#### Scenario: 文档落位与入口可发现

- **WHEN** 开发者需要新增或评审 Web 管理端复制入口
- **THEN** `docs/knowledge-base/best-practices/` 或等价长期文档位置 SHALL 提供 Clipboard helper best-practice 文档
- **AND** `docs/knowledge-base/README.md`、`src/web/README.md` 或等价索引 SHALL 提供可发现入口
- **AND** 文档 SHALL 说明其适用于 Web 管理端 Clipboard helper 调用方，不替代 helper 实现要求。

#### Scenario: 调用方文案映射已文档化

- **WHEN** 调用方根据 Clipboard helper 返回的结构化结果展示用户反馈
- **THEN** best-practice 文档 SHALL 说明 `success`、`failed`、`unavailable`、`empty` 的推荐文案原则
- **AND** 成功或失败提示 SHALL 保留业务对象名称，例如 `request_id`、随机密码或版本号
- **AND** 文案 SHALL NOT 直接回显 Token、密钥、Cookie、Authorization、客户隐私原文或其他敏感值。

#### Scenario: fallback 策略已文档化

- **WHEN** Clipboard API 不可用、写入失败、fallback 回调失败或待复制内容为空
- **THEN** best-practice 文档 SHALL 说明手动选择文本、禁用或隐藏复制入口、明确失败提示等调用方策略
- **AND** 文档 SHALL 要求调用方不得让复制点击在失败路径下无用户可感知反馈
- **AND** 文档 SHALL 保持 helper 与 UI 解耦，调用方负责 toast、`role="status"`、弹窗提示和业务 DOM。

#### Scenario: 敏感值边界已文档化

- **WHEN** 调用方准备为某个文本提供复制入口
- **THEN** best-practice 文档 SHALL 至少区分允许复制、谨慎复制、禁止或默认不复制三类数据
- **AND** AccessKey、SecretKey、Token、Cookie、Authorization、客户隐私原文 SHALL 被列为禁止或默认不复制类别，除非后续有专门安全流程
- **AND** 文档 SHALL 要求 helper 与调用方不得将复制原文写入日志、埋点 payload、测试快照、控制台输出或错误消息。

#### Scenario: checklist、示例与反例可用于评审

- **WHEN** reviewer 或 QA 检查新增复制入口
- **THEN** best-practice 文档 SHALL 提供调用方 checklist，覆盖授权可见、敏感值分类、结果文案、fallback、空值、日志/埋点和测试覆盖
- **AND** 文档 SHOULD 提供推荐示例与反例
- **AND** 示例 SHALL 使用脱敏或虚构值，不得包含真实密钥、真实 Token、真实客户隐私数据或真实生产签名 URL。
