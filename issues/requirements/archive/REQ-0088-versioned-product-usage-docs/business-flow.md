---
requirement_id: REQ-0088-versioned-product-usage-docs
title: 版本化产品使用文档生成与发布治理 - 业务流程
status: done
created_at: 2026-08-01 08:24:50
updated_at: 2026-08-02 17:59:12
owner: product
---

# 业务流程

## 1. 总体流程

```text
已评审 / 已归档交付范围
        |
        v
/release-propose <version>
        |
        | 生成 release.json，记录 Sprint / REQ / BUG / Change / impact_scope
        v
/release-prepare <version>
        |
        +-- 生成 announcement.mdx
        |
        +-- 确认本次是否需要生成 / 更新 usage-docs
        |       |
        |       +-- 未确认：记录 blocker，等待用户确认
        |       |
        |       +-- 不需要：记录 usage_docs skipped + rationale
        |       |
        |       +-- 需要：/usage-docs-generate <version>
        |               |
        |               +-- 读取 release.json
        |               +-- 读取上一版本 usage-docs（如存在）
        |               +-- 读取管理端导航 / 小程序页面 / 发布影响范围
        |               +-- 写入当前版本 usage-docs/**
        |               +-- 写入 usage-docs/manifest.json
        |
        +-- 需要生成 / 更新时：/usage-docs-validate <version>
        |       |
        |       +-- 校验 manifest
        |       +-- 校验 Mintlify 导航
        |       +-- 校验 broken links
        |       +-- 校验敏感信息
        |       +-- 校验覆盖度和旧版本改写策略
        |
        v
记录 usage_docs_preview gate 或 skipped rationale
        |
        v
/image-prepare / /image-build（按需）
        |
        v
/release-publish <version>
        |
        | 校验 release gates + usage docs + image evidence（按需）
        v
发布确认或阻断
```

## 2. 产品文档生成决策流程

```text
读取 releases/<version>/release.json
    |
    v
汇总本次发布影响范围和上一版本文档状态
    |
    v
询问用户是否需要生成 / 更新产品文档
    |
    +-- 未确认：阻断，记录 pending_confirmation
    |
    +-- 不需要：记录 skipped、确认来源和跳过原因
    |
    +-- 需要
            |
            v
识别上一版本 usage-docs
            |
            +-- 存在：复制为当前版本基础
            +-- 不存在：使用 releases/templates/usage-docs 模板
            |
            v
读取当前版本文档覆盖输入
            |
            +-- 管理端导航 admin-nav.ts
            +-- Web 路由 App.tsx
            +-- 小程序 app.json
            +-- 产品总览 docs/00-product-overview.md
            +-- release.json 正式范围
            |
            v
生成或更新当前版本页面
            |
            v
写入 usage-docs/manifest.json
```

## 3. 产品文档校验流程

```text
读取 usage-docs/manifest.json
    |
    v
校验结构和版本一致性
    |
    +-- version 与 release.json 一致
    +-- pages 与实际文件一致
    +-- input_files 可解析
    |
    v
校验 Mintlify 导航
    |
    +-- 当前版本公告入口
    +-- 当前版本产品文档入口
    +-- 历史版本入口
    |
    v
校验公开安全
    |
    +-- 无密钥 / 连接串 / Authorization / Cookie / 真实客户数据
    |
    v
校验覆盖度
    |
    +-- 管理端菜单
    +-- 小程序 tabBar / 主要页面
    +-- release impact_scope
    |
    v
输出 pass / blocker / warning
```

## 4. 旧版本维护流程

```text
发现旧版本文档需要维护
    |
    v
判断变更类型
    |
    +-- 非内容性维护 / 安全修复
    |       |
    |       v
    |   自动化可执行，manifest 留痕
    |
    +-- 内容性更正
            |
            v
        需要明确授权
            |
            v
        记录原因 / 操作者 / 时间 / 文件范围 / 说明
```

## 5. 与已有发布流程的差异

| 现状 | 新流程 |
|---|---|
| Mintlify 主要承载版本公告 | Mintlify 同时承载版本公告和产品使用文档 |
| `/release-prepare` 只校验公告和发布门禁 | `/release-prepare` 先确认是否需要 usage-docs；需要时生成并校验，不需要时记录跳过原因 |
| 文档更新依赖人工记忆 | 文档生成、校验和 gate 固化为命令流程 |
| 旧版本文档策略未定义 | 旧版本内容默认冻结，维护/安全修复允许受控自动化 |
| 文档覆盖无法机器判断 | manifest 记录页面清单、输入文件和覆盖摘要 |

## 6. 异常流程

| 异常 | 处理 |
|---|---|
| 缺少 `release.json` | 文档生成阻断，提示先完成 `/release-propose` 或 `/release-prepare` 前置输入。 |
| 用户未确认是否需要产品文档 | 不生成新版本产品文档，记录 `pending_confirmation` blocker。 |
| 用户确认不需要产品文档 | 不创建空 `usage-docs/` 版本目录，记录 skipped rationale。 |
| 缺少上一版本 usage-docs | 使用模板生成首版文档，并在 manifest 中记录 `source_version: null`。 |
| Mintlify 导航缺少当前版本页面 | `usage-docs-validate` 阻断，并输出缺失页面。 |
| 文档包含敏感信息 | 发布门禁阻断，要求移除或改写公开文档。 |
| 管理端菜单或小程序页面缺少文档覆盖 | 记录 blocker 或要求明确豁免理由。 |
| 旧版本内容性文档被自动化改写 | 校验阻断，要求明确授权并补充留痕。 |
| `/docs` 子路径部署不可用 | 发布材料记录部署 blocker 或改用确认过的子域名/反向代理方案。 |
