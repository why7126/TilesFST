## 上下文

`REQ-0115` 已建立 `thumbnail`、`display`、`original` 三规格语义，`system-settings` 已提供 media 分组和 `thumbnail_max_size_kb` 缩略图体积目标配置。当前缺口是 display 图体积目标仍由后端常量固定为 768KB，导致管理端无法调整详情普通展示图策略，也容易让缩略图配置被误用为 display 配置。

REQ-0119 已纳入 `sprint-025`，状态为 `in_sprint`，readiness 为 `Partially Ready`：六件套齐全，存在轻量 HTML/context 原型，PNG、Skeleton 截图和 computed style evidence 留到 `/opsx-apply` 阶段按 UI Contract 补证。

## 目标与非目标

**目标：**

- 新增 display 图体积目标配置，默认 effective 值为 `768` KB。
- 字段与 `thumbnail_max_size_kb` 独立，互不覆盖、互不推导。
- 新上传、SKU pending 正式化和维护任务重生成 `.display` 时读取同一 effective 配置。
- 管理端系统设置媒体页新增字段，并满足表单页横切一致性。
- 同步 API、OpenAPI、Orval、文档和聚焦测试。

**非目标：**

- 不改变 `.thumb` / `.display` / original 同目录 key 或 URL 模型。
- 不在保存系统设置时自动重建历史 `.display` 对象。
- 不为 SKU、品牌、Banner、证书等资源分别提供单独 display 体积目标。
- 不新增 WebP 转换策略、视频多清晰度、视频封面体积配置或独立媒体处理控制台。
- 不重做商品详情、图册、列表或上传组件视觉布局。

## 原型冲突处理

事实源优先级为：`prototype/web/system-settings-media-display-size.html` > `prototype/web/context.md` > `acceptance.md` > `rules/ui-design.md` > 已归档 `system-settings` spec。

- 原型建议字段文案为「详情展示图体积目标上限 (KB)」，OpenSpec 采用该中文文案；代码字段命名采用 `display_max_size_kb`，避免与缩略图字段混淆。
- 原型里缩略图示例值为 `0`，本 Change 不修改缩略图默认语义；display 默认值固定为 `768`。
- 原型使用静态 CSS 和局部 token 示例，实际实现必须使用项目 Design System semantic token 与既有系统设置组件，不复制裸 Hex。
- 原型只展示默认/保存入口，不覆盖 Skeleton、截图、computed style 和真实 API evidence；这些证据在实现阶段补齐。

## UI Contract

| 项 | 合同 |
|---|---|
| 事实源优先级 | HTML 原型 > context.md > acceptance.md > `rules/ui-design.md` > 既有系统设置 spec。冲突时以字段语义、默认值和非自动重建边界优先。 |
| 页面与入口 | 管理端 `role=admin` 访问 `/admin/settings/media`；`employee` 不可访问系统设置；不新增独立页面或菜单。 |
| 信息架构 | 保持 `page-hero`、`summary-grid`、`settings-layout`、`settings-nav`、`settings-panel` 和 `settings-panel-footer`；新字段放在 media 上传限制 / 图片生成策略区域，与缩略图体积目标相邻。上传限制 2 列网格按语义分四行：图片最大尺寸 / 视频最大尺寸，文件最大尺寸 / 空位，缩略图体积目标上限 / 详情展示图体积目标上限，支持图片格式 / 支持视频格式。 |
| 视觉 token | 使用既有暗色旗舰风 semantic token、表单控件、字段帮助文本、错误文本、footer 和 fixed toast；禁止裸 Hex；使用 `cn()` 合并 className。 |
| 交互状态 | 覆盖加载、编辑 dirty、保存成功、保存失败、字段校验失败、恢复默认、dirty 切换 Tab 确认、disabled/loading/focus。 |
| 图标与文案 | 字段文案优先「详情展示图体积目标上限 (KB)」；帮助文案必须说明默认 768KB、仅影响新生成 display 图、历史需维护任务重生成、与缩略图目标独立。 |
| Mock/API 边界 | 实现阶段必须接入真实系统设置 API；不得用静态 mock 声称验收通过。若某 evidence 使用示例图片，必须标注为脱敏样例。 |
| 权限规则 | 全部系统设置 media API 使用 `require_system_admin` 或等价管理员权限；响应不得暴露对象存储密钥、bucket 权限细节、内部 endpoint 或本机路径。 |
| 一致性参照 | 对齐 `system-settings` 页面规范、管理端表单横切最佳实践、媒体上传链路最佳实践和对象存储四联验收模板。 |

## 设计决策

### 决策 1：字段命名采用 media 分组内 `display_max_size_kb`

`display_max_size_kb` 与现有 `thumbnail_max_size_kb` 对称，表达“生成 display 图时尽量控制的 KB 目标”。它不包含 `image` 中缀，避免后续 media 分组字段过长；对外文案用「详情展示图」降低非技术用户理解成本。

### 决策 2：默认值为 768，且不支持用缩略图字段兜底

默认值沿用现有硬编码 display 目标，避免升级后改变既有生成效果。若数据库没有覆盖值，effective settings 返回 `768`；不得从 `thumbnail_max_size_kb` 推导 display 目标。这样能保持列表图和详情图策略独立。

### 决策 3：字段范围在实现阶段收敛为可验证契约

实现阶段应在 Pydantic Schema 和前端表单中定义一致范围。若采用 `0` 表示不限制，必须让 GET、PATCH、reset、帮助文案、测试和文档同时表达该语义；若不支持 `0`，应使用正整数范围并提供字段级错误。

### 决策 4：生成链路每次读取 effective 配置

上传、SKU pending 正式化和维护任务重生成 `.display` 时应读取当前 effective 配置，避免仅在进程启动时读取常量。若生成结果无法达标，不阻断原图上传或业务保存，但必须记录 warning、失败原因或维护任务摘要。

### 决策 5：历史对象只通过维护任务处理

保存系统设置不得自动扫描对象存储、读取历史原图、覆盖 `.display` 对象或触发批处理。历史 display 策略调整必须走 dry-run / apply 两阶段维护任务，并在 apply 前保留备份、风险和幂等边界。

## 风险与取舍

- display 目标值配置过低可能影响详情图清晰度 → 管理端帮助文案说明这是“目标上限”，实现记录无法达标 warning，验收覆盖 render。
- 字段与缩略图配置混用会伤害列表性能或详情清晰度 → API、Schema、UI 和测试必须验证两个字段互不影响。
- 保存设置误触发历史重建会造成对象存储 I/O 和缓存抖动 → spec 和测试明确禁止保存时自动重建。
- OpenAPI / Orval 漏同步会导致前端类型漂移 → tasks 将生成物和 API 文档同步作为独立检查项。
- PNG / 复杂透明图可能无法达到目标体积 → 生成失败不阻断业务保存，但需要 warning 或维护任务失败原因。

## 迁移与回滚

- 部署时新增配置默认值 `768`，已有系统设置记录缺字段时通过 effective merge 返回默认值。
- 若使用 KV 表，不新增业务表；如存在默认 seed 或迁移脚本，必须同步 display 默认值。
- 回滚时可移除管理端字段和 API schema 字段，后端 display 生成恢复 768KB 常量；不得删除已生成的 `.display` 对象。
- 若维护任务已按新目标重生成历史对象，回滚不自动恢复对象内容，需按对象存储备份和维护 runbook 单独处理。

## 待实现收敛

- `display_max_size_kb` 是否允许 `0` 表示不限制。
- 字段允许范围采用 `1-2048KB`、`0-2048KB` 或其他值。
- 对 PNG / WebP / JPEG 未达标 warning 的记录入口。
- 维护任务是否仅复用既有多规格重生成任务，或补充 display-only 统计项。
