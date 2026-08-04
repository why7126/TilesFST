## 背景与动机

`BUG-0116-prod-media-historical-object-drift` 已评审通过。生产历史媒体数据存在 SKU 商品图片、品牌 Logo、品牌证书图片三条线的对象 Key 与缩略图规范漂移：公开 SKU 主图可能仍停留在 `images/default/tiles/pending/`，品牌 Logo 与证书图片可能缺少真实同目录 `.thumb` 缩略图，图片类证书可能仍保留在 `files/default/brand-certificates/`。

当前 `object-storage` 与 `media-acceptance-template` 已定义单 Bucket、标准前缀、真实缩略图和媒体 BUG 四联验收规则，但 BUG-0116 需要一个明确的修复型 Change，将历史数据审计、受控 apply、二次审计和验收回填组织成可执行闭环。该修复应复用 `add-prod-media-maintenance-jobs` 提供的生产维护入口，避免在开发机或临时脚本中直接 apply 生产数据。

## 变更内容

- 修改 `object-storage` 能力，新增 BUG-0116 历史媒体对象漂移修复场景，要求审计与修复覆盖 SKU、品牌 Logo、证书图片三类对象。
- 修改 `media-acceptance-template` 能力，补充 BUG-0116 的媒体四联验收输出要求，要求记录 dry-run、apply、二次审计、幂等和 fail / blocked 摘要。
- 要求实现阶段复用或对齐 `add-prod-media-maintenance-jobs` 的受控生产维护入口；若该入口尚未完成，BUG-0116 apply 必须阻塞在 dry-run 或本地等价测试阶段。
- 不新增用户可见页面，不新增对外 API，不直接执行真实生产维护任务，不提交生产 `.env`、备份、对象导出、客户数据或私有 URL。

## 影响范围

```yaml
impact:
  backend: true
  web: false
  miniapp: false
  admin: false
  database: true
  storage: true
  api: false
  deployment: true
  tests: true
```

- 后端：需要统一或补齐维护命令，覆盖历史 key 迁移、SKU pending 正式化和缩略图审计/回填。
- 数据库：受控 apply 会更新历史业务表中的媒体 key 与 URL；设计阶段不直接修改 schema。
- 对象存储：受控 apply 会 copy / put / stat 历史对象和缩略图；禁止未备份直接删除。
- 部署：生产执行应通过受控 maintenance 入口或与其兼容的 Compose 一次性命令。
- 测试：需要覆盖 dry-run 不写、apply 幂等、分流规则、脱敏输出和媒体四联验收摘要。

## 回滚计划

- apply 前必须确认 MySQL 快照和对象存储 bucket / prefix 快照已完成。
- 数据库引用回滚优先恢复 MySQL 快照；对象存储回滚优先恢复 bucket / prefix 快照。
- 若仅完成对象 copy 但数据库未更新，重复 apply 必须幂等识别目标已存在并继续或安全跳过。
- 若发现 PDF 或文档类证书被误迁移到 `images/`，必须停止后续 apply，恢复数据库与对象快照，并记录新的缺陷或返修任务。
- 若端侧 URL 或 render 验收失败，必须保留 dry-run/apply 摘要，按 BUG-0116 acceptance 的 fail / blocked 结构记录失败项，不得静默归档。
