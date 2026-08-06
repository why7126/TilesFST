---
created_at: 2026-08-05 14:39:06
updated_at: 2026-08-05 23:29:59
source_requirement: REQ-0100-mintlify-docs-site-ia-content-experience
---

# 设计说明

## D1 信息架构策略

本 Change 采用“Mintlify 原生文档站体验增强”策略：优先调整 `mintlify/` 下的 MDX 页面、Mintlify 配置、README / manifest 说明和校验脚本，不将 REQ 原型转换成 `src/web` 应用页面，也不引入 Web 管理端或小程序代码。

验收返修后，站点主配置从旧式 `mint.json` 迁移为 `docs.json` 唯一主配置，使用 Mintlify `mint` theme、站点色彩、favicon、versions、tabs 和 groups 组织导航。`mint.json` 不再作为 Mintlify 源目录主配置存在。

推荐站点结构：

```text
开始
├── 产品简介
├── 快速开始
└── 当前版本总览

当前版本
├── 管理端
│   ├── 管理端使用说明
│   ├── 商品资料维护
│   ├── 品牌、证书、Banner 与媒体
│   └── 账号、设置、日志与接口文档
├── 小程序
│   ├── 小程序使用说明
│   ├── 浏览、搜索、商品与收藏
│   └── 品牌与证书
├── 公开浏览
└── 常见问题

历史版本
├── v0.3.4
└── v0.3.3

发布公告
├── v0.3.4
└── v0.3.3
```

## D2 首页内容模型

首页或等价首页入口应承载五类信息：

- 产品定位：瓷砖资料展示、查询、维护和版本化产品文档浏览。
- 角色入口：企业员工、系统管理员、店主/导购、公开访客。
- 常用任务：商品资料维护、品牌证书、Banner/媒体、小程序浏览、公开浏览、FAQ。
- 当前版本：展示 `latest` 指向的实际版本和当前文档范围。
- 发布公告：展示最近版本公告入口。

首页可以使用 Mintlify 的 CardGroup、Card、Accordion、Steps、Info/Warning 等 MDX 组件，但不得使用无业务意义的装饰内容替代产品说明。

## D3 事实源边界

本 Change 不改变既有事实源关系：

```text
releases/vX.Y.Z/release.json
    └── 发布事实源

releases/vX.Y.Z/usage-docs/manifest.json
    └── 该版本产品使用文档事实源

mintlify/site-manifest.json
    └── 站点投影、latest、截图资产和人工覆盖记录

mintlify/docs/latest/
    └── 当前站点默认版本投影，不是独立产品事实源
```

实现不得绕过 release 快照直接以 `mintlify/` 改写历史版本产品语义。历史版本内容性更正必须记录授权来源、原因、时间和文件范围。

## D4 参考项目裁剪

可借鉴：

| 来源 | 借鉴点 |
|---|---|
| ProjectDocs/promptt | 首页卡片、产品简介、用户指南、快速上手、FAQ、更新公告的组织方式。 |
| langgenius/dify-docs | 多层导航、场景分组、站点级 metadata、footer、redirects、文档贡献和写作治理。 |

不可照搬：

- Dify 的 Cloud / Self-hosted / Developer Resources 多产品线结构。
- Dify 的多语言体系，除非后续另有需求。
- AI 平台、模型、工作流、API endpoint 示例等与瓷砖平台无关内容。
- 参考项目的品牌、logo、外部域名、analytics ID、版权配置。

## D5 冲突处理

REQ-0100 存在 `prototype/web/index-wireframe.html` 和 `prototype/web/context.md`。优先级按项目规则为 HTML > context > acceptance > ui-design > spec。

冲突结论：

- HTML 线框只约束 Mintlify 首页的信息架构和入口内容，不要求生成 `src/web` 应用源码。
- context 中的角色入口和导航结构与 acceptance 一致，无功能冲突。
- 若后续实现发现某个卡片目标页面不存在，应优先按 acceptance 移除或替换入口，不保留空链接。
- 若 `mint.json` 与 `docs.json` 迁移存在兼容冲突，优先使用 `docs.json` 作为唯一主配置；生成器和校验必须阻断 `mintlify/mint.json` 与 `docs.json` 并存。

## D6 校验策略

实现应提供或更新静态校验，至少覆盖：

- Mintlify 配置结构合法。
- `docs.json` 使用 `mint` theme、站点色彩、favicon、versions、tabs 和 groups。
- 导航引用页面存在。
- `latest` 指向 site manifest 中最新可用 usage docs 版本。
- `releases/<version>/usage-docs/manifest.json` 页面清单与站点投影目录一致。
- 站内链接、公告链接、图片引用有效。
- `mintlify/` 不包含 `.DS_Store`、构建产物、`node_modules/`、`.mintlify/`、`dist/`、`build/` 等。
- 公开安全扫描拒绝密钥、真实客户数据、Authorization header、Cookie、数据库连接串、生产私有域名、本地绝对路径等。
- Mintlify CLI `broken-links` 或等价预览链接检查通过；若 preview 无法运行，验收记录必须说明原因。

## D8 Docs-site 预览镜像策略

验收返修确认 Docker `docs-site` profile 不得再使用静态目录服务器替代 Mintlify 预览。Compose 应使用 `deploy/docs-site/Dockerfile` 构建本地可复用镜像，在构建阶段预装 Mintlify CLI，并在容器内运行 `mintlify dev --host 0.0.0.0 --port 3000`。

运行时只挂载公开 `mintlify/` 源目录和 Docker named volume 缓存，禁止挂载宿主机 `~/.mintlify*`。这样可以避免 root/Docker 用户写入宿主机 Mintlify 缓存后导致 `ENOTEMPTY`、权限漂移或目录索引 fallback 被误认为真实预览。

## D7 知识库引用

后续实现设计和验收应继承 REQ trace 中的经验：

- `docs/knowledge-base/retrospectives/sprint-017-retrospective.md`：usage docs 生成/跳过决策必须显式确认。
- `docs/knowledge-base/retrospectives/sprint-018-retrospective.md`：Mintlify 文档站应继续从 release manifest 出发，避免 `mintlify/` 反向成为事实源。
- `docs/knowledge-base/retrospectives/sprint-019-retrospective.md`：文档治理需要避免中间态文案和路径残留漂移。
