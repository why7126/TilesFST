## MODIFIED Requirements

### Requirement: 非首页返回首页悬浮按钮
系统 SHALL 在小程序首页以外的主要业务页面提供统一返回首页悬浮按钮，使用户可从深层浏览页面快速回到首页，同时保持页面原有顶部返回、TabBar、分享、滚动、筛选、加载和底部操作能力可用。

#### Scenario: 点击快速回首页
- **WHEN** 用户点击返回首页悬浮按钮
- **THEN** 小程序 SHALL 进入首页或项目确认的首页安全入口
- **AND** 若首页为 TabBar 页面，导航策略 SHALL 使用 `wx.switchTab` 或项目确认的等价策略
- **AND** 若首页非 TabBar 页面或需要重置深层页面栈，导航策略 SHALL 使用 `wx.reLaunch` 或项目确认的等价策略
- **AND** 返回首页过程 SHALL NOT 出现空白页、死循环跳转、重复堆叠首页或多次连续跳转。

#### Scenario: 导航失败可恢复
- **WHEN** 返回首页导航 API 返回失败、首页路径不可达或用户连续点击悬浮按钮
- **THEN** 页面 SHALL 保持当前页可恢复状态
- **AND** 系统 SHALL 通过防抖、状态锁或等价策略避免重复触发
- **AND** 失败处理 SHALL NOT 清空当前页面内容、阻断重试或暴露内部路径。

#### Scenario: 返回首页按钮跨页面重复进入后仍可用
- **WHEN** 用户在任一覆盖页面点击返回首页悬浮按钮并成功回到首页
- **AND** 用户再次进入同一覆盖页面或另一个覆盖页面
- **THEN** 返回首页悬浮按钮 SHALL 恢复可点击状态并能再次进入首页
- **AND** 按钮 SHALL NOT 因上一次点击后的防抖、状态锁、loading、disabled、页面实例变量或导航回调残留而失效。

#### Scenario: 返回首页导航状态在所有路径释放
- **WHEN** 返回首页悬浮按钮触发 `wx.switchTab`、`wx.reLaunch` 或项目确认的等价导航策略
- **THEN** 导航锁、loading、disabled 或等价点击保护状态 SHALL 在 `success`、`fail`、`complete` 或页面重新显示路径中恢复为可重试状态
- **AND** 快速连续点击 SHALL 最多触发一次有效导航
- **AND** 快速连续点击后再次进入覆盖页面 SHALL 仍可正常点击返回首页。
