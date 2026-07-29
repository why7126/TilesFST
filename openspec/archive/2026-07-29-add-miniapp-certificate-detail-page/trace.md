---
change_id: add-miniapp-certificate-detail-page
change_type: add
status: proposed
created_at: 2026-07-29 08:19:01
updated_at: 2026-07-29 08:24:32
source_requirement: REQ-0080-miniapp-certificate-detail-page
source_requirement_path: issues/requirements/archive/REQ-0080-miniapp-certificate-detail-page/
iteration: sprint-013
capabilities:
  new: []
  modified:
    - miniapp-certificate-list-page
impact:
  backend: true
  web: false
  miniapp: true
  admin: false
  database: true
  storage: true
  api: true
readiness: Ready
---

# Change Trace

## 来源

- REQ：`REQ-0080-miniapp-certificate-detail-page`
- 需求路径：`issues/requirements/archive/REQ-0080-miniapp-certificate-detail-page/`
- 评审状态：approved
- 预期 Change：`add-miniapp-certificate-detail-page`

## 影响分析

```yaml
impact:
  backend: true
  web: false
  miniapp: true
  admin: false
  database: true
  storage: true
  api: true
capabilities:
  new: []
  modified:
    - miniapp-certificate-list-page
change_type: add
```

## 原型与验收冲突报告

| 来源 | 结论 |
|---|---|
| `prototype/miniapp/certificate-detail.html` | 作为布局、信息层级、状态表达参考，不要求逐像素实现 |
| `prototype/miniapp/prototype-context.md` | 明确复用商品详情页结构但删除商品交易能力 |
| `acceptance.md` | 40 条功能/UI/API/非功能 AC + 小程序导航专项 AC |
| `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` | 分享直达、返回兜底、状态栏/胶囊 reserve、页面 offset 和 evidence 必须执行 |
| `openspec/specs/miniapp-certificate-list-page/spec.md` | 旧列表卡片主点击直接预览文件；本 Change 将主点击改为进入详情页，预览下沉到详情页 |

## PNG / Evidence Checklist

- [ ] DevTools 320 pt：正常、加载、错误、无图/PDF、分享直达
- [ ] DevTools 375 pt：正常、加载、错误、无图/PDF、分享直达
- [ ] DevTools 430 pt：正常、加载、错误、无图/PDF、分享直达
- [ ] 真机 evidence：如不可用，标记 blocked/follow_up 并说明原因

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-29 08:24:32 | `/sprint-propose` | 纳入 `sprint-013` 正式范围，允许后续 `/opsx-apply` 前置门禁解析到 Sprint。 |
| 2026-07-29 08:19:01 | `/req-opsx` | 从 REQ-0080 创建 OpenSpec Change，生成 proposal、design、delta spec、tasks 与 trace。 |
