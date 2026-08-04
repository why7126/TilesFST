## ADDED Requirements

### Requirement: 小程序发布前 Network checklist
产品版本发布管理能力 SHALL 在小程序发布准备流程中纳入 DevTools Network 与体验版 Network 人工检查清单，确保发布确认前能区分自动门禁、真实小程序网络链路验证、阻塞项和 follow-up 风险。

#### Scenario: miniapp prepare 输出 Network checklist
- **WHEN** `/miniapp-prepare` 或等价小程序发布准备命令完成自动门禁
- **THEN** 输出 SHALL 区分 prod 策略、`urlCheck=true`、静态测试和生产接口 smoke 等自动门禁
- **AND** 输出 SHALL 包含 DevTools Network 人工检查项
- **AND** 输出 SHALL 包含体验版 Network 人工检查项
- **AND** 输出 SHALL 指向 `/miniapp-confirm` 或等价确认流程记录验证结论
- **AND** 输出 SHALL NOT 将未执行的人工 Network checklist 标记为自动通过。

#### Scenario: Network checklist 覆盖关键页面和资源
- **WHEN** 发布负责人执行小程序 Network checklist
- **THEN** checklist SHALL 至少覆盖首页、一个列表页、一个详情或媒体资源页面
- **AND** 首页检查 SHALL 覆盖首页聚合接口、Banner、推荐商品、静态资源和错误态
- **AND** 列表页检查 SHALL 覆盖列表接口、分页请求、空态和网络失败提示
- **AND** 详情或媒体资源页面检查 SHALL 覆盖图片、视频、证书图片或受控媒体 URL 的加载结论。

#### Scenario: Network 失败阻断发布准备通过
- **WHEN** DevTools 或体验版实际请求仍指向本地或非预期环境
- **THEN** 发布准备 SHALL 标记 failed 或 blocker
- **AND** 关键 API 返回非 2xx HTTP 状态且页面无可接受降级时 SHALL 标记 failed
- **AND** 关键业务响应失败且影响首页、列表或详情主路径时 SHALL 标记 failed
- **AND** 图片、视频或证书资源域名不合法并导致核心内容不可用时 SHALL 标记 failed 或 blocked。

#### Scenario: miniapp confirm 承接 Network evidence
- **WHEN** `/miniapp-confirm` 或等价确认流程记录小程序体验版或正式版验证结果
- **THEN** 记录 SHALL 支持表达 DevTools Network 结论、体验版 Network 结论、失败项、阻塞项、剩余风险和下一步
- **AND** 缺少体验版 Network evidence 时 SHALL 记录 `blocked`、`follow_up` 或明确的 `not_applicable` 原因
- **AND** 记录 SHALL NOT 包含 token、Cookie、Authorization header、`.env`、真实密钥、真实客户数据或未脱敏隐私。
