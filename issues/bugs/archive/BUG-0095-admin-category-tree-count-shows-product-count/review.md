---
bug_id: BUG-0095-admin-category-tree-count-shows-product-count
status: done
review_result: approved
reviewed_at: 2026-07-31 15:06:02
reviewer: product
created_at: 2026-07-31 15:06:02
updated_at: 2026-07-31 17:35:01
---

# 评审结论

批准修复。

管理端类目树右侧计数当前显示商品数量，与已确认的产品口径不一致：该位置应显示下一层级类目数量，“全部类目”入口应显示顶层类目数量。该问题影响管理人员理解类目层级结构，属于已交付类目管理能力的计数语义偏差。

# 评审清单

- [x] 可复现或根因充分：截图和补充验证已确认当前口径错误，后端已具备直接子类目数量字段，问题收敛到前端计数字段绑定。
- [x] 严重等级合理：`medium`，不阻断主流程，但影响高频管理端类目树判断。
- [x] 回归验收明确：已覆盖一级类目、叶子类目、多层级类目、“全部类目”和商品数量区分。
- [x] 是否需 hotfix 路径：不需要 hotfix，可进入常规 Sprint 修复。

# 批准范围

- 修正管理端类目树节点右侧计数字段，改为直接子类目数量。
- 修正“全部类目”入口右侧数字，显示顶层类目数量。
- 补充管理端类目树组件/页面测试；如接口契约或生成类型受影响，同步 API、OpenAPI、Orval 和后端接口测试。

# 后续动作

- 可执行 `/bug-opsx BUG-0095-admin-category-tree-count-shows-product-count` 创建修复 Change。
- 可纳入 Sprint 正式范围。
