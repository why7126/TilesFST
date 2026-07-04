---
title: 验收标准
purpose: REQ-0026 产品版本发布与公告管理验收标准
created_at: 2026-07-02 13:39:28
updated_at: 2026-07-03 23:56:30
owner: product
status: done
---

# 验收标准

## 1. 产品版本发布对象

- [x] AC-001 MUST 支持一个产品版本关联多个 Sprint。
- [x] AC-002 MUST 支持发布对象追踪关联 REQ、BUG 和 OpenSpec Change。
- [x] AC-003 MUST 明确产品版本发布公告与 Sprint 级 `release-note.md` 的职责差异。
- [x] AC-004 MUST 阻止未评审、未纳入交付或未归档闭环的内容进入正式发布范围。

## 2. 产品版本号

- [x] AC-005 发布时 MUST 校验 `src/shared/product-version.ts` 中 `PRODUCT_VERSION` 与发布公告版本一致。
- [x] AC-006 MUST NOT 使用 `package.json`、FastAPI `version`、OpenAPI 版本、Git commit 或 CI 构建号作为用户可见产品版本。
- [x] AC-007 若发布不改变 `PRODUCT_VERSION`，MUST 在发布材料中记录原因。

## 3. Mintlify 公开发布公告

- [x] AC-008 发布公告 MUST 面向公开页面展示。
- [x] AC-009 发布公告 MUST 采用 Mintlify 静态文档生成。
- [x] AC-010 发布公告 MUST 可在本地或等价环境完成构建/预览校验。
- [x] AC-011 发布公告 MUST 不依赖后端运行时 API 或数据库才能展示。
- [x] AC-012 发布公告源文件 MUST 可纳入 Git 管理并适合 Review。

## 4. 公告内容

- [x] AC-013 公告 MUST 包含版本号、发布时间和关联 Sprint。
- [x] AC-014 公告 MUST 汇总新增功能，并可追踪到 REQ。
- [x] AC-015 公告 MUST 汇总修复 BUG，并可追踪到 BUG。
- [x] AC-016 公告 MUST 包含发布注意事项。
- [x] AC-017 公告 MUST 包含已知问题。
- [x] AC-018 公告 MUST 包含升级步骤。
- [x] AC-019 公告 MUST 包含回滚说明。
- [x] AC-020 公告 MUST 包含影响范围，至少区分 Web 管理端、店主 Web、小程序、后端、数据库、对象存储和 Docker。
- [x] AC-021 公告 MUST NOT 泄露密钥、真实客户数据、内部数据库连接串、不可公开域名或敏感运维信息。

## 5. 发布前校验

- [x] AC-022 发布前 MUST 校验 OpenSpec Change 已 archive，相关能力已合并到 `openspec/specs/`。
- [x] AC-023 发布前 MUST 校验测试已按变更范围执行并记录结果。
- [x] AC-024 若涉及 API 变更，MUST 校验 OpenAPI 与 Orval 已同步。
- [x] AC-025 若涉及 Docker Compose 或部署变更，MUST 校验部署文档与 Compose 配置已同步。
- [x] AC-026 若涉及数据库迁移，MUST 校验迁移脚本、数据库文档和回滚说明已同步。
- [x] AC-027 若涉及环境变量，MUST 校验 `.env.example` 与相关注释已同步。
- [x] AC-028 任一必填校验失败时，发布流程 MUST 阻断并输出失败原因。

## 6. `releases/` 目录治理

- [x] AC-029 新增顶层 `releases/` 目录前 MUST 先通过 OpenSpec Change。
- [x] AC-030 OpenSpec Change MUST 更新 `rules/directory-structure.md`，说明 `releases/` 职责、边界、命名和生命周期。
- [x] AC-031 OpenSpec Change MUST 说明 `releases/` 与 `iterations/`、`issues/`、`openspec/changes/`、Mintlify 文档源之间的关系。
- [x] AC-032 在 OpenSpec Change 归档前 MUST NOT 直接创建 `releases/` 顶层目录。

## 7. 发布命令族

- [x] AC-033 后续发布命令族 SHOULD 至少覆盖创建发布计划、发布前校验、发布公告生成/确认。
- [x] AC-034 新增或修改 slash 命令时，MUST 以 `.cursor/commands/` 为事实源。
- [x] AC-035 命令同步后 MUST 运行 `python scripts/sync-agent-commands.py` 或等价同步流程。

## 8. 明确不做

- [x] AC-036 MUST NOT 在管理端菜单、登录页、店主端入口或小程序入口新增发布公告入口。
- [x] AC-037 MUST NOT 支持草稿、待发布、已发布、撤回等复杂发布状态机。
- [x] AC-038 MUST NOT 新增后端发布公告 API 或数据库表，除非后续 OpenSpec Change 明确要求。

## 9. Knowledge-base Gate

本 REQ 判定为发布治理 / 静态文档生成需求，不涉及管理端 CRUD 列表页、管理端表单页、管理端弹窗或媒体上传回显。

- [x] AC-KB-001 Knowledge-base gate 为 N/A，无需写入 `AC-XCUT-*`。
- [x] AC-KB-002 Trace MUST 记录 `knowledge_base_refs: []` 与 `cross_cutting_tags: []`。
- [x] AC-KB-003 Trace SHOULD 引用最近 Sprint 复盘中“acceptance 人工勾选被跳过、发布/归档校验需加强”的流程风险。
