# REQ-0038 品牌证书管理页面/弹窗 - 产品原型图上下文工程

## 1. 原型目标

用于指导前端开发还原 TILESFST 管理后台“瓷砖品牌 / 品牌证书”页面及“新增/编辑证书”弹窗。Golden Reference：

- `brand-certificate-management.png`
- `brand-certificate-management.html`

视觉优先级：acceptance.md > requirement.md > 本上下文 > HTML > PNG > ui-design.md。

注意：当前 HTML / PNG 原型仍保留早期品牌摘要栏视觉，用于色彩、密度、弹窗和表格样式参考；正式实现必须以 `acceptance.md` 的“品牌证书一级页不展示品牌摘要栏”作为门禁。

## 2. 视觉来源

继承品牌管理 V7 与管理后台 Design System：

- 工业石材 · 暗色旗舰风。
- 固定 264px Sidebar，右侧独立滚动。
- 页面底色、卡片底色、深色底、主文字、弱文字、品牌金、风险色均映射语义 Token。
- 品牌金仅用于主 CTA、激活态、关键指标、长期有效/正常状态。
- 圆角接近直角：按钮 2px、卡片 3px、Badge 1–2px。
- 分割线 0.5px，内容密度偏企业管理后台。

正式 React 实现禁止复制原型中的裸色值，必须使用项目语义 Token。

## 3. 页面画布

- Golden Reference：1440 × 1100。
- Sidebar：264px，100vh sticky。
- 主内容：左/右 56px 内边距，最大宽度 1080px。
- 页面独立滚动，不让 Sidebar 跟随滚动。
- 当前导航：品牌证书高亮。

## 4. 页面结构

```text
page-header
→ metric-grid (4)
→ filter-card
→ certificate-table-card
→ pagination
```

### 4.1 页面头部

页面头部可提供弱化的“← 返回品牌列表”辅助入口，但品牌证书一级页不展示品牌摘要栏或品牌详情面包屑。

### 4.2 页面标题

- 眉标：BRAND ASSETS，10px，品牌金，高字距。
- 标题：品牌证书，24px，正常字重。
- 描述：12px 弱文字。
- 右侧主按钮：＋ 新增证书，40px 高，品牌金实底。

### 4.3 指标卡片

4 列，间距 12px，高约 104px：

1. 证书总数 18。
2. 有效证书 14。
3. 即将到期 2。
4. 已过期 2。

数字为 26px。即将到期数字使用警示语义；已过期使用风险语义；其余使用品牌金。卡片右上保留轻微材质光晕。

### 4.4 筛选区

单行六段：

```text
关键词(1fr) / 所属品牌(150) / 证书类型(140) / 有效状态(140) / 展示状态(130) / 重置
```

输入框与 Select 高 40px。无“证书检索”标题。

### 4.5 列表卡片

表头：证书 / 类型 / 发证机构 / 有效期 / 有效状态 / 前台展示 / 排序 / 更新时间 / 操作。

建议桌面最小内容宽度 1040px；窄屏时表格容器横向滚动，页面本身不产生横向滚动。

证书列：

- 缩略图 42×54，接近证书纵向比例。
- PDF 用深色文档占位 + PDF 标签。
- 右侧证书名主文字，证书编号弱文字。

操作：预览、编辑为品牌金；显示/隐藏为次文字；删除为风险色。操作间距 10px。

### 4.6 状态 Badge

- 质量体系/产品检测/绿色环保/荣誉资质：低饱和度细边框 Badge。
- 有效、长期有效：品牌金背景/文字。
- 即将到期：警示色。
- 已过期：风险色。
- 展示中：品牌金。
- 已隐藏：弱色。

### 4.7 分页

分页采用更轻量的左右分区：左侧仅显示“共 x 个证书”；右侧显示“上一页 / 页码 / 下一页 / 每页显示 20条、50条、100条”。不展示跳页输入框。

## 5. 弹窗结构

Golden Reference PNG 默认展示“新增证书”弹窗覆盖页面，以同时表达页面与 CRUD 弹窗视觉。

- 宽度 760px。
- 最大高度 `calc(100vh - 80px)`。
- 居中，遮罩 `rgba(0,0,0,.62)`。
- Header、Footer 固定，Body 滚动。
- Panel 3px 圆角、0.5px 强分割线。

### 5.1 弹窗头部

- 标题：新增证书。
- 描述：维护证书资料、有效期与店主端展示设置。
- 右上角关闭按钮。

### 5.2 表单栅格

使用 12 列语义：

- 证书名称 8 列；证书排序 4 列。
- 证书类型 6 列；证书编号 6 列。
- 发证机构 12 列。
- 证书文件 12 列。
- 长期有效 12 列。
- 生效日期 6 列；到期日期 6 列。
- 前台展示 12 列。
- 备注 12 列。

HTML 原型以 CSS Grid 实现同等比例。

### 5.3 上传区成功态

Golden Reference 展示已选 PDF 的成功态，便于开发识别完整组件：

- 左侧 PDF 文档图标。
- 中间文件名、格式和大小。
- 下方上传完成进度条。
- 右侧“重新上传”“移除”。

上传区仍保留虚线边框和轻微品牌金底色。

### 5.4 Switch

采用工业化小尺寸 Switch：轨道 38×20，开启时品牌金，圆角只用于开关必要的胶囊形态。右侧提供名称和说明，不增加大块提示卡。

### 5.5 弹窗底部

右对齐：取消（Ghost）/ 保存证书（Primary）。保存中按钮文案改为“保存中…”，并禁用关闭与重复提交。

## 6. 交互说明

- 页面“新增证书”打开新增弹窗。
- 表格“编辑”打开编辑弹窗并回填。
- 长期有效开启：清空并禁用日期输入。
- 预览：图片 Lightbox，PDF 新窗口。
- 显示/隐藏：点击后二次轻确认，成功后原地刷新状态。
- 删除：强确认弹窗；成功后若当前页无数据且页码>1，回退一页。
- 指标卡片可点击筛选；hover 仅提升边框，不做明显位移。

## 7. 响应式

- 1024–1279px：主内容边距缩至 24–32px；指标 2×2；筛选区 2 行。
- <1024px：Sidebar 转为顶部/抽屉属于后台全局能力；本原型保持内容可读。
- <640px：弹窗宽度 `calc(100% - 32px)`；表单单列；Footer 按钮仍右对齐。
- 表格区域允许横向滚动，不压缩证书名称和操作到不可用。

## 8. 一致性检查

- Logo、导航、用户菜单结构与 brand-management.html V7 一致。
- 页面标题、眉标、描述、主按钮的字号和间距一致。
- Metric、Filter、Table、Pagination 复用同一组视觉规则。
- 输入框、Select、Textarea、Date、Upload、Switch、Button、Badge 均符合 Design Token。
- 无导出按钮、无批量操作、无大圆角、无高饱和多彩装饰。
- 品牌金未用于普通正文或大面积背景。

## 9. 开发交付映射

建议组件：

```text
BrandCertificatePage
├── AdminSidebar
├── BreadcrumbBack
├── BrandCertificateHeader
├── BrandSummaryCard
├── MetricGrid
├── CertificateFilterBar
├── CertificateTable
├── Pagination
└── CertificateFormDialog
    ├── CertificateFileUpload
    ├── IndustrialSwitch
    └── ModalFooter
```

建议状态：

```text
filters / pagination / metrics / list
formMode(create|edit) / formValues / validationErrors
uploadState(idle|uploading|success|error)
previewCertificate / deleteCertificate
```


## 7. 即时筛选与分页补充

- 筛选区不出现“查询”按钮。
- 关键词输入 300ms 防抖后自动筛选；Select 变化后立即筛选。
- “重置”保留在筛选区最右侧。
- 分页左侧为总数信息，右侧为完整分页操作，形成清晰的信息与操作分区。
- “上一页”“下一页”使用文字按钮；当前页使用品牌金实底。
