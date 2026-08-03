---
change_id: update-miniapp-brand-list-ui-interaction-optimization
status: proposed
change_type: update
created_at: 2026-07-31 15:20:01
updated_at: 2026-07-31 21:19:20
source_requirement: REQ-0086-miniapp-brand-list-ui-interaction-optimization
sprint: sprint-015
related_requirements:
  - REQ-0060-brand-list-page
  - REQ-0083-miniapp-brand-list-category-summary
owner: product
---

# Change Trace

## 来源

- REQ：`issues/requirements/archive/REQ-0086-miniapp-brand-list-ui-interaction-optimization/`
- 父需求：`REQ-0060-brand-list-page`
- 相关需求：`REQ-0083-miniapp-brand-list-category-summary`
- 原型：`issues/requirements/archive/REQ-0086-miniapp-brand-list-ui-interaction-optimization/prototype/miniapp/prototype.html`

## 影响分析

```yaml
impact:
  backend: conditional
  web: false
  miniapp: true
  admin: false
  database: false
  storage: false
  api: conditional
capabilities:
  new: []
  modified:
    - miniapp-brand-list-page
change_type: update
readiness: ready
```

## 原型与验收冲突报告

| 项 | 结论 |
|---|---|
| prototype/miniapp/prototype.html | 作为最高优先级视觉与交互参考。 |
| prototype.png | 待后续导出，不阻塞本 Change 创建。 |
| acceptance.md | 已覆盖功能、数据、UI、导航设备、埋点、文档原型。 |
| rules/ui-design.md | 提供暗色旗舰风和品牌金原则；页面细节以原型优先。 |
| openspec/specs | 已有品牌列表页能力，本 Change 以 update 方式补充。 |

## PNG / Evidence Checklist

- [ ] 后续从 HTML 或设计稿导出 `prototype.png`，或在验收中说明使用附件截图替代。
- [ ] DevTools evidence 覆盖 320、375、390、430 pt。
- [ ] 真机 evidence 不可用时标记 `blocked` 或 `follow_up`。
- [ ] evidence 不包含本机绝对路径、密钥、token、Cookie、Authorization header 或真实客户数据。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-31 21:19:20 | `/opsx-modify` | 验收返修：将品牌列表页类目胶囊字号调整为 `30rpx`，比品牌名称 `32rpx` 小 `2rpx`；同步测试、README、验收与 delta spec。 |
| 2026-07-31 20:57:00 | `/opsx-modify` | 验收返修：移除品牌矩阵右侧“按类目快速识别”和类目区“全部类目 · 点击查看该品牌下的类目商品”说明文案；同步实现、测试、README、验收与 delta spec。 |
| 2026-07-31 15:25:37 | `/sprint-propose` | 纳入 `sprint-015` 正式范围 |
| 2026-07-31 15:20:01 | `/req-opsx` | 由 REQ-0086 创建 OpenSpec Change，状态 proposed |
