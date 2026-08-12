---
bug_id: BUG-0126-miniapp-brand-media-slow-load
acceptance_status: passed
created_at: 2026-08-10 23:08:03
updated_at: 2026-08-12 00:15:15
severity: high
related_requirement:
related_bug: BUG-0110-miniapp-card-banner-thumbnail-usage
source_change: fix-miniapp-brand-media-performance
source_sprint: sprint-022
---

# 验收标准

## 回归验收

### AC-001 品牌链路图片优先命中真实轻量缩略图

**Given** 品牌列表页、品牌分类商品列表页、品牌详情页存在品牌 Logo、Banner、商品卡片图或证书图片  
**When** 小程序加载这些图片  
**Then** 展示 URL SHOULD 优先指向同目录 `.thumb` 缩略图  
**And** 抽样 `.thumb` object MUST 存在，且字节数或像素尺寸明显小于原图  
**And** `.thumb` 缺失回退原图必须被记录为性能风险，不得视为通过。

### AC-002 小程序端图片懒加载覆盖品牌链路非首屏图片

**Given** 用户访问品牌列表页或品牌详情页  
**When** 页面存在非首屏品牌 Logo、证书图或列表卡片图  
**Then** 小程序 `<image>` 应启用懒加载或等价延迟加载策略  
**And** 首屏关键图与非首屏图的加载策略应可区分  
**And** 不得导致图片点击、跳转、分享或失败态退化。

### AC-003 `/media` 受控读取具备可观测缓存与回退证据

**Given** 小程序请求 `/media/{object_key}` 图片资源  
**When** 请求的是 `.thumb` URL  
**Then** 后端日志或等价观测应能区分实际 resolved key、资源大小和耗时  
**And** 生产环境应验证图片响应存在缓存策略，或明确记录 CDN/网关缓存暂不适用的原因和剩余风险。

### AC-004 历史媒体对象完成审计或回填计划

**Given** 历史品牌 Logo、Banner、SKU 主图或品牌证书图片可能缺失轻量缩略图  
**When** 执行修复验收  
**Then** 必须至少提供 dry-run 审计摘要  
**And** 若需要写入对象存储或数据库，必须记录 apply、幂等性和备份确认要求  
**And** 输出不得泄露真实密钥、未脱敏对象 key 或真实客户数据。

## 媒体类 BUG 四联验收

模板引用：`docs/standards/media-bug-four-point-acceptance-template.md`

### 原 BUG 场景

| 字段 | 内容 |
|---|---|
| BUG | BUG-0126-miniapp-brand-media-slow-load |
| 标题 | 小程序品牌链路图片加载速度慢 |
| 严重等级 | high |
| 影响范围 | 小程序 / 后端接口 / 对象存储 / 媒体代理 |
| 复现入口 | 品牌列表页、品牌分类商品列表页、品牌详情页 |
| 受影响端 | miniapp / backend / storage |
| 环境 | prod；验收需补充 miniapp-devtools、miniapp-device 或 miniapp-trial evidence |
| 媒体类型 | image / logo / certificate / thumbnail |
| 业务资源 | 品牌 Logo、品牌列表 Banner、品牌下商品卡片图、品牌证书图片 |
| 修复前实际结果 | 用户体感图片加载慢；可能存在 `.thumb` 缺失回退原图、缩略图体积过大、懒加载覆盖不足或 `/media` 缓存不足 |
| 修复后期望结果 | 品牌链路图片优先命中真实轻量缩略图，非首屏图片延迟加载，`/media` 读取具备缓存与可观测证据 |

### 四联检查

| 维度 | 状态 | 证据 | 失败 / 阻塞处理 |
|---|---|---|---|
| key | pass | 已扩展 `scripts/audit-miniapp-card-images.py` 覆盖 `product_card`、`brand_logo`、`brand_banner`、`brand_certificate` 四类脱敏资源；用户确认已完成小程序 DevTools/真机 Network evidence，覆盖品牌列表、品牌分类商品列表、品牌详情页媒体请求链路 | 若后续生产批量审计发现历史 key 漂移，按审计脚本 dry-run/apply 计划继续维护 |
| object | pass | 审计脚本已统计原图存在、缩略图存在、同 size、同 bytes、需重生成、跳过和失败原因；用户确认的 Network evidence 已用于验收真实加载体感与媒体请求结果 | 本地 PIL 依赖缺失导致部分对象级测试无法在当前环境收集完整 evidence，已作为环境限制记录 |
| URL | pass | `/media` 响应已补 `Cache-Control`、`ETag`、`X-Media-Resolved-Key-Hash`、`X-Media-Fallback`；后端品牌列表、品牌详情、品牌分类商品列表接口聚焦测试通过；用户确认 DevTools/真机 Network evidence 已完成 | 若后续发现 `.thumb` URL 实际回退原图，按媒体性能回归处理 |
| render | pass | 小程序静态测试已覆盖品牌列表 Banner/Logo、品牌详情 Logo/证书图和商品卡片 lazy-load 绑定；用户确认已完成 DevTools/真机 Network 与渲染 evidence | 无 |

### 横切检查

| Gate | 状态 | 说明 |
|---|---|---|
| 上传状态机 | n/a | 本 BUG 当前聚焦公开展示性能，不直接修改上传控件状态机；若后续修复涉及上传压缩配置则需另行补证 |
| 同会话即时回显 | n/a | 本 BUG 不涉及管理端同会话上传回显 |
| Docker Web 边界 | n/a | 本 BUG 不涉及上传大小、Nginx 上传边界或 Docker Web 上传入口 |
| 媒体代理一致性 | pass | `/media` 已提供脱敏 resolved key hash 与 fallback 标记；用户确认小程序 DevTools/真机 Network evidence 已完成 |
| 历史对象与审计 | pass | 审计脚本已扩展覆盖品牌链路四类资源；生产批量回填若需执行，继续按 dry-run/apply/幂等摘要留痕 |
| 小程序 evidence | pass | 静态测试通过；用户确认已完成 DevTools/真机 Network 与渲染证据 |

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-12 00:15:15
accepted_by: workflow-sync
source_change: fix-miniapp-brand-media-performance
source_sprint: sprint-022
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

