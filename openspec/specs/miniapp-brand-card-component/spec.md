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

品牌卡片组件 SHALL 使用稳定尺寸 Logo 容器，并在 Logo 缺失、加载失败、品牌名称缺失或入口不可用时提供统一可理解的降级状态。品牌卡片组件用于小图展示时 SHALL 优先使用后端受控缩略图或等价轻量 Logo URL；详情、预览或后续高清展示 SHALL 使用原图或等价安全引用。品牌卡片普通展示 SHALL NOT 以 `brand_logo_url` 原图作为默认 fallback；来自 SKU 详情页、证书详情页、品牌详情页或品牌列表页的品牌卡展示均 SHALL 遵守同一约束。

#### Scenario: Logo 缺失或加载失败

- **WHEN** 品牌 Logo 缩略图缺失、为空、不可访问或图片加载失败
- **THEN** 品牌卡片 SHALL 按安全占位、品牌首字或默认图片的顺序降级
- **AND** 小图展示场景 SHALL NOT 直接请求大体积 Logo 原图作为性能通过 fallback
- **AND** 卡片 SHALL NOT 展示破图
- **AND** 图片异常 SHALL NOT 影响品牌名称、入口提示和卡片点击能力。

#### Scenario: 品牌卡默认禁止原图 Logo fallback

- **WHEN** 页面未显式声明高清预览、下载或原图查看入口
- **THEN** 品牌卡片组件默认 SHALL 禁止使用 `brand_logo_url` 作为普通展示图片源
- **AND** 组件收到 `brand_logo_thumbnail_url` 为空时 SHALL 展示安全占位、品牌首字或默认图
- **AND** 静态测试 SHALL 覆盖默认配置不会产生 `brand_logo_thumbnail_url || brand_logo_url` 等原图 fallback 表达式。

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

### Requirement: 证书详情页品牌入口复用品牌卡片

小程序证书详情页 SHALL 使用既有品牌卡片组件展示所属品牌入口。证书详情页 SHALL 将证书详情响应中的品牌数据、来源上下文和证书上下文传入品牌卡片组件；品牌卡片组件 SHALL 继续负责 Logo 展示、名称展示、入口提示、不可用态、点击跳转和埋点触发。

#### Scenario: 证书详情页传入品牌卡片数据

- **WHEN** 小程序证书详情页渲染所属品牌入口
- **THEN** 页面 SHALL 使用品牌卡片组件
- **AND** 页面 SHALL 向组件传入 `brandId`、`brandName`、`brand_logo_thumbnail_url`、品牌入口参数和来源上下文
- **AND** 页面 SHALL NOT 保留页面私有品牌入口 DOM、模板结构或独立点击逻辑。

#### Scenario: 证书详情页品牌入口点击跳转

- **WHEN** 用户点击证书详情页可用品牌卡片
- **THEN** 小程序 SHALL 跳转到对应品牌详情页或既定品牌入口
- **AND** 跳转上下文 SHALL 包含可用的品牌标识和 `sourcePage=certificate_detail` 或等价来源参数
- **AND** 埋点失败 SHALL NOT 阻断品牌跳转。

#### Scenario: 证书详情页品牌入口不可用

- **WHEN** 证书详情页品牌数据缺失、品牌不可公开或品牌入口参数不可用
- **THEN** 品牌卡片 SHALL 使用统一不可用态或页面 SHALL 不展示品牌入口
- **AND** 小程序 SHALL 阻止无效跳转
- **AND** 证书详情页主体信息 SHALL 继续可浏览。

#### Scenario: 证书详情页品牌卡片移动端验收

- **WHEN** 团队验收证书详情页品牌入口
- **THEN** 验收 SHALL 覆盖 320 pt、375 pt 和 430 pt 逻辑宽度
- **AND** 正常态、缩略图缺失态、图片失败态、长品牌名态和不可用态 SHALL 确认无重叠、无遮挡、无横向溢出
- **AND** 证据 SHALL 说明证书详情页与其他品牌卡片调用方的一致性结论。

