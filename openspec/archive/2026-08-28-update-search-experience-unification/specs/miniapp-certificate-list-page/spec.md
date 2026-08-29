## MODIFIED Requirements

### Requirement: 证书列表状态
小程序证书列表页 SHALL 区分加载、空结果、网络失败和加载更多状态，并 SHALL 支持按证书名称、品牌名称、证书类型枚举或中文类型标签在当前证书列表页查找。证书列表搜索 SHALL 保持证书卡片布局，不跳完整搜索结果页，且 SHALL 仅返回公开可见证书，不得暴露后台内部字段或未授权文件引用。

#### Scenario: 证书列表搜索入口
- **WHEN** 用户进入证书列表页
- **THEN** 页面 SHALL 展示 `search-entry` 输入模式或等价证书关键词输入
- **AND** 搜索能力 SHALL 支持证书名称、品牌名称、证书类型枚举或中文类型标签
- **AND** 搜索提交 SHALL 请求 `/api/v1/miniapp/certificates` 并携带 `keyword`
- **AND** 页面 SHALL NOT 展示管理端证书类型筛选、品牌筛选、有效状态筛选或复杂筛选抽屉
- **AND** 页面 SHALL NOT 跳转 `/pages/search/index` 承接证书列表页搜索
- **AND** 小程序 SHALL 继续按分页请求公开证书列表或当前关键词下的公开证书结果。

#### Scenario: 证书列表搜索空态
- **WHEN** 证书关键词搜索无结果
- **THEN** 页面 SHALL 展示当前关键词对应的证书范围无结果说明
- **AND** 页面 SHALL 提供清空关键词或继续调整关键词的路径
- **AND** 页面 SHALL NOT 将列表内无结果误表达为全站无结果。

#### Scenario: 下拉刷新与加载更多
- **WHEN** 用户下拉刷新或触底加载更多
- **THEN** 小程序 SHALL 分别处理刷新、首屏加载和加载更多状态
- **AND** 重复触发 SHALL NOT 产生并发重复请求
- **AND** 无更多数据时 SHALL 展示轻量提示
- **AND** 若当前存在关键词，刷新和加载更多请求 SHALL 保留该关键词。

#### Scenario: 空状态与错误状态
- **WHEN** API 返回空列表或请求失败
- **THEN** 页面 SHALL 展示与当前默认列表或关键词搜索范围匹配的空态
- **AND** 网络失败 SHALL 保留可用已加载数据或缓存并提供重试入口
- **AND** 页面 SHALL NOT 白屏或长期停留在无反馈加载状态。
