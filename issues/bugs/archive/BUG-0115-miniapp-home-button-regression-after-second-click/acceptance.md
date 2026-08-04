---
bug_id: BUG-0115-miniapp-home-button-regression-after-second-click
acceptance_status: passed
created_at: 2026-08-04 08:55:33
updated_at: 2026-08-04 23:12:32
---

# 验收标准

## AC-001 同一页面重复点击可持续生效

- GIVEN 用户进入任一带返回首页悬浮按钮的非首页页面
- WHEN 用户点击返回首页按钮回到首页，并再次进入同一页面后重复点击
- THEN 每一次点击都应稳定返回首页
- AND 不应出现点击无响应、按钮永久禁用或控制台导航错误

## AC-002 跨页面返回首页状态互不污染

- GIVEN 分类页、品牌列表页、搜索结果页、商品详情页、品牌详情页等页面均存在返回首页入口
- WHEN 用户从一个页面点击返回首页后，再进入另一个页面点击返回首页
- THEN 每个页面的返回首页按钮都应独立、稳定生效
- AND 不应继承上一个页面点击后的 `navigating`、loading、disabled 或等价状态

## AC-003 TabBar 与非 TabBar 页面均覆盖

- GIVEN 小程序存在 TabBar 页面和非 TabBar 详情/列表页面
- WHEN 用户分别从这些页面点击返回首页按钮
- THEN TabBar 页面应通过安全的首页跳转路径返回首页
- AND 非 TabBar 页面应通过 `switchTab` 或兜底策略返回首页
- AND 两类页面在第二轮点击时行为一致

## AC-004 导航锁在成功、失败和兜底路径均释放

- GIVEN 返回首页按钮使用防重复点击状态
- WHEN `wx.switchTab` 成功、失败，或失败后进入 `wx.reLaunch` 兜底
- THEN 组件导航锁均应在可预期时间内恢复
- AND 后续正常点击不应被上一轮状态拦截

## AC-005 快速重复点击不造成永久失效

- GIVEN 用户快速连续点击返回首页按钮
- WHEN 小程序处理重复点击
- THEN 应最多触发一次有效首页导航
- AND 不应生成异常页面栈、重复首页、报错或永久锁定状态
- AND 经过防重复窗口后再次点击仍可正常返回首页

## AC-006 回归测试覆盖真实状态流

- MUST 补充或更新可执行的组件/导航状态流测试，覆盖“首次点击成功 → 再次进入页面 → 第二次点击仍触发返回首页”。
- MUST 保留或更新小程序静态检查，确保覆盖页面仍使用统一 `home-floating-button`。
- SHOULD 在微信开发者工具或体验版中记录同页重复进入、跨页重复进入、TabBar 页面和非 TabBar 页面验证结果。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-04 23:12:32
accepted_by: workflow-sync
source_change: fix-miniapp-home-button-repeat-click-regression
source_sprint: sprint-019
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

## Apply evidence

| 类型 | 状态 | 证据 |
|---|---|---|
| 自动化测试 | passed | `uv run pytest tests/test_miniapp_static.py`，33 passed；覆盖统一组件接入、返回首页状态流、失败兜底、快速重复点击和解锁后再次点击。 |
| OpenSpec 校验 | passed | `openspec validate fix-miniapp-home-button-repeat-click-regression --strict` 通过；`python scripts/validate-openspec-language.py` 通过。 |
| 人工体验版 / 真机验证 | follow_up | 仍需在微信开发者工具或体验版补录分类页、品牌列表页、搜索结果页、商品详情页和品牌详情页的同页/跨页第二轮点击 evidence。 |

```yaml
acceptance_status: passed
accepted_at: null
accepted_by: null
source_change: fix-miniapp-home-button-repeat-click-regression
source_sprint: sprint-019
evidence: []
failed_items: []
source_event: opsx.apply
notes: 已验收；由 opsx.apply 标记，后续 archive 时回填结论。
```
