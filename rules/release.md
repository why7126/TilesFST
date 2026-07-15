---
purpose: 全局规则
content: 团队研发规范和AI约束
source: AI自动生成初稿，项目团队确认
update_method: 项目初始化后由人工确认；后续由AI辅助更新并经人工Review
note: 适用于瓷砖信息管理平台项目模板
created_at: 2026-06-13 00:00:00
updated_at: 2026-07-14 19:05:47
---

# 发布规范

发布前必须完成测试、OpenSpec校验、接口生成、变更归档和发布说明。

## 发版检查清单（Web 产品版本）

对外发布 Web 管理端或店主端时，若本次发版包含产品版本语义变更，MUST 人工更新：

```text
src/shared/product-version.ts  →  PRODUCT_VERSION（如 v0.0.1）
```

MUST NOT 依赖 `package.json`、FastAPI `version`、OpenAPI 版本、Git commit 或 CI 构建号作为用户可见产品版本。

## 产品版本发布对象

产品版本发布对象用于表达一次对外产品发版，放入：

```text
releases/vX.Y.Z/release.json
```

产品版本发布对象 MUST 支持：

- 一个产品版本关联一个或多个 Sprint。
- 追踪关联 REQ、BUG 和 OpenSpec Change。
- 区分 Sprint `release-note.md` 与产品版本公告：Sprint release note 描述迭代交付，产品版本公告描述对外版本。
- 阻止未评审、未纳入交付或未归档闭环的内容进入正式发布范围。

## 公开发布公告

公开发布公告源文件放入：

```text
releases/vX.Y.Z/announcement.mdx
```

发布公告 MUST：

- 面向公开页面展示。
- 使用 Mintlify 静态文档生成或预览校验。
- 可纳入 Git Review。
- 不依赖后端运行时 API 或数据库才能展示。
- 包含版本号、发布时间、关联 Sprint、新增功能、修复 BUG、发布注意事项、已知问题、升级步骤、回滚说明和影响范围。
- 不泄露密钥、真实客户数据、内部数据库连接串、MinIO 凭据、不可公开域名或敏感运维信息。

## 发布前门禁

发布确认前 MUST 校验：

| 门禁 | 要求 |
|---|---|
| OpenSpec | 关联 Change 已 archive，相关能力已合并到 `openspec/specs/`；未归档项不得进入正式发布范围 |
| 测试 | 按变更范围执行并记录结果 |
| API / Orval | 涉及 API 变更时，OpenAPI 与 Orval 已同步 |
| Docker Compose | 涉及部署变更时，Compose 配置与部署文档已同步 |
| 数据库 | 涉及数据库迁移时，迁移脚本、数据库文档和回滚说明已同步 |
| 环境变量 | 涉及环境变量时，`.env.example` 与相邻注释已同步 |
| 产品版本 | `src/shared/product-version.ts` 的 `PRODUCT_VERSION` 与发布对象版本一致；如不更新，必须记录原因 |
| Mintlify | 公告 build / preview 或等价校验通过 |

任一必填门禁失败时，发布流程 MUST 阻断，并输出失败原因与修复建议。

## 发布命令族

发布命令族以 `.agents/skills/release-*`（若存在）或对应 Codex 技能为入口；新增或修改发布命令时 MUST 更新 `.agents/skills/`。

推荐命令：

| 命令 | 目标 |
|---|---|
| `/release-propose <version>` | 创建或更新产品版本发布计划，选择关联 Sprint / REQ / BUG / Change |
| `/release-prepare <version>` | 执行发布前校验，生成或更新 Mintlify 公告源文件 |
| `/release-publish <version>` | 记录发布确认结果和最终公告位置 |

本项目当前不引入草稿、待发布、已发布、撤回等复杂发布状态机。发布命令只记录计划、校验和确认事实。
