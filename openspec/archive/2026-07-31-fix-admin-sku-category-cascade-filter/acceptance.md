## Acceptance

## AC-001 类目筛选展示各层级类目

- GIVEN 管理后台存在一级、二级、三级或更深层级瓷砖类目
- WHEN 管理员打开「瓷砖 SKU」页面并操作类目筛选
- THEN 级联选择控件 MUST 可选择当前类目树中的各层级类目

## AC-002 父类目包含子孙 SKU

- GIVEN 某父类目下存在多个子孙类目并分别绑定 SKU
- WHEN 管理员选择该父类目筛选
- THEN SKU 列表 MUST 返回该父类目自身及所有子孙类目的 SKU
- AND 不得只返回直接归属该父类目自身的 SKU

## AC-003 子类目筛选准确

- GIVEN 某二级或更深层级类目绑定 SKU
- WHEN 管理员选择该子类目筛选
- THEN SKU 列表 MUST 只返回该子树范围内的 SKU

## AC-004 组合筛选不回归

- GIVEN 管理员同时设置关键词、品牌、类目、状态或素材完整度筛选
- WHEN SKU 列表刷新
- THEN 各筛选条件 MUST 按 AND 语义组合生效
- AND 分页与默认排序 MUST 保持稳定

## AC-005 重置能力保留

- GIVEN 管理员已选择任意层级类目
- WHEN 点击重置或清空级联选择
- THEN 类目筛选 MUST 回到「全部类目」
- AND SKU 列表 MUST 恢复对应的未限制类目结果

## AC-006 不影响 SKU 维护

- GIVEN 级联筛选修复完成
- WHEN 管理员新增、编辑、上下架或删除 SKU
- THEN 原有 SKU 管理流程、权限边界、素材展示和表单类目选择 MUST 不回归
