## 根因分析

`previous_usage_docs_version()` 使用目录名字符串排序选择候选版本。字符串排序不理解 SemVer 的 major、minor、patch 数值语义，因此 `v0.10.0` 与 `v0.9.0` 等版本在字典序下可能与真实版本先后不一致。

## 修复方案

1. 引入受控的 SemVer 解析函数，解析 `v<major>.<minor>.<patch>` 以及当前项目允许的后缀形式。
2. 扫描 `releases/` 版本目录时，只保留满足以下条件的候选：
   - 目录名可被 SemVer 解析；
   - 不是当前目标版本；
   - 存在 `usage-docs/manifest.json`；
   - 语义版本小于当前目标版本，或在无法安全比较扩展后缀时按明确规则处理。
3. 以 SemVer tuple 排序候选，选择小于当前版本的最大版本作为自动 `source_version`。
4. 若 `release.json` 已显式配置 `usage_docs.source_version`，继续尊重显式配置，但仍由后续校验保证 manifest 和页面集合有效。

## 边界规则

- 当前版本自身不得成为自己的来源版本。
- 相邻上一版本缺少 usage docs 时不得回退到模板页；应继续查找更早已生成 usage docs 的版本。
- 若没有任何历史 usage docs 版本，保持首次生成时使用模板页的行为。
- 带后缀版本必须有确定性排序策略；无法清晰定义的后缀不得静默参与错误排序。

## 测试策略

- 单元测试覆盖 `previous_usage_docs_version()` 对 `v0.9.0`、`v0.10.0`、`v0.11.0` 的选择。
- 单元测试覆盖缺失相邻 usage docs 版本时继续向前查找。
- 单元测试覆盖当前版本排除。
- 生成流程测试覆盖 `release.json usage_docs.source_version` 与 `usage-docs/manifest.json source_version` 一致。
- 保留现有 `v0.3.x` 版本继承行为回归。

## 风险与缓解

- 风险：后缀版本排序规则定义不清。缓解：测试中明确项目支持的后缀行为，不支持的格式应被排除或报错。
- 风险：测试创建 release 夹具时污染真实 `releases/`。缓解：使用临时目录或 monkeypatch 脚本常量，避免写入真实发布目录。
