---
requirement_id: REQ-0066-admin-sku-image-removal-main-image-rules
title: 管理端 SKU 编辑弹窗商品图片移除与主图规则业务流程
status: done
owner: product
source: requirement.md
created_at: 2026-07-22 09:19:53
updated_at: 2026-07-22 10:13:18
---

# REQ-0066 业务流程

## 1. 总流程

```text
后台运营进入 SKU 管理列表
  ↓
点击某条 SKU 的「编辑」
  ↓
GET /api/v1/admin/tile-skus/{id}
  ↓
弹窗回填商品图片 images[]
  ↓
运营执行：添加图片 / 设为主图 / 移除图片
  ↓
前端即时重算 images[]：唯一主图 + 连续 sort_order
  ↓
PUT /api/v1/admin/tile-skus/{id}
  ↓
保存成功 → Toast → 列表刷新
  ↓
再次打开弹窗，图片顺序与主图状态一致
```

## 2. 设置主图流程

```text
用户点击第 N 张图片「设为主图」
  ↓
前端将第 N 张图片标记 is_main=true
  ↓
前端将该图片移动到 images[0]
  ↓
其他图片 is_main=false
  ↓
重新计算 sort_order = 0..N
  ↓
弹窗即时显示第一张图片带「主图」标签
```

## 3. 移除非主图流程

```text
用户点击非主图图片的移除入口
  ↓
从 images[] 中移除该图片
  ↓
现有主图保持 is_main=true
  ↓
主图继续位于第一位
  ↓
重新计算剩余图片 sort_order
```

## 4. 移除当前主图流程

```text
用户点击当前主图的移除入口
  ↓
记录移除前主图 index
  ↓
从 images[] 中移除主图
  ↓
是否仍有图片？
  ├─ 否 → images=[]，无 is_main，允许草稿缺图状态
  └─ 是
      ↓
      移除前主图后一张是否存在？
      ├─ 是 → 后一张成为新主图
      └─ 否 → 移除后列表第一张成为新主图
      ↓
      新主图移动/保持到 images[0]
      ↓
      重新计算 sort_order
```

## 5. 保存与回填流程

```text
弹窗内 images[] 最终态
  ↓
buildPayload()
  ↓
提交 images: [{ object_key, url, is_main, sort_order }]
  ↓
后端 replace_images(tile_id, normalize_images(images))
  ↓
GET SKU detail
  ↓
按 sort_order 回填图片，主图唯一
```

## 6. 与父需求差异

| 项 | REQ-0006 原能力 | REQ-0066 补强 |
|---|---|---|
| 多图上传 | 支持 | 不改变 |
| 指定主图 | 支持 | 指定后主图必须前置 |
| 删除图片 | 明确删除非主图 | 扩展到可移除任意图片 |
| 删除主图 | 未定义 | 定义兜底主图规则 |
| 对象存储物理删除 | 未定义 | 本期不做物理删除，仅解除 SKU 关联 |

## 7. 异常与边界

| 场景 | 处理 |
|---|---|
| 移除最后一张图片 | 图片列表为空；允许草稿保存；正式上架沿用既有校验 |
| 图片上传失败 | 保持上传控件内错误提示，不改变现有图片列表 |
| 保存失败 | 保留弹窗当前编辑态，展示服务端错误 |
| 只读账号 | 不展示写操作入口 |
| 重复点击移除 | 实现阶段需保证状态幂等，不产生脏 payload |
