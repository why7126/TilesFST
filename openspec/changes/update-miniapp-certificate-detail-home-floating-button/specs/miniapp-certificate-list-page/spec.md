## ADDED Requirements

### Requirement: 证书详情返回首页悬浮按钮

小程序证书详情页 SHALL 复用既有 `home-floating-button` 组件提供明确的返回首页悬浮入口。该入口 SHALL 与其他非首页深层内容页保持一致的位置口径，默认使用 `offset="list"`；页面 SHALL NOT 新增私有返回首页按钮结构、私有 offset、私有样式或私有跳转逻辑。

#### Scenario: 证书详情页挂载返回首页按钮

- **WHEN** 用户进入 `pages/certificate-detail/index`
- **THEN** 页面 SHALL 声明并挂载 `home-floating-button`
- **AND** 按钮 SHALL 默认使用 `offset="list"`
- **AND** 页面原有 `custom-navigation` 左上返回能力 SHALL 保持可用。

#### Scenario: 点击悬浮按钮返回首页

- **WHEN** 用户点击证书详情页返回首页悬浮按钮
- **THEN** 小程序 SHALL 沿用 `home-floating-button` 的首页导航策略进入 `/pages/index/index`
- **AND** 失败兜底、忙碌态、失败提示和导航锁 SHALL 由既有组件负责
- **AND** 页面 SHALL NOT 实现重复的私有 `wx.switchTab`、`wx.reLaunch` 或 toast 逻辑。

#### Scenario: 页面状态覆盖

- **WHEN** 证书详情页处于正常、加载、网络失败、证书不可查看、证书不存在、图片失败或分享直达状态
- **THEN** 页面 SHALL 保留可恢复的返回首页路径
- **AND** 悬浮按钮 SHALL NOT 遮挡证书主图、品牌入口、错误态按钮、顶部自定义导航或底部安全区
- **AND** 证书信息字段被悬浮按钮局部覆盖 SHALL be acceptable，页面 SHALL NOT 为证书信息卡新增右侧避让。

#### Scenario: 重复点击与再次进入

- **WHEN** 用户快速重复点击证书详情页返回首页悬浮按钮，或成功返回首页后再次进入证书详情页
- **THEN** 返回首页导航 SHALL 保持可恢复、可重试
- **AND** 页面 SHALL NOT 出现重复跳转、多次 toast、页面栈异常或导航锁无法释放。

#### Scenario: 静态检查与设备 evidence

- **WHEN** 团队验收证书详情页返回首页悬浮按钮
- **THEN** 验收 SHALL 覆盖 `index.json` 组件声明、`index.wxml` 组件引用、`offset="list"` 和 `.ts` / `.js` 同步
- **AND** DevTools evidence SHALL 覆盖 320、375、430 pt 视口下标题、原生胶囊 reserve、内容 offset、品牌入口同宽、证书信息非避让排版和悬浮按钮位置一致结论
- **AND** 真机 evidence 不可用时 SHALL 标记 `blocked` 或 `follow_up`，不得写作真机通过。
