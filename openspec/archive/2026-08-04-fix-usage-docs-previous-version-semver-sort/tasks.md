## 1. 版本选择逻辑

- [x] 1.1 为 usage docs 来源版本选择增加 SemVer 解析与比较逻辑。
- [x] 1.2 调整 `previous_usage_docs_version()`，只从已生成 `usage-docs/manifest.json` 的历史版本中按 SemVer 语义选择最近版本。
- [x] 1.3 保持显式 `usage_docs.source_version` 覆盖能力，并确保当前版本自身不会成为来源版本。

## 2. 回归测试

- [x] 2.1 增加测试覆盖 `v0.9.0`、`v0.10.0`、`v0.11.0` 的 SemVer 顺序。
- [x] 2.2 增加测试覆盖相邻上一版本缺少 usage docs 时继续向更早版本查找。
- [x] 2.3 增加测试覆盖当前版本排除和首次生成模板页 fallback。
- [x] 2.4 增加生成流程测试，确认 `release.json` 与 `usage-docs/manifest.json` 的 `source_version` 一致。

## 3. 文档与校验

- [x] 3.1 如脚本行为说明发生变化，同步更新 `releases/README.md` 或相关发布治理文档。
- [x] 3.2 运行相关 pytest、`python scripts/validate-openspec-language.py` 和必要的 OpenSpec 校验。
- [x] 3.3 评估是否需要沉淀到 `docs/knowledge-base/incidents/`；若不适用，在归档或验收输出中说明原因。
