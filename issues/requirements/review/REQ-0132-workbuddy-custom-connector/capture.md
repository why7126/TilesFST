---
req_id: REQ-0132-workbuddy-custom-connector
status: captured
created_at: 2026-09-04 16:43:52
updated_at: 2026-09-04 16:43:52
recorded_by: product
source: 用户输入
priority_hint: P1
parent_requirement:
---

# 一句话

将 ProjectTilesFST 支持为腾讯 WorkBuddy 自定义连接器，通过 MCP + Skill 暴露瓷砖业务查询与受控管理能力。

# 原始描述

用户希望将 ProjectTilesFST 支持作为腾讯 WorkBuddy 自定义连接器：

- MVP 先做 MCP + Skill 能力，覆盖 SKU 搜索、商品详情、品牌/类目查询和目录摘要。
- MVP 范围包含管理端写操作。
- 交付形态采用分阶段路线：第一阶段本地 stdio 只读 PoC；第二阶段 HTTPS 远程 MCP 服务与企业级鉴权审计。
- 后续再扩展更完整的受控写操作。

# 待澄清

- [ ] MVP 中“管理端写操作”的首批工具范围：新增/编辑 SKU、上下架、品牌/类目维护、媒体上传是否全部纳入，还是先选最小子集。
- [ ] 第一阶段本地 stdio PoC 是否严格只读，或是否需要提前提供写操作 mock / dry-run 工具。
- [ ] 第二阶段 HTTPS 远程 MCP 服务的目标部署环境、域名、TLS、凭据注入和企业使用人数。
- [ ] 连接器鉴权方式：独立 API Token、复用管理员 Bearer Token、OAuth / gateway 授权，或分阶段演进。
- [ ] WorkBuddy 写操作是否要求二次确认、幂等键、审批记录和回滚提示。

# 探索结论

前置探索建议采用“两阶段路线”：

1. 第一阶段以本地 stdio PoC 验证 WorkBuddy 调用 ProjectTilesFST 的只读工具，包括 SKU 搜索、商品详情、品牌/类目查询和目录摘要。
2. 第二阶段升级为 HTTPS 远程 MCP 服务，补齐企业级鉴权、审计、限流、请求日志、工具级权限边界，并开放管理端受控写操作。

该需求涉及 API、权限、安全、部署、请求日志、行为/任务链路观测和可能的管理端能力，应在后续 `/req-generate` 与 OpenSpec Change 中补齐 `product_data_collection_observability` 适用性声明、affected layers、N/A 原因和验证摘要。
