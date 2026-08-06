---
bug_id: BUG-0117-miniapp-privacy-clipboard-phone-drift
acceptance_status: passed
created_at: 2026-08-05 09:43:30
updated_at: 2026-08-06 08:23:35
source_change: fix-miniapp-privacy-interface-drift
source_sprint: sprint-020
---

# Acceptance

## 回归验收项

### AC-001 小程序提交包不含电话与剪贴板隐私接口

- [x] `src/miniapp` 的 `.ts` 与运行 `.js` 文件中不再出现 `wx.makePhoneCall`。
- [x] `src/miniapp` 的 `.ts` 与运行 `.js` 文件中不再出现 `wx.setClipboardData`。
- [x] 静态测试覆盖小程序提交包不含电话和剪贴板隐私接口。

### AC-002 门店服务不再返回电话或复制微信号动作

- [x] `GET /api/v1/miniapp/home` 的 `services[].action_type` 不再返回 `phone`。
- [x] `GET /api/v1/miniapp/home` 的 `services[].action_type` 不再返回 `copy_wechat`。
- [x] 后端 Schema 移除或拒绝电话/复制微信号动作口径。
- [x] 后端测试覆盖 `miniapp.contact_phone` 或 `miniapp.contact_wechat` 配置存在时也不会暴露电话/剪贴板动作。

### AC-003 证书详情文件失败兜底不再复制 URL

- [x] 证书详情页 PDF/文件下载失败时展示稳定错误提示。
- [x] 证书详情页 `wx.openDocument` 失败时展示稳定错误提示。
- [x] 失败路径不调用剪贴板，不展示“文件链接已复制”。
- [x] 证书详情相关文档和测试删除复制文件链接兜底口径。

### AC-004 文档与规格口径一致

- [x] OpenSpec 删除电话、复制微信号、复制证书文件链接作为用户能力的描述。
- [x] `src/miniapp/README.md` 删除“失败时复制后端受控 URL 作为兜底”。
- [x] `docs/03-api-index.md` 更新 `GET /api/v1/miniapp/home` 示例，不再展示 `copy_wechat`。
- [x] 相关测试与验收记录使用“无电话、无剪贴板隐私接口”的目标口径。

### AC-005 小程序提审隐私声明可通过

- [x] 使用修复后的代码包完成本地静态预检，未发现电话或剪贴板隐私接口调用。
- [x] 选择“未采集用户隐私”的代码侧前置条件已满足：提交包不含 `wx.makePhoneCall` / `wx.setClipboardData`。
- [x] 若微信平台仍提示隐私接口，记录剩余接口清单并作为独立后续问题处理。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-06 08:23:35
accepted_by: workflow-sync
source_change: fix-miniapp-privacy-interface-drift
source_sprint: sprint-020
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

