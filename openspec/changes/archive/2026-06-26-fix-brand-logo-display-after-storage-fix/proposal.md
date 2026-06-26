# Proposal: fix-brand-logo-display-after-storage-fix

## Why

`BUG-0007-brand-logo-not-displayed-after-storage-fix` 已评审通过并纳入 `sprint-002`。对象存储写入问题（`BUG-0006`）修复后，品牌列表页和品牌编辑弹窗仍无法展示品牌 Logo。

品牌 Logo 是品牌管理核心展示字段。列表页和编辑弹窗同时不可见，说明品牌 Logo 的对象存储写入、品牌记录 `logo_object_key`、后端受控读取、品牌接口 `logo_url` 与前端渲染之间仍存在展示链路断点。

## What Changes

- 修复品牌 Logo 展示读取闭环，确保品牌列表页和品牌编辑弹窗都能显示已上传 Logo。
- 明确品牌接口返回的 `logo_url` 必须可被浏览器加载。
- 明确 `/media/{object_key}` 或等价媒体访问策略必须从 MinIO 受控读取品牌 Logo。
- 明确历史 `logo_object_key` 的兼容或迁移策略。
- 补充后端和前端回归测试，覆盖列表展示、编辑回显和上传后刷新仍可见。

## Impact

| 影响面 | 说明 |
|---|---|
| Web 管理端 | `/admin/brands` 列表和品牌编辑弹窗 Logo 展示 |
| 后端媒体访问 | 可能涉及 `/media/{object_key}` 受控读取或 URL 生成 |
| 后端品牌接口 | 可能涉及 `logo_url` 生成逻辑；若响应 schema 不变则无需 Orval |
| MinIO | 必须复用 `MINIO_BUCKET=tile-info-platform` 与标准对象前缀 |
| 历史数据 | 需判断旧 `logo_object_key` 是否可兼容读取或需要重新上传/迁移 |
| 小程序 / 店主端 | 本 change 默认不影响；如共享媒体 URL 策略，需确认兼容性 |

## Out of Scope

- 不新增多个 MinIO Bucket。
- 不开放未授权对象存储公开读。
- 不重做品牌管理列表/弹窗整体 UI。
- 不处理非品牌 Logo 的媒体展示问题，除非复用的媒体读取函数必须同步修复。

## Rollback Plan

1. 回滚品牌 Logo URL 生成或媒体读取策略相关代码。
2. 保留对象存储写入链路（`BUG-0006`）已修复能力，不回退到本地 `UPLOAD_DIR` 写入。
3. 若引入历史数据迁移，迁移脚本必须可重复执行或有回滚说明。
4. 回滚后重新标记 `BUG-0007` 未修复，并保留验收失败记录。
