---
created_at: 2026-09-05 22:28:07
updated_at: 2026-09-07 22:53:59
---

# 公开页面分享设计

## 1. 上下文与目标

来源REQ-0134已评审并纳入sprint-029，L/5人天。11页矩阵、29条验收以需求requirement.md与acceptance.md为事实源。实现修改小程序分享与接收逻辑及后端既有事件字典，复用公开接口、原生菜单和现有导航。

## 2. 设计决策

### D1 统一参数工具与页面适配

在src/miniapp/utils中新增同步TS/JS分享工具，负责白名单、编码、容错、长度限制与默认卡片；页面适配器提供已生效状态和公开对象素材。朋友path与朋友圈query共用同一序列化结果，禁止拷贝整个query/data/storage。页面保留明确生命周期回调，便于注册矩阵检查。相比逐页复制逻辑，共用工具降低编码与安全策略漂移；不引入全局Page劫持。

| 页面目录 | 允许的业务参数 | 恢复策略 |
|---|---|---|
| index、store-info、find | 无 | 固定公开入口。 |
| tile-detail | skuId | 同一公开SKU。 |
| brand-detail | brandId | 同一公开品牌，默认Tab。 |
| certificate-detail | certificateId | 同一公开证书。 |
| product-list | categoryId、categoryLevel、categoryName、brandId、keyword、section、spec、priceRange、sort | 合法参数恢复并第一页查询。 |
| brand-list、certificates | keyword | 当前列表内部搜索，第一页。 |
| category | categoryId | 作为一级分类选择；失效则默认，不恢复滚动。 |
| search | keyword、scope、tab | 无词为公开首页，有词为结果；tab仅all/brand/sku/certificate。 |

所有分享统一生成source=share，shareChannel为wechat_friend或wechat_timeline；兼容读取旧sourcePage=share，业务参数不接受发送者链路ID。来源仅用于非可信归因。

ID需为正安全整数；categoryLevel仅primary/secondary；section仅new/hot；sort仅default/latest/price_asc/price_desc。keyword/spec上限80字符，priceRange上限40字符，沿用后端miniapp.py契约；价格区间语法和scope有效集合在实施前核对现有解析器，不扩展API。categoryName仅展示，上限80字符，不作为查询身份。

项目主动设置编码后query上限2048个ASCII字符，这是应用保护阈值，不声称为微信平台最大值。生成端先省略categoryName等冗余展示名；仍超限或必需输入不合法时返回该页默认入口卡片，标题明确为默认入口。详情保留合法ID；非法ID直达呈不可用态。用2047/2048/2049边界与中文编码样例测试，目标客户端不支持该阈值时降低统一常量并回归。

解析仅经过一个容错解码入口，结合开发工具实际onLoad参数形态确认解码层级；不循环decode。畸形转义、未知键和不支持枚举安全忽略，不能白屏。列表不传播page、结果数组或滚动位置。

### D2 有效状态与接收恢复

分享只取已提交查询，输入草稿不传播。商品列表已有轻量UI不新增筛选控件，但其兼容入口携带合法spec/priceRange/sort时应保留并送入既有products查询。无这些条件时保持默认列表；测试以合法深链设置状态。

搜索将“执行结果查询”和“主动提交并写历史”拆为可复用方法：分享恢复只查询、记录接收访问，不写历史或search_submit。分类onLoad和onShow统一遵守有效分享选择优先，避免旧storage回写覆盖。发现页仅同步TS已有openSearch到JS。

### D3 卡片与失败边界

优先使用已取得的公开轻量分享图/缩略图；无数据或已知不可读时使用包内/assets/logos/product-logo.png。搜索首页始终用固定公开图，不依赖截图。图片预检查不得阻塞同步分享返回；未就绪时直接固定图，异步准备就绪后，后续分享使用getImageInfo返回的已解码本地路径，避免原URL随后过期；没有有效本地路径则继续使用Logo。验证URL可读性及实际卡片渲染；原始大图、个人历史和内部字段不进入卡片。

接收用既有公开API重取数据；内容失效或下架保持明确不可用态，不借用其他对象伪装当前详情。普通模式无栈返回沿用统一首页兜底；朋友圈单页模式按实际可用能力提供进入小程序入口。无新增鉴权绕过。

### D4 事件与请求链路

保留已存在home_share、sku_share_click、product_list_share_click、brand_detail_share_click、certificate_detail_share_click；新增brand_list_share_click、certificate_list_share_click、store_info_share_click、category_share_click、search_share_click、find_share_click。share_page_open作为统一接收事件，普通页面访问口径不重复加成。

事件只表示触发或接收，不表示完成。payload仅含无query的page_path、渠道、对象ID、has_keyword、keyword_length、filter_count等摘要；不放keyword原文、完整URL或发送者链路ID。同一次点击由生命周期回调采集一次，现有按钮不重复track。用安全包装处理同步抛错；既有track处理异步失败，不修改底层请求契约。接收端建立自身行为上下文。

## 3. UI Contract

| 项目 | 合同 |
|---|---|
| 事实源 | 无prototype/PNG；已批准REQ→acceptance→本设计→ui-design→已有页面。 |
| 页面与入口 | 11页注册路径，朋友与朋友圈直达；收藏不纳入。 |
| 信息架构 | 保留顶部导航、主体列表/详情、空态/错误态和原生菜单；不新增面板、筛选抽屉或排序tabs。 |
| 视觉token | 使用现有semantic token、字体、间距和Logo；本Change不调整色值或布局。 |
| 交互状态 | 正常、加载、空、错误、重复进入、无栈返回；hover/键盘桌面交互N/A，为小程序触控场景。 |
| 图标文案 | 不模拟原生胶囊；标题匹配对象或默认入口，find保留开始搜索。 |
| Mock/API边界 | 单测用虚构页面数据与wx stub；实际页面用现有公开API；Mock不证明真机成功。 |
| 权限 | 分享不传凭据，不改变管理端权限；公开状态由后端决定。 |
| 一致性参照 | 保留首页引导、详情分享、分类与搜索结构；核对REQ的5条AC-XCUT。 |

原型冲突报告：无prototype文件。正式miniapp-product-list-page禁止复杂筛选UI，本Change只恢复合法查询上下文，不恢复已移除控件。以MODIFIED delta扩展分享契约；其他视觉规格保持不变。无新页面壳，不设置原型Skeleton批准门禁；实施前记录现有页面基线截图作为结构对照。桌面1440px为N/A，改用小程序320/375/430pt、DevTools或真机证据；相关导航/图片疑点记录实际样式或等价工具证据。

## 4. 产品数据采集与影响

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers: [miniapp, backend, usage_events]
  reason: 补齐分享与接收事件，复用端请求封装；API、DB、request_logs和保留周期无契约变化。
  validation: 本地98项回归及转译TS28项通过；DevTools记录公开页面基线，真实双端已豁免，线上采集留待发布验证。
  task_trace: N/A，未新增后端复杂任务或节点。
```

不新增OpenAPI、Orval、SQLite/MySQL迁移、Pydantic Schema、API错误码或Docker输入。若实际实现改变契约，先更新范围声明和对应文档/测试。storage仅消费公开素材，无上传及权限变更。

## 5. 风险、依赖与回退

- sprint-029剩余8人天缓冲，低于30%建议；本项5人天估算不重复计入Change。与REQ-0133同页JS修改串行整合并联合回归，保持BUG-0148-miniapp-product-list-card-image-fit 图片适配成果。
- 导航知识库仍draft，需求评审已采纳AC-XCUT具体条款。引用docs/knowledge-base/best-practices/miniapp-custom-navigation.md和retrospectives/sprint-028-retrospective.md。
- 微信/基础库具体版本在实施测试计划冻结，不承诺未测试历史最低版本。按用户指示豁免真机验证，记录未执行，不计为通过。
- 无数据迁移；经正常小程序版本发布交付，失败时回退小程序构建；后端事件字典为兼容性扩展，无需删除数据。

## 6. 实施前核对

实施任务负责核对scope与priceRange解析语法、编码层级、客户端版本和2048应用阈值兼容性，并将结果回填trace/test-plan；这些不改变批准业务范围，无需再次选择产品策略。

## 实施边界核对

后端既有priceRange解析器允许非负、有限且有序的min-max和单侧空值；分享层文本限制40字符。scope沿用分类名称，恢复到搜索filterSnapshot.category，无新API参数。普通导航值按现有encodeURIComponent构造，分享入口仅解码一次。编码总长阈值为2048，先移除categoryName展示字段，仍超限则全部默认；可选数字ID的0表示未选择，不应导致其他有效条件丢失。测试已覆盖上述契约；DevTools 2.02.2608060与基础库3.17.1（灰度）已冻结；真实微信版本和平台接收矩阵按用户指示豁免，不以模拟器版本证明真机兼容性。

## DevTools采集契约修正

2026-09-06权限恢复后，模拟器分享直达正常加载，usage-events出现HTTP 400。本地真实JS载荷→FastAPI集成测试复现29项失败，错误40001分别为未知事件和缺少必填属性。根因状态confirmed（本地契约）：共享工具遗漏旧事件兼容字段，后端字典未注册7个新增事件。修复范围增加后端事件注册；保留旧事件必填约束，小程序补充无query的share_path、接收端本地requestId、sourcePage及camelCase公开ID兼容字段。新事件拒绝原文关键词/完整URL属性。请求响应Pydantic/OpenAPI结构、数据库表、错误码与请求封装保持不变；后端修复须随正常发布交付，不能以本地通过表示线上已修复。
