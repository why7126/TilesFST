---
bug_id: BUG-0090-admin-sku-list-publish-sort-order
status: done
created_at: 2026-07-30 23:11:20
updated_at: 2026-07-31 00:18:16
---

# 验收标准

## AC-001 已发布 SKU 按发布时间降序

- GIVEN 管理端存在多条 `PUBLISHED` SKU
- AND 这些 SKU 的 `published_at` 不同
- WHEN 用户进入 Web 管理端 SKU 列表
- THEN 已发布 SKU 应按 `published_at` 从新到旧展示
- AND 不应因 `updated_at` 更晚而排到发布时间更新的 SKU 前面

## AC-002 未发布 SKU 按创建时间降序

- GIVEN 管理端存在多条未发布 SKU
- AND 这些 SKU 的 `created_at` 不同
- AND 部分 SKU 的 `updated_at` 晚于其他 SKU
- WHEN 用户进入 Web 管理端 SKU 列表
- THEN 未发布 SKU 应按 `created_at` 从新到旧展示
- AND 不应因最近编辑导致草稿顺序覆盖创建顺序

## AC-003 混排规则明确且稳定

- GIVEN 同一列表结果中同时包含已发布 SKU 和未发布 SKU
- WHEN 用户查看默认列表
- THEN 已发布与未发布 SKU 的分组先后规则必须在修复方案中明确
- AND 每个分组内分别遵循 `published_at DESC` 或 `created_at DESC`
- AND 主排序时间相同或为空时应使用稳定兜底排序，避免刷新、翻页或重复请求后顺序跳动

## AC-004 搜索、筛选和分页保持同一排序契约

- GIVEN 用户使用关键词、品牌、类目、状态或素材完整度筛选 SKU
- WHEN 列表返回筛选结果并分页展示
- THEN 结果仍应遵循同一默认排序策略
- AND 翻页不应出现重复、漏项或跨页顺序反复变化

## AC-005 操作行为不受影响

- GIVEN 本 BUG 修复上线后
- WHEN 用户新增、编辑、上架、下架或删除 SKU
- THEN 原有操作权限、校验、接口响应结构和错误码不应因排序修复发生非预期变化
- AND 上架动作仍应正确写入或更新 `published_at`

## AC-006 回归测试覆盖

- SHOULD 覆盖后端 SKU 列表查询排序测试。
- SHOULD 覆盖 Web 管理端 SKU 列表加载后的展示顺序或 API 调用契约。
- SHOULD 覆盖已发布、未发布、混排、时间相同、发布时间为空、搜索筛选和分页场景。
