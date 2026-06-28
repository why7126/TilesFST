## Why

`BUG-0003-brand-image-display-layout-shift` 已评审通过并纳入 `sprint-002`。瓷砖品牌管理页存在两类高感知缺陷：

1. `/admin/brands` 上传品牌 Logo 后，品牌列表页和品牌编辑弹窗均不能正常展示已上传图片。
2. 品牌状态变更后，页面顶部 Tips 临时插入并在几秒后消失，导致页面主体上下波动。

根因已在 `issues/bugs/archive/BUG-0003-brand-image-display-layout-shift/root-cause.md` 中确认：品牌上传和品牌列表接口返回 `/media/{object_key}`，但当前后端未挂载可访问媒体服务或受控代理；同时 `admin-notice` 作为普通文档流节点条件渲染，自动消失时改变页面高度。

品牌 Logo 是品牌主数据的关键展示字段。若上传后无法展示，运营无法确认素材是否生效；提示布局波动则影响连续维护品牌数据的操作稳定性。因此需要以 `fix-*` OpenSpec Change 承载修复，禁止绕过规范直接改代码。

## What Changes

- 补齐品牌 Logo 上传后的可访问媒体 URL 链路：
  - 明确 `/media/{object_key}` 受控访问策略，或改为返回可实际加载的等价 `url` / `preview_url`。
  - 保持上传经过后端鉴权、MIME 校验和对象 Key 生成，不允许前端直连未授权对象存储。
  - 品牌列表与编辑弹窗必须使用可访问 URL 正常展示/回显 Logo。
- 修复品牌页自动消失提示的布局策略：
  - 品牌启用、停用、删除、创建、更新后的提示不得推挤页面主体。
  - 可采用固定 toast、稳定预留提示区域或等价非位移方案。
- 补充回归测试与验收：
  - 覆盖上传返回 URL、列表 Logo 渲染、编辑弹窗 Logo 回显。
  - 覆盖状态提示不使用会推挤页面主体的文档流插入模式。
  - 若 API 响应结构变化，必须同步 OpenAPI 与 Orval。

## Impact

| 影响面 | 说明 |
|---|---|
| Web 管理端 | `/admin/brands` 列表 Logo 展示、品牌弹窗 Logo 回显、状态提示布局 |
| 后端 API | 可能涉及上传返回 URL 或媒体访问代理；若响应结构变化需同步 OpenAPI |
| 媒体 / MinIO | 补齐品牌 Logo object_key 到可访问 URL 的闭环，遵守单桶与前缀策略 |
| 数据库 | 不新增字段；继续使用 `brands.logo_object_key` |
| Orval | 若 API schema 或接口响应变化则必须重新生成；若仅补 `/media` 代理且 schema 不变则不需要 |
| Docker | 若新增后端媒体服务或 Web/Nginx 代理，需要 Docker Compose 环境验证 |
| 小程序 | 不直接修改；媒体访问策略应避免破坏后续小程序复用 |

## Rollback Plan

若修复引起品牌管理或媒体访问异常，可按以下顺序回滚：

1. 回滚本 change 中后端媒体访问代理、URL 生成或上传响应变更。
2. 回滚品牌页提示布局修改，恢复修复前 `admin-notice` 行为。
3. 回滚前端品牌 Logo 展示/回显相关改动。
4. 若执行了 Orval，回滚生成客户端到变更前版本。
5. 数据库不涉及结构变更，无需数据迁移回滚。

回滚后保留 BUG 与 OpenSpec 记录，重新评估替代媒体访问策略。
