---
requirement_id: REQ-0081-release-image-build-governance
title: 发布镜像准备与构建治理 - 业务流程
status: done
created_at: 2026-07-29 10:07:04
updated_at: 2026-07-29 18:35:04
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
        | 校验发布门禁，判断 image_required
        v
  image_required?
      |                         |
      | no                      | yes
      v                         v
记录 image rationale      /image-prepare <version>
      |                         |
      |                         | 生成 image-build-plan.json
      |                         v
      |                   需要真实镜像产物?
      |                         |
      |                         | yes
      |                         v
      |                   /image-build <version>
      |                         |
      |                         | 生成 image-manifest.json + tar.gz + sha256
      |                         v
      +-------------------------+
        |
        v
/release-publish <version>
        |
        | 校验 release gates + image plan/manifest
        v
发布确认或阻断
```

## 2. `/image-prepare` 流程

```text
读取 release.json
    |
    v
解析版本 / scope / impact_scope
    |
    v
扫描构建输入清单
    |
    +-- Dockerfile
    +-- docker-compose*.yml
    +-- scripts/build-images.sh
    +-- scripts/build-images.env.example
    +-- src/web/nginx.conf.template
    +-- schema.sql / schema.mysql.sql
    +-- migration scripts
    |
    v
校验版本与 tag 一致性
    |
    v
生成 input_hashes 与 blockers
    |
    v
写入 releases/<version>/image-build-plan.json
```

## 3. `/image-build` 流程

```text
读取 image-build-plan.json
    |
    v
校验 plan 未过期
    |
    v
执行 scripts/build-images.sh
    |
    +-- 构建 backend image
    +-- 构建 web image
    +-- 验证平台
    +-- 验证 backend 依赖
    +-- 验证 Web Nginx
    +-- 导出 tar.gz
    +-- 生成 sha256
    |
    v
写入 releases/<version>/image-manifest.json
```

## 4. 与已有发布流程的差异

| 现状 | 新流程 |
|---|---|
| `/release-prepare` 只汇总发布门禁，镜像构建证据不成体系 | `/release-prepare` 识别 image_required，并引用 image plan / manifest |
| 镜像构建 env、脚本、Dockerfile、schema 变化依赖人工记忆 | `/image-prepare` 固化输入清单与 hash |
| `/image-build` 可能直接按本地 env 构建 | `/image-build` 必须基于已通过的 image-build-plan |
| 发布确认只看 release gates | `/release-publish` 还要校验 manifest 与当前输入一致 |

## 5. 异常流程

| 异常 | 处理 |
|---|---|
| 缺少 `release.json` | `/image-prepare` 阻断，提示先执行 `/release-propose` 或 `/release-prepare`。 |
| 缺少 `scripts/build-images.env` | `/image-prepare` 记录 blocker，提示由 example 复制并填写版本。 |
| `PRODUCT_VERSION`、`TILESFST_IMAGE_TAG`、`IMAGE_BUILD_TAG` 不一致 | `/image-prepare` 记录版本一致性 blocker。 |
| Docker 或 buildx 不可用 | `/image-build` 失败并分类为环境阻断，不写 pass evidence。 |
| manifest 生成后输入文件变化 | `/release-publish` 阻断，要求重新 `/image-prepare` 和必要的 `/image-build`。 |
| 外部构建证据由人工提供 | 发布对象必须记录证据来源、校验方式、sha256 和风险说明。 |
