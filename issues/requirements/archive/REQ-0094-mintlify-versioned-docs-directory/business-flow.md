---
requirement_id: REQ-0094-mintlify-versioned-docs-directory
title: Mintlify 多版本产品文档目录与站点浏览 - 业务流程
created_at: 2026-08-03 18:30:03
updated_at: 2026-08-03 18:35:14
owner: product
---

# 业务流程

## 1. 总体流程

```text
已发布版本 / release 快照
        |
        v
releases/vX.Y.Z/usage-docs/
        |
        | 事实源：全量 MDX + manifest
        | manifest 记录页面、截图引用、hash、覆盖和同步状态
        v
站点同步 / 投影命令
        |
        +-- 同步文档页面到 mintlify/docs/vX.Y.Z/
        +-- 同步公告页面到 mintlify/releases/vX.Y.Z/
        +-- 写入或复用 mintlify/assets/screenshots/
        +-- 更新 mintlify/mint.json
        +-- 更新 latest / stable 指针
        |
        v
Mintlify 校验
        |
        +-- 页面清单一致
        +-- 截图 hash / 复用依据一致
        +-- 导航无缺页
        +-- broken links 通过
        +-- 公开安全扫描通过
        |
        v
文档站发布或记录替代校验证据
```

## 2. release 快照到站点目录流程

```text
读取 releases/<version>/release.json
    |
    v
确认 usage_docs.status
    |
    +-- pending_confirmation
    |       |
    |       v
    |   阻断站点投影，提示先确认是否生成 / 更新 usage docs
    |
    +-- skipped
    |       |
    |       v
    |   站点可只同步公告，或生成文档不可用说明
    |
    +-- generated
            |
            v
        读取 releases/<version>/usage-docs/manifest.json
            |
            v
        校验 release 快照页面完整性
            |
            v
        投影到 mintlify/docs/<version>/
            |
            v
        处理截图资产引用
            |
            +-- hash 已存在且复用规则通过：引用共享资产
            +-- hash 不存在：写入 mintlify/assets/screenshots/
            +-- UI 语义变化：阻断复用，要求新截图
            |
            v
        更新 mintlify/mint.json 和 latest 指针
```

## 3. 共享截图资产流程

```text
页面需要截图
    |
    v
计算截图内容 hash
    |
    +-- mintlify/assets/screenshots/ 已存在同 hash
    |       |
    |       v
    |   判断版本适用性
    |       |
    |       +-- 界面 / 字段 / 流程 / 权限未变化：复用并记录 reuse_reason
    |       +-- 存在语义变化：新增截图并阻断复用
    |
    +-- 不存在同 hash
            |
            v
        写入 sha256-<hash>-<semantic-name>.png
            |
            v
        manifest 记录 first_used_in、covered_pages、source_type
```

## 4. latest 指针流程

```text
发布或同步某版本
    |
    v
判断该版本 usage docs 是否 generated 且站点校验通过
    |
    +-- 是
    |       |
    |       v
    |   latest 指向该版本
    |
    +-- 否
            |
            v
        latest 保持最近一个可用产品文档版本
            |
            v
        当前最新版本显示文档未生成或仅公告可用说明
```

## 5. 与父需求 REQ-0088 的差异

## 5. Docker Compose 文档站启动流程

```text
需要本地预览 / 演示 / 受控部署文档站
    |
    v
确认 mintlify/ 站点源目录已生成并通过校验
    |
    v
选择部署方式
    |
    +-- 外部 Mintlify / 静态托管
    |       |
    |       v
    |   release 记录外部 preview/build 或替代校验证据
    |
    +-- Docker Compose 内启动
            |
            v
        设置 HOST_PORT_MINTLIFY_DOCS 等示例变量
            |
            v
        docker compose --profile docs-site up -d mintlify
            |
            v
        校验文档站端口、导航、broken links 和公开安全
            |
            v
        release-prepare / publish 记录 Compose 验证证据
```

异常处理：

| 异常 | 处理 |
|---|---|
| 未启用 `docs-site` profile | 默认部署不启动 Mintlify 服务，业务系统仍可正常启动。 |
| 宿主机端口冲突 | 修改 `.env` 中 `HOST_PORT_MINTLIFY_DOCS`，不得修改多个文件硬编码端口。 |
| `mintlify/` 目录缺失或未校验 | Compose 文档站服务不得作为 pass 证据，需先完成站点投影和校验。 |
| 生产采用外部托管 | Compose 内 Mintlify 服务可不启用，但 release 必须记录外部托管或 preview 证据。 |

## 6. 与父需求 REQ-0088 的差异

| REQ-0088 已完成 | REQ-0094 增强 |
|---|---|
| 定义 `releases/<version>/usage-docs/` 快照和 manifest | 新增 `mintlify/` 站点源目录和多版本浏览结构 |
| `releases/mint.json` 可导航 release usage docs | `mintlify/mint.json` 成为站点配置，支持版本、latest 和公告分区 |
| 截图默认位于 release usage docs 目录 | 截图集中到 `mintlify/assets/screenshots/`，release manifest 记录引用与 hash |
| 校验当前版本 usage docs 和 Mintlify 导航 | 校验 release 快照、站点投影、共享截图复用和站点路径一致性 |
| 旧版本内容冻结和受控维护 | 历史站点目录可非内容性迁移，截图按 hash 去重 |
| 记录 `/docs` 访问边界 | 增加 Docker Compose 可选文档站服务和外部托管替代说明 |

## 7. 异常流程

| 异常 | 处理 |
|---|---|
| 新增 `mintlify/` 未更新目录规则 | 阻断实现，必须先通过 OpenSpec Change 同步目录治理。 |
| release 快照缺失 manifest | 阻断站点投影，提示先补齐 usage docs 事实源。 |
| `usage_docs.status=pending_confirmation` | 阻断站点投影，提示先完成 generate / skip 决策。 |
| 站点页面与 release manifest 清单不一致 | 校验失败，输出缺失、额外或 hash 漂移页面。 |
| 截图复用缺少 `reuse_reason` | 校验 warning 或 blocker，要求补齐版本适用性说明。 |
| 页面语义变化但复用旧截图 | 校验 blocker，要求重新截图或记录明确豁免。 |
| `latest` 指向未校验版本 | 校验 blocker，保持上一可用版本或改为不可用说明。 |
| 公开文档包含敏感信息 | 发布门禁阻断，必须移除或脱敏。 |
| 历史版本内容被站点同步改写 | 校验 blocker，要求明确授权和 manifest 留痕。 |
| Compose 文档站服务暴露内部文档 | 校验 blocker，必须从 `mintlify/` 导航和公开安全扫描中移除。 |
