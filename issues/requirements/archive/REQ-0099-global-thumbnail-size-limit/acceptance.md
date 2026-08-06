---
requirement_id: REQ-0099-global-thumbnail-size-limit
acceptance_status: passed
created_at: 2026-08-05 09:44:12
updated_at: 2026-08-06 08:23:35
owner: product
source: requirement.md
---

# 验收标准

## 功能 AC

- [ ] AC-001 系统设置 media 分组返回缩略图体积目标上限字段，默认值表示“不限制”，且不改变现有图片、视频、文件大小限制字段。
- [ ] AC-002 管理后台“系统设置 - 媒体与存储”展示缩略图体积目标上限配置，字段文案说明 `0` 表示不限制、仅对新生成缩略图生效、历史需维护任务重生成。
- [ ] AC-003 管理员可保存有效上限值，例如 `20KB`，保存后设置立即影响后续新生成缩略图。
- [ ] AC-004 管理员输入非法值时，后端返回明确校验错误，前端在字段或设置表单中展示错误，不静默失败。
- [ ] AC-005 默认不限制时，现有缩略图生成尺寸、质量、格式和 `.thumb` Key / URL 行为保持兼容。
- [ ] AC-006 配置目标上限后，SKU 图片、品牌 Logo、Banner 图片和品牌证书图片新上传生成缩略图时均读取同一全局策略。
- [ ] AC-007 SKU 暂存图片正式化时，如需补生成缩略图，必须读取同一全局策略。
- [ ] AC-008 缩略图对象继续使用同目录 `.thumb` 命名，系统不得要求新增业务表 `thumbnail_key` 字段或改变前端现有缩略图 URL 规则。
- [ ] AC-009 当 JPEG / WebP 示例图片超过目标体积时，系统通过质量递减或尺寸收缩等策略尽量压缩到目标附近或低于目标。
- [ ] AC-010 当复杂 PNG、透明图或高细节图片无法达到目标上限时，原图上传和业务保存不得失败，并应记录 warning 或可复核失败原因。
- [ ] AC-011 管理后台保存缩略图体积上限时，不得自动批量扫描、读取或覆盖历史 `.thumb` 对象。
- [ ] AC-012 历史缩略图应用新策略必须通过维护任务执行，维护任务 dry-run 输出候选数量、跳过原因、失败原因和预计写入摘要。
- [ ] AC-013 维护任务 apply 输出成功、失败、跳过和重试候选摘要，并支持二次审计。
- [ ] AC-014 系统设置字段变化同步 OpenAPI、Orval、前端类型和相关测试。
- [ ] AC-015 小程序和店主 Web 不新增配置入口，但可继续通过既有 `/media/...` 受控路径读取后续更轻量缩略图。

## 非功能 AC

- [ ] AC-NF-001 缩略图体积控制不得绕过上传鉴权、MIME 校验、对象存储适配层或 `/media/...` 受控读取链路。
- [ ] AC-NF-002 配置保存和维护任务输出不得包含真实密钥、真实客户数据、Authorization header、Cookie、真实 `.env` 内容或本机敏感路径。
- [ ] AC-NF-003 历史维护任务应具备幂等性；重复 dry-run 或重复 apply 不应造成重复对象、错误计数漂移或不可解释覆盖。
- [ ] AC-NF-004 缩略图压缩策略应避免无边界循环，必须有质量、尺寸或尝试次数下限。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-form-page-consistency.md`、`docs/knowledge-base/best-practices/admin-media-upload-chain.md` — 预防 Sprint 002/003 复发类缺陷

- [ ] AC-XCUT-001 管理后台系统设置页全页仅保留 1 个“保存设置”或等价保存按钮；不得在页头和表单 footer 重复渲染保存 CTA。
- [ ] AC-XCUT-002 恢复默认、dirty Tab 切换或放弃未保存修改必须使用 DS confirm modal；测试需确认未调用 `window.confirm` / `window.alert`。
- [ ] AC-XCUT-003 保存成功或失败反馈使用 fixed toast 或既有固定反馈区域，不得在设置表单上方插入会造成 `settings-layout` 垂直位移的文档流提示块。
- [ ] AC-XCUT-004 设置页在 1440x1024 视口下与现有 SystemSettingsPage 结构一致，新增字段不得破坏媒体与存储 Tab 的 footer 保存、重置和只读对象存储策略布局。
- [ ] AC-XCUT-005 图片上传链路保持 `idle -> uploading -> done/failed` 状态机；本需求不新增上传控件，N/A — 若实现未触碰上传 UI，需在验收记录中说明复用既有控件且未改变状态机。
- [ ] AC-XCUT-006 新上传图片同一会话内仍能即时回显缩略图或原图 URL；若缩略图未达标或生成失败，控件内错误或日志可定位，不能只依赖全局 toast。
- [ ] AC-XCUT-007 涉及上传大小、Nginx 或 Docker Web 边界时，必须经 `http://localhost:3000` 用户入口验证，不能只调用后端 `:8000`。
- [ ] AC-XCUT-008 缩略图生成或维护验收必须同时记录脱敏 object_key、对象存在性、`/media/...` URL 可读性和用户可见表现；历史重生成还需记录 dry-run、apply 和二次审计摘要。


## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-06 08:23:35
accepted_by: workflow-sync
source_change: update-global-thumbnail-size-limit
source_sprint: sprint-020
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

