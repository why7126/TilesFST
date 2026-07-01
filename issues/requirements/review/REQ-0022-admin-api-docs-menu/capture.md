---
req_id: REQ-0022-admin-api-docs-menu
status: captured
created_at: 2026-06-30 21:57:46
updated_at: 2026-06-30 21:57:46
recorded_by: product
source: 用户反馈
priority_hint: P1
parent_requirement: REQ-0017-system-settings
captured_via: capture
classification_rationale: 在系统设置下方新增接口文档菜单并允许后台管理员查看全部接口，属于管理端新增导航与文档查看能力。
---

# 一句话

在管理端系统设置下方新增「接口文档」菜单栏，支持后台管理员用户查看系统所有接口文档。

# 原始描述

在系统设置下方新增接口文档菜单栏，支持后台管理员用户查看系统所有的接口。

# 背景与关联

- 父需求：`REQ-0017-system-settings`
- 涉及端：Web 管理端
- 涉及文档/API：`docs/03-api-index.md`、FastAPI OpenAPI / Swagger UI、Orval 生成接口清单
- 目标用户：后台管理员用户
- 业务价值：让内部管理员可在管理端快速查询系统接口能力、路径、请求响应与错误码，降低联调和运维排查成本
- 权限边界：接口文档入口与页面必须仅对后台管理员可见；店主端与小程序不暴露该入口

# 待澄清

- [ ] 接口文档页面是内嵌 FastAPI Swagger UI、展示静态 `docs/03-api-index.md` 内容，还是基于 OpenAPI JSON 自渲染列表
- [ ] 「系统所有接口」是否包含仅内部维护接口、健康检查接口、上传签名/媒体接口与管理端私有接口
- [ ] 是否需要按模块、权限级别、HTTP 方法、路径关键字筛选接口
- [ ] 是否需要展示请求示例、响应示例、错误码、鉴权要求、Orval 方法名与最后更新时间
- [ ] 是否允许管理员在管理端直接跳转到 `/docs`，还是必须留在管理端 Shell 内查看
- [ ] 是否需要在生产环境隐藏或限制 Swagger Try It Out，仅提供只读文档查看

# 探索结论

（/req-explore 后人工确认写入）

# 分类说明（/capture）

该条目描述新增管理端菜单与接口文档查看能力，当前没有已交付基线可判定为偏差，因此判定为 REQ。不拆分原因：菜单入口、权限控制与接口文档展示属于同一管理端接口文档查看闭环。
