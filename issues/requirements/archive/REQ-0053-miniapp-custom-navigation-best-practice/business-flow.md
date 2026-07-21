---
requirement_id: REQ-0053-miniapp-custom-navigation-best-practice
title: 小程序自定义导航 best-practice 沉淀业务流程
status: done
created_at: 2026-07-19 18:41:33
updated_at: 2026-07-19 21:05:25
---

# REQ-0053 小程序自定义导航 best-practice 沉淀业务流程

## 1. 后续页面接入流程

```text
新增 / 改造小程序页面
  |
  v
是否使用自定义导航？
  |
  +-- 否：记录豁免原因
  |       |
  |       +-- acceptance 标记 N/A
  |
  +-- 是：识别页面形态
          |
          +-- 首页形态：品牌信息优先，无返回按钮
          |
          +-- TabBar 页面形态：按页面定位确认是否展示返回
          |
          +-- 普通非首页：标题 + 返回按钮 + 胶囊 reserve
          |
          +-- 详情 / 分享直达：返回按钮必须具备首页兜底
          |
          v
      套用状态栏、胶囊、offset checklist
          |
          v
      按截图矩阵记录 DevTools / 真机 evidence
```

## 2. 状态栏与胶囊决策流程

```text
页面加载自定义导航
  |
  v
读取窗口 / 状态栏 / 胶囊信息
  |
  +-- 成功：使用真实状态栏高度、胶囊尺寸和右侧 reserve
  |
  +-- 失败：使用项目统一 fallback
          |
          +-- fallback 值必须在 best-practice 中说明
          +-- 不允许各页面自行猜测高度
```

## 3. 返回兜底流程

```text
用户点击返回按钮
  |
  v
是否存在上一页页面栈？
  |
  +-- 是：wx.navigateBack()
  |       |
  |       +-- fail：回首页兜底
  |
  +-- 否：回首页兜底
          |
          +-- fail：二级兜底到安全入口
```

## 4. 截图验收记录流程

```text
识别导航相关 Change / 页面
  |
  v
选择验收矩阵
  |
  +-- DevTools：320 / 375 / 430 pt
  |
  +-- 真机：iPhone 刘海屏 / iPhone 非刘海屏 / Android 常见机型
  |
  +-- 状态：正常 / 加载 / 空状态 / 错误 / 分享直达 / 长标题
  |
  v
记录 evidence
  |
  +-- passed：截图或录屏引用 + 结论
  +-- failed：失败表现 + 影响页面 + 后续处理
  +-- blocked：阻塞原因
  +-- follow_up：剩余风险和承接方式
  +-- not_applicable：N/A reason
```

## 5. 与父 REQ 差异

| 对比项 | REQ-0048 小程序全局自定义导航栏 | REQ-0053 小程序自定义导航 best-practice |
|---|---|---|
| 类型 | 功能实现需求 | 治理 / 经验沉淀需求 |
| 交付重点 | 首页与非首页导航模块、返回、胶囊避让、页面接入 | 文档化规则、checklist、截图矩阵和引用方式 |
| 是否改源码 | 是，后续 OpenSpec 已交付小程序组件和页面接入 | 本需求默认不改源码，后续 Change 以文档和流程引用为主 |
| 验收方式 | 页面功能和布局验收 | 可复用 AC、evidence 矩阵和后续 Change 引用 |
| 与 REQ-0052 关系 | 可被设备 evidence 模板记录 | 直接复用 REQ-0052 的 DevTools / 真机 evidence 字段 |

## 6. 风险控制

| 风险 | 控制方式 |
|---|---|
| best-practice 变成泛泛说明 | acceptance 要求必须提供接入 checklist、截图矩阵和引用示例。 |
| DevTools 通过被误写为真机通过 | 与 REQ-0052 evidence 状态联动，DevTools 和真机分层记录。 |
| 页面 offset 再次散落硬编码 | best-practice 要求统一 spacer / token / class 策略，并要求特殊页面说明原因。 |
| 胶囊避让只在单机型通过 | 截图矩阵覆盖 320 / 375 / 430 pt 和真机设备组合。 |
| 历史回填扩大范围 | 本需求只沉淀规则，不强制回填全部历史截图。 |
