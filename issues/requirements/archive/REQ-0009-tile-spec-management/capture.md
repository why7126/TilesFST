---
req_id: REQ-0009-tile-spec-management
status: captured
created_at: 2026-06-27 08:58:09
updated_at: 2026-06-27 08:58:09
recorded_by: product
source: 反馈
priority_hint: P1
parent_requirement:
---

# 一句话

管理后台新增瓷砖规格页，支持规格主数据的查看与编辑；左侧导航在「瓷砖类目」下新增「瓷砖规格」入口。

# 原始描述

新增一下瓷砖规格页，支持编辑瓷砖规格，左侧导航栏在瓷砖类目下新增瓷砖规格。

# 背景与关联

- 当前 SKU 表单中「规格尺寸」为自由文本输入（`TileSkuFormModal` → `size` 字段），尚无独立规格主数据管理页。
- 左侧导航现状（`admin-nav.ts` OPERATIONS）：首页 → 瓷砖 SKU → 瓷砖品牌 → 瓷砖类目 → Banner 管理。
- 关联能力：瓷砖类目（`REQ-0005-tile-category-management`）、瓷砖 SKU（`REQ-0006-tile-sku-management`）。

# 待澄清

- [ ] 规格数据模型：仅尺寸（如 `800×800mm`）还是含厚度、单位、排序、启停等字段？
- [ ] 与 SKU 的关联方式：下拉选择规格主数据 vs 继续自由文本 vs 两者并存？
- [ ] 列表页交互：对齐品牌/类目管理（检索、分页、启停、条件删除）还是更轻量？
- [ ] 导航结构：「瓷砖类目下」是同级菜单项（紧跟类目）还是折叠子菜单？
- [ ] 权限边界：与现有管理端 RBAC 角色是否一致（admin / employee / readonly）？

# 探索结论

（/req-explore 后人工确认写入）
