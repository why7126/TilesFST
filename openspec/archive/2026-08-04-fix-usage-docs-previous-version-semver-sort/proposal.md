## 背景

BUG-0111 指出 `scripts/generate-usage-docs.py` 的 `previous_usage_docs_version()` 当前通过字符串排序选择前一个已生成 usage docs 的版本。该策略在 `v0.3.4`、`v0.3.5` 这类同位数版本中表现正常，但当版本进入 `v0.10.0`、`v0.9.0` 等 SemVer 位数变化场景时，字典序可能与语义版本顺序不一致，导致新版本继承错误的 usage docs 页面基线。

版本化产品使用文档要求当前版本优先继承前一个已生成 usage docs 版本的完整页面集，因此来源版本选择必须稳定、可测试，并且在相邻版本未生成 usage docs 时继续向更早版本查找。

## 变更内容

- 将 usage docs 自动来源版本选择从字符串排序改为 SemVer 语义排序。
- 自动候选只包含已生成 `releases/<version>/usage-docs/` 且具备 manifest 的版本，并排除当前目标版本自身。
- 当相邻上一版本没有 usage docs 时，继续向更早的已生成 usage docs 版本查找。
- 保持显式 `usage_docs.source_version` 的覆盖能力，供特殊维护或人工确认场景使用。
- 增加回归测试覆盖 `v0.9.0`、`v0.10.0`、缺失相邻版本、排除当前版本和现有 `v0.3.x` 兼容场景。

## 能力范围

### 新增能力

- 无。

### 修改能力

- `product-release-management`：修正版本化产品使用文档的来源版本自动选择规则，要求按 SemVer 语义选择最近的已生成 usage docs 版本。

## 影响范围

- 影响 `scripts/generate-usage-docs.py` 的 usage docs 来源版本选择逻辑。
- 影响发布文档生成测试夹具和相关 pytest。
- 不影响业务 API、数据库表结构、Web 前端、微信小程序、管理端、MinIO、Orval 生成物或 Docker Compose 部署。

## 回滚计划

- 若 SemVer 解析引入不兼容行为，可临时回退到人工显式配置 `usage_docs.source_version` 的规避方案。
- 若自动选择逻辑回滚，必须保留或补充发布操作说明，要求 `v0.10.0` 之后的版本生成 usage docs 前人工确认 `source_version`。
- 回滚不得删除已生成版本的 `usage-docs/` 快照或 `manifest.json`，已生成错误来源的版本需通过显式维护记录更正。
