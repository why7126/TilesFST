# miniapp-brand-card-component Specification

## Purpose
定义微信小程序品牌卡片组件的展示、Logo 降级、跳转 fallback、埋点上下文与移动端验收要求，确保 SKU 详情页和后续品牌相关页面复用同一单品牌入口能力。
## Requirements
### Requirement: 微信小程序品牌卡片组件
系统 SHALL 提供微信小程序品牌卡片组件，用于在 SKU 详情页和后续品牌相关小程序页面中复用单个品牌展示、入口提示、点击跳转和卡片级异常处理。

#### Scenario: 组件接收单品牌展示数据
- **WHEN** 页面容器渲染品牌卡片组件
- **THEN** 页面 SHALL 向组件传入单个品牌展示对象、来源上下文和可选入口配置
- **AND** 组件 SHALL NOT 在内部直接请求品牌列表、品牌详情、SKU 列表或搜索接口
- **AND** 页面容器 SHALL 负责页面加载态、错误态、列表状态机和是否展示品牌卡片。

#### Scenario: 展示品牌核心信息
- **WHEN** 品牌展示对象包含 Logo、品牌名称和入口提示
- **THEN** 品牌卡片 SHALL 展示稳定 Logo 区、品牌名称、入口提示或副文案以及进入提示
- **AND** 副文案缺失时 SHALL 按统一策略隐藏或展示兜底文案
- **AND** 卡片 SHALL NOT 展示空字符串、`null`、`undefined`、接口字段名或破损异常文本。

#### Scenario: 长品牌名小屏展示
- **WHEN** 品牌名称较长且设备宽度为 320 pt、375 pt 或 430 pt
- **THEN** 品牌名称 SHALL 按设计策略截断或换行
- **AND** 品牌名称 SHALL NOT 撑破卡片、遮挡 Logo、遮挡入口提示或挤压进入箭头。

### Requirement: 品牌 Logo 与异常状态
品牌卡片组件 SHALL 使用稳定尺寸 Logo 容器，并在 Logo 缺失、加载失败、品牌名称缺失或入口不可用时提供统一可理解的降级状态。

#### Scenario: Logo 容器稳定
- **WHEN** 品牌 Logo 正在加载、加载完成或加载失败
- **THEN** Logo 区域 SHALL 保持稳定尺寸
- **AND** 卡片高度 SHALL NOT 因图片加载状态变化发生明显跳动。

#### Scenario: Logo 缺失或加载失败
- **WHEN** 品牌 Logo 缺失或图片加载失败
- **THEN** 品牌卡片 SHALL 展示品牌首字、默认图片或统一深色占位
- **AND** 卡片 SHALL NOT 展示破图
- **AND** 图片异常 SHALL NOT 影响品牌名称、入口提示和卡片点击能力。

#### Scenario: 品牌名称缺失
- **WHEN** 品牌名称缺失或不可用
- **THEN** 品牌卡片 SHALL 展示“品牌信息待完善”或等价兜底文案
- **AND** 组件 SHALL 禁用依赖品牌名称的搜索 fallback
- **AND** 组件 SHALL 记录或触发可供页面上报的数据异常上下文。

#### Scenario: 入口不可用
- **WHEN** 品牌入口不可用且无法使用品牌名称搜索 fallback
- **THEN** 品牌卡片 SHALL 展示禁用态或点击后提示“品牌内容暂不可查看”或等价文案
- **AND** 组件 SHALL 阻止无效跳转。

### Requirement: 品牌卡片点击与跳转
品牌卡片组件 SHALL 提供整卡点击能力，并按配置入口、品牌名称搜索 fallback 和不可用提示的顺序处理跳转。

#### Scenario: 使用配置入口跳转
- **WHEN** 用户点击品牌卡片且品牌数据提供 `brand_entry_path`
- **THEN** 小程序 SHALL 优先跳转到 `brand_entry_path`
- **AND** 跳转上下文 SHALL 包含可用的品牌 ID、品牌名称和来源页面信息。

#### Scenario: 使用品牌名称搜索 fallback
- **WHEN** 用户点击品牌卡片且 `brand_entry_path` 缺失但品牌名称可用
- **THEN** 小程序 SHALL fallback 到品牌关键词搜索页或等价品牌承接页
- **AND** 小程序 SHALL 对品牌名称进行 URL 编码后再拼接跳转参数。

#### Scenario: 整卡触控与反馈
- **WHEN** 用户触控品牌卡片
- **THEN** 整张品牌卡片 SHALL 作为主要点击热区
- **AND** 有效触控高度 SHALL 不小于 44px
- **AND** 小程序 SHALL 提供可感知的触控反馈。

#### Scenario: 防止重复跳转
- **WHEN** 用户连续快速点击品牌卡片
- **THEN** 小程序 SHALL 防止重复打开多个页面或重复触发多次跳转。

### Requirement: 品牌卡片埋点与验收证据
品牌卡片组件 SHALL 支持点击、图片异常和不可用点击等事件上下文，并在实现验收中覆盖小程序视口与运行入口一致性。

#### Scenario: 品牌卡片点击事件
- **WHEN** 用户点击可用品牌卡片
- **THEN** 系统 SHOULD 记录 `brand_card_click` 或等价事件
- **AND** 事件参数 SHOULD 包含 `brandId`、`brandName`、`sourcePage`、`sourceModule`、`skuId`、`listContext`、`index` 和 `requestId` 中可用字段。

#### Scenario: 图片异常事件
- **WHEN** 品牌 Logo 加载失败
- **THEN** 系统 SHOULD 记录 `brand_card_image_failed` 或等价事件
- **AND** 事件参数 SHOULD 包含可用的品牌和来源上下文。

#### Scenario: 不可用点击事件
- **WHEN** 用户点击不可用品牌卡片
- **THEN** 系统 SHOULD 记录 `brand_card_unavailable_click` 或等价事件
- **AND** 事件参数 SHOULD 标识不可用原因和来源上下文。

#### Scenario: 移动端截图验收
- **WHEN** 团队验收品牌卡片组件
- **THEN** 验收证据 SHALL 覆盖 320 pt、375 pt 和 430 pt 宽度
- **AND** 正常态、Logo 缺失态、长品牌名态和不可用态 SHALL 分别确认无重叠、无遮挡、无横向溢出。

#### Scenario: 小程序运行入口一致
- **WHEN** 新增品牌卡片组件并在微信开发者工具或真机验收
- **THEN** 实际加载的 `.js` 逻辑 SHALL 与源 `.ts` 逻辑一致
- **AND** 若项目采用构建同步机制，任务输出 SHALL 说明同步命令或项目认可的同步方式。
