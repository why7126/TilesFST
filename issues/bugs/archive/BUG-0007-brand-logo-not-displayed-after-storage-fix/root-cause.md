---
bug_id: BUG-0007-brand-logo-not-displayed-after-storage-fix
status: in_sprint
created_at: 2026-06-26 15:17:41
---

# 根因分析

## 1. 直接原因

对象存储写入链路修复后，品牌 Logo 的展示链路仍未闭环：

- 品牌列表页依赖品牌数据中的 Logo 可访问 URL 或对象 key 渲染图片。
- 品牌编辑弹窗依赖同一字段回显已上传 Logo。
- 当前表现为两个页面都无法显示图片，说明问题大概率不在单个前端组件空态，而在媒体访问 URL、对象 key 兼容、后端受控读取或品牌接口返回字段之间。

## 2. 根本原因

初步判断为 **媒体存储写入修复与品牌 Logo 展示读取链路未同步完成**。

对象存储问题修复后，上传对象可能已经进入 MinIO，但品牌展示仍可能存在以下断点：

| 断点 | 说明 |
|---|---|
| URL 生成 | 品牌接口返回的 `logo_url` 可能仍指向旧的本地 `/media/{object_key}` 策略，或生成的 URL 浏览器不可访问。 |
| 受控读取 | `/media/{object_key}` 若未改为从 MinIO 读取对象，会导致对象已在 MinIO 中但页面请求不到。 |
| 对象 key 兼容 | 历史数据中的 `logo_object_key` 可能对应本地文件路径或旧前缀，修复后未做兼容或迁移。 |
| 前端绑定 | 品牌列表页和编辑弹窗可能没有使用修复后的可访问 URL 字段，或错误回退到空态。 |
| 缓存/旧数据 | 已上传品牌记录可能保留旧 URL/key，需要刷新、重新保存或迁移后才可显示。 |

## 3. 触发条件

1. 对象存储上传链路修复完成。
2. 品牌记录存在 `logo_object_key` 或已上传 Logo。
3. 进入 `/admin/brands` 或打开品牌编辑弹窗。
4. 页面尝试加载 Logo 图片。

## 4. 分类

| 维度 | 分类 |
|---|---|
| 缺陷类型 | code / integration |
| 子系统 | media-access / brand-management / web-admin |
| 主要风险 | 对象存储写入与读取展示策略不一致 |
| 相关规范 | `rules/object-storage.md`、`rules/media.md` |

## 5. 待验证项

- 品牌列表接口返回的 `logo_url` 是否为空或不可访问。
- `logo_object_key` 是否指向 MinIO 中实际存在的对象。
- 浏览器访问 `logo_url` 时的 HTTP 状态码与响应内容。
- `/media/{object_key}` 是否已支持从 MinIO 读取对象。
- 新上传 Logo 与历史 Logo 是否表现一致。
