## MODIFIED Requirements

### Requirement: 媒体对象必须可受控读取

系统 SHALL 通过后端受控接口读取媒体对象，保护对象存储访问边界，并 SHALL 支持图片缓存、列表缩略图、详情展示图、媒体观测、对象存储直出和视频 Range 请求。商品列表缩略图、品牌图片缩略图、Banner 图片缩略图、图片类品牌证书缩略图和图片 `display` 派生图 SHALL 与原图位于同一对象目录或等价可追溯对象路径，并 SHALL 通过文件名差异、规格目录或等价稳定规则区分 `thumbnail`、`display` 与 `original`。

系统 SHALL 生成真实轻量缩略图与详情展示图：对于尺寸大于目标尺寸的支持图片，派生图 SHALL 经过后端图片处理生成，像素宽高 SHALL 小于或等于对应规格约定最大宽高，且 SHALL NOT 只是原图 bytes 的复制品。缩略图体积目标 SHALL 读取缩略图配置；详情展示图 / `.display` 体积目标 SHALL 读取系统设置 media 分组的 display 图体积目标 effective 配置，默认 SHALL 为 `768` KB。无法达到目标体积时 SHALL NOT 默认阻断原图上传或业务保存，且 SHALL 记录 warning 或可复核失败原因。

对象存储直出 SHALL 作为受控媒体读取形态之一，仅能由后端媒体服务或对象存储适配层生成。系统 SHALL 明确签名 URL、公开 URL、后端 `/media` 代理 URL 的选择条件、过期策略、缓存策略和 fallback。客户端 SHALL NOT 直连未授权对象存储，响应 SHALL NOT 暴露对象存储密钥、bucket 权限细节或内部 endpoint 白名单。

#### Scenario: 多规格图片读取 URL 可追溯

- **WHEN** 客户端请求图片媒体 URL
- **THEN** 系统 SHALL 能返回或派生 `thumbnail`、`display`、`original` 三类 URL 语义
- **AND** 每类 URL SHALL 可追溯到同一媒体记录或业务对象
- **AND** 响应 SHALL NOT 暴露原始 object key、对象存储 endpoint、bucket 名称、access key、secret key 或未授权素材路径。

#### Scenario: 对象存储直出失败可回退

- **GIVEN** 当前媒体使用对象存储直出 URL
- **WHEN** 直出 URL 过期、对象不可读或权限校验失败
- **THEN** 客户端或后端 SHALL 按明确策略回退到受控 `/media` 代理 URL 或安全占位
- **AND** 回退事件 SHALL 可观测
- **AND** 验收 SHALL 记录 URL 类型、HTTP 状态、业务状态和用户可见表现。

#### Scenario: 派生图不是原图复制

- **WHEN** 系统生成 `thumbnail` 或 `display`
- **THEN** 派生图 SHALL 经过后端图片处理
- **AND** 对大于目标尺寸的支持图片，派生图像素或 bytes SHALL 体现对应规格收益
- **AND** `.display` 体积目标 SHALL 来自 display 图体积目标 effective 配置
- **AND** 验收 SHALL NOT 将与原图同 bytes 或无收益的派生图写作性能通过。

#### Scenario: display 配置变更不改变对象寻址

- **WHEN** `admin` 修改 display 图体积目标上限配置
- **THEN** 后续新生成 `.display` 对象 MAY 因压缩策略产生不同 bytes、尺寸、质量或文件大小
- **AND** `.display` object key、URL、bucket、标准前缀和受控 `/media/...` 读取语义 SHALL 保持稳定
- **AND** 保存设置 SHALL NOT 自动覆盖历史 `.display` object。
