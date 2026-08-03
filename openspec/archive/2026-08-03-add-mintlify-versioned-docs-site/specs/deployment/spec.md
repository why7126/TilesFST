## ADDED Requirements

### Requirement: Docker Compose 可选启动 Mintlify 文档站
部署能力 SHALL 支持通过 Docker Compose 可选 profile 启动 Mintlify 文档站服务，用于本地预览、演示部署或受控生产部署。

#### Scenario: 默认 Compose 不启动文档站服务
- **GIVEN** 运维未启用文档站 profile
- **WHEN** 运维执行默认 Docker Compose 启动或服务清单检查
- **THEN** Mintlify 文档站服务 SHALL NOT 被无条件启动
- **AND** backend、web、minio 或对象存储服务 SHALL NOT 依赖 Mintlify 文档站服务才能启动。

#### Scenario: docs-site profile 启动文档站
- **GIVEN** `mintlify/` 站点源目录已生成并通过校验
- **WHEN** 运维执行 `docker compose --profile docs-site up -d` 或等价命令
- **THEN** Compose SHALL 启动 Mintlify 文档站服务
- **AND** 服务 SHALL 使用 `mintlify/` 作为工作目录或挂载源
- **AND** 服务 SHALL 使用 `mintlify/mint.json` 或等价 Mintlify 配置启动文档站。

#### Scenario: 文档站服务端口可配置
- **WHEN** Compose 定义 Mintlify 文档站服务端口
- **THEN** 宿主机端口 SHALL 通过 `.env.example` 中的变量配置，例如 `HOST_PORT_MINTLIFY_DOCS`
- **AND** 项目 SHALL 在端口规则和部署文档中说明容器内端口、宿主机端口和端口冲突处理方式
- **AND** 实现 SHALL NOT 在多个文件中硬编码不可覆盖的文档站宿主机端口。

### Requirement: Mintlify 文档站部署说明和发布门禁
部署能力 SHALL 文档化 Mintlify 文档站的本地、演示和生产部署选择，并 SHALL 在发布涉及 Compose 文档站服务时纳入验证证据。

#### Scenario: 部署文档说明文档站承载方式
- **WHEN** 运维阅读部署文档
- **THEN** 文档 SHALL 说明本地或演示环境如何通过 Compose profile 启动 Mintlify 文档站
- **AND** 文档 SHALL 说明生产可选择 Compose 内 Mintlify 服务、外部 Mintlify 托管、静态托管、CDN rewrite 或反向代理
- **AND** 未确认生产承载方式时，发布准备 SHALL 记录 blocker 或待确认项。

#### Scenario: Compose 文档站服务进入发布范围
- **WHEN** 发布范围包含 Mintlify Compose service、Dockerfile、Compose 配置或相关 `.env.example` 变量变更
- **THEN** 发布流程 SHALL 要求 Docker Compose 验证证据
- **AND** 发布流程 SHALL 按发布规范判断是否需要 `/image-prepare` 与 `/image-build` 证据
- **AND** 验证证据 SHALL NOT 包含真实生产域名、外部托管账号、访问 token、真实 `.env` 或不可公开运维信息。

#### Scenario: Compose 注释和环境变量同步
- **WHEN** 新增或修改 Mintlify 文档站 service、ports、volumes、profiles、environment 或 command
- **THEN** Compose 文件 SHALL 包含邻近注释说明用途、默认值、安全边界和持久化影响
- **AND** `.env.example`、`rules/environment.md`、`rules/port-management.md` 和 `docs/02-deployment.md` SHALL 同步说明相关变量和端口。
