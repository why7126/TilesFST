---
title: 业务流程
purpose: REQ-0039 XL 管理端页面分层验收模板业务流程
content: 模板创建、引用、验收与复盘闭环
source: requirement.md
owner: product
status: done
created_at: 2026-07-16 09:06:14
updated_at: 2026-07-16 09:37:04
---

# 业务流程

## 1. 主流程

```text
REQ-0039 文档完善
  |
  v
评审确认模板边界
  |
  v
OpenSpec Change 实现模板沉淀
  |
  +--> docs/standards/ 中形成长期模板文档
  |
  +--> 后续复杂管理端页面引用模板
          |
          v
      按层判定 gate required / N/A
          |
          v
      DB / API / 上传 / Orval / Web / Docker / UI 分层验收
          |
          v
      验收证据写入 acceptance / trace / report
          |
          v
      Sprint 复盘沉淀新横切问题
```

## 2. 模板引用流程

```text
新 XL 管理端页面 REQ
  |
  v
是否命中复杂页面？
  |
  +-- 否 --> 常规 REQ 验收
  |
  +-- 是 --> 引用 REQ-0039 模板
              |
              v
          逐层判断适用性
              |
              +-- DB/API/上传等不适用 --> 写 N/A 理由
              |
              +-- 适用 --> 写检查项、owner、证据类型
              |
              v
          后续 OpenSpec tasks 按层拆分
```

## 3. 与父 REQ 差异

本 REQ 暂无父需求。它不是某个管理端页面的功能细化，而是从 `REQ-0038` 品牌证书全链路交付和 sprint-007 复盘中抽象出的横切治理需求。

| 对比项 | REQ-0039 | 具体管理端页面 REQ |
|---|---|---|
| 交付物 | 分层验收模板 | 页面、接口、数据、上传或交互能力 |
| 是否改源码 | 不直接修改 | 视具体 Change 而定 |
| 是否运行 Orval | 不直接运行 | API contract 变化时必须运行 |
| 是否 Docker 验证 | 不直接验证 | 上传、代理、Nginx、compose 变化时必须验证 |
| 验收重点 | gate 结构、N/A 判定、证据格式、横切 AC | 页面功能和实际链路 |

## 4. 异常流程

| 场景 | 处理 |
|---|---|
| 后续页面只改纯文案或轻量 UI | 可引用模板并将 DB/API/上传/Orval/Docker 标记 N/A。 |
| 后续页面新增上传控件 | 上传 gate 与 Docker `localhost:3000` 边界验收必须从 N/A 改为 required。 |
| 后续页面新增 API 字段 | API gate 与 Orval gate 必须 required，并同步接口文档与测试。 |
| 后续页面发现模板缺项 | 在对应 Change trace 中记录缺口，并在 Sprint 复盘或后续治理 REQ 中更新模板。 |
