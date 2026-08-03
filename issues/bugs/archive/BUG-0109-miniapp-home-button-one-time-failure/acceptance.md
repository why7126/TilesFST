---
bug_id: BUG-0109-miniapp-home-button-one-time-failure
acceptance_status: passed
created_at: 2026-08-03 08:22:19
updated_at: 2026-08-03 20:52:16
---

# 验收标准

## AC-001 返回首页按钮可重复生效

- GIVEN 用户进入任一带返回首页按钮的非首页页面
- WHEN 用户点击返回首页按钮，并在返回首页后再次进入同一页面重复点击
- THEN 每次点击都应稳定返回首页
- AND 不应出现点击无响应、按钮永久禁用或控制台导航错误

## AC-002 多页面返回首页行为一致

- GIVEN 商品详情、品牌详情、证书详情、搜索结果等页面均存在返回首页入口
- WHEN 用户分别进入这些页面并点击返回首页按钮
- THEN 每个页面都应正常返回首页
- AND 从任一页面返回首页后，再进入其他页面继续点击也应生效

## AC-003 点击状态在成功、失败和完成路径均能恢复

- GIVEN 返回首页按钮使用防重复点击、节流、防抖、loading 或 disabled 状态
- WHEN 首页跳转成功、跳转失败或跳转完成回调执行
- THEN 按钮内部导航锁和可点击状态均应恢复
- AND 再次进入页面时不应继承上一次点击后的失效状态

## AC-004 快速重复点击不造成异常页面栈

- GIVEN 用户在非首页页面快速连续点击返回首页按钮
- WHEN 小程序处理重复点击
- THEN 应最多执行一次有效首页跳转
- AND 不应生成异常页面栈、重复页面、报错或永久锁定状态

## AC-005 回归范围覆盖

- SHOULD 覆盖微信开发者工具和体验版小程序。
- SHOULD 覆盖同一页面重复进入、不同页面交叉进入、从首页再进入详情页、从搜索结果进入详情页后返回首页等路径。
- SHOULD 补充或更新小程序导航组件、页面方法或等价静态/手工验收记录。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-03 20:52:16
accepted_by: workflow-sync
source_change: fix-miniapp-home-navigation-repeat-click
source_sprint: sprint-018
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

