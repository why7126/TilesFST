# product-release-management 规格变更

## MODIFIED Requirements

### Requirement: Mintlify 站点发布门禁
产品版本发布管理能力 SHALL 在发布准备和发布确认阶段校验 Mintlify 站点源目录、站点导航、共享截图、页面表达和公开安全。

#### Scenario: 发布准备校验站点目录
- **WHEN** `/release-prepare <version>` 处理 `usage_docs.status=generated` 的版本
- **THEN** 发布准备流程 SHALL 校验 release usage docs 快照与 `mintlify/docs/<version>/**` 的页面清单一致
- **AND** SHALL 校验 `mintlify/docs.json` 或等价唯一主配置包含该版本公告、产品文档入口、站点 theme、metadata、版本、tabs 和 groups
- **AND** SHALL 校验共享截图引用、截图 hash、broken links 或等价静态构建结果
- **AND** 失败时 SHALL 记录 blocker 或阻断发布确认。

#### Scenario: 公开安全覆盖 Mintlify 目录
- **WHEN** 校验产品使用文档、manifest、Mintlify 配置或 `mintlify/` 站点源文件
- **THEN** 校验 SHALL 拒绝密钥、真实 `.env` 内容、数据库连接串、Authorization header、Cookie、对象存储凭据、非公开运维地址、本地绝对路径或真实客户数据。

#### Scenario: 站点配置和链接质量校验
- **WHEN** 校验 Mintlify 文档站体验
- **THEN** 校验 SHALL 发现导航引用缺页、首页卡片空链接、站内 broken links、图片引用错误、`latest` 指针漂移和 site manifest 漂移
- **AND** 校验 SHALL 阻断 `.DS_Store`、构建产物、`node_modules/`、`.mintlify/`、`dist/`、`build/` 等进入公开文档站源目录
- **AND** 校验输出 SHALL 摘要化展示 pass、warning、blocker、涉及路径和建议修复方向。

#### Scenario: 本地 docs-site 镜像预览 Mintlify 文档站
- **WHEN** Docker Compose 启用 `docs-site` profile
- **THEN** docs-site 服务 SHALL 使用项目内 Dockerfile 构建本地可复用镜像并预装 Mintlify CLI
- **AND** 服务 SHALL 运行 Mintlify dev preview，而不是目录索引或仅返回 MDX 原文的静态文件服务器
- **AND** Mintlify 运行缓存 SHALL 写入容器内部路径或 CLI 自行管理的临时目录，不得挂载或写入宿主机 `~/.mintlify*`
- **AND** docs-site 服务 SHALL NOT 将 Docker named volume 直接挂载到 `/home/node/.mintlify`
- **AND** Compose config 校验 SHALL 覆盖根、local 和 prod docs-site 入口。
