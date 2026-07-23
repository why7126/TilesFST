## ADDED Requirements

### Requirement: 小程序环境命令族
系统 MUST 提供两段式小程序环境命令族，用于切换、检查、发布前准备、验证确认和发布后恢复小程序 API 环境策略。

#### Scenario: 命令入口命名
- **WHEN** 用户查看或使用小程序环境命令
- **THEN** 系统 MUST 提供 `/miniapp-env`、`/miniapp-check`、`/miniapp-prepare`、`/miniapp-confirm` 和 `/miniapp-restore`
- **AND** 命令名 MUST 保持两段式 `<domain>-<action>` 风格

#### Scenario: 不越权发布
- **WHEN** 用户执行 `/miniapp-prepare` 或 `/miniapp-confirm`
- **THEN** 系统 MUST 明确这些命令不调用微信平台真实发布动作
- **AND** 系统 MUST 输出需要人工在微信开发者工具或微信公众平台完成的步骤

### Requirement: 小程序环境策略
系统 MUST 支持 `dev`、`prod` 和 `auto` 三种小程序环境策略，并同步维护 TypeScript 源码和微信运行时 JavaScript 文件。

#### Scenario: 切换到开发策略
- **WHEN** 用户执行 `/miniapp-env dev`
- **THEN** 系统 MUST 将小程序环境解析策略设置为使用本地开发 API 地址
- **AND** 系统 MUST 同步更新 `src/miniapp/utils/env.ts` 与 `src/miniapp/utils/env.js`

#### Scenario: 切换到生产策略
- **WHEN** 用户执行 `/miniapp-env prod`
- **THEN** 系统 MUST 将小程序环境解析策略设置为所有运行形态使用生产 API 地址
- **AND** 生产 API 地址 MUST 为 `https://tilesfst.wjoyhappy.site`

#### Scenario: 切换到自动策略
- **WHEN** 用户执行 `/miniapp-env auto`
- **THEN** 系统 MUST 将开发版解析为本地开发 API 地址
- **AND** 系统 MUST 将体验版和正式版解析为生产 API 地址

### Requirement: 小程序环境检查
系统 MUST 提供环境检查命令，验证当前策略、运行入口同步、静态测试和生产公开接口可访问性。

#### Scenario: 检查当前策略
- **WHEN** 用户执行 `/miniapp-check`
- **THEN** 系统 MUST 报告当前小程序环境策略、开发 API 地址、生产 API 地址和 fallback 配置
- **AND** 系统 MUST 检查 `.ts` 与 `.js` 环境配置一致

#### Scenario: 发布前接口 smoke
- **WHEN** 用户执行 `/miniapp-prepare`
- **THEN** 系统 MUST 检查 `GET /api/v1/miniapp/home` 和 `GET /api/v1/miniapp/brands?page=1&pageSize=2` 的生产 HTTPS 响应
- **AND** 任一接口非 `200 OK` 或统一响应 `code != 0` 时 MUST 阻断发布准备

### Requirement: 小程序发布确认与恢复
系统 MUST 支持记录小程序体验版或正式版验证结论，并支持发布后恢复默认环境策略。

#### Scenario: 记录验证确认
- **WHEN** 用户执行 `/miniapp-confirm`
- **THEN** 系统 MUST 记录或输出小程序版本、渠道、验证时间、验证范围、结果和剩余风险
- **AND** 系统 MUST 不记录真实用户隐私、微信会话密钥、Authorization header、Cookie 或 `.env` 内容

#### Scenario: 恢复默认策略
- **WHEN** 用户执行 `/miniapp-restore`
- **THEN** 系统 MUST 将小程序环境策略恢复为项目默认策略
- **AND** 系统 MUST 运行环境静态检查并输出恢复后的策略摘要
