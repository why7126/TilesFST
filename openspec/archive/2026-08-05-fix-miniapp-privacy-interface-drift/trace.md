---
change_id: fix-miniapp-privacy-interface-drift
source_bug: BUG-0117-miniapp-privacy-clipboard-phone-drift
status: applied
sprint: sprint-020
created_at: 2026-08-05 14:42:11
updated_at: 2026-08-05 18:02:03
---

# Change 追踪

## 来源

```yaml
bug_id: BUG-0117-miniapp-privacy-clipboard-phone-drift
bug_path: issues/bugs/archive/BUG-0117-miniapp-privacy-clipboard-phone-drift/
review_status: approved
bug_status: in_sprint
change_type: fix
sprint: sprint-020
impact:
  backend: true
  miniapp: true
  api: true
  docs: true
  tests: true
  database: false
  web_admin: false
```

## 冲突处理

- 当前产品口径确认不提供电话拨打、复制门店微信号或复制证书文件链接能力。
- 旧 `miniapp-home` 规格中的“拨打电话或复制微信号”视为历史漂移，本 Change 收敛为无电话、无剪贴板隐私接口。
- 旧证书详情文件失败“复制提示”兜底视为历史漂移，本 Change 改为稳定错误提示。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-05 18:02:03 | `/opsx-apply` | 完成任务实现、测试与校验，状态同步为 applied。 |
| 2026-08-05 14:42:11 | `/bug-opsx` | 从 BUG-0117 创建 OpenSpec Change，生成 proposal/design/specs/tasks/trace。 |
