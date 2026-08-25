## 1. Trace frontmatter 写入修复

- [x] 1.1 复现并固定 `REQ-0120-webp-derived-image-variants/trace.md` frontmatter 非法 YAML 样本，记录标准 parser 失败点。
- [x] 1.2 修复 `scripts/workflow_sync/patch.py` 的 Issue trace frontmatter 写入逻辑，确保 `lifecycle.generated`、`openspec_changes[]`、`related_changes` / `related_change` 等字段写入后结构合法。
- [x] 1.3 确保写入后使用标准 YAML parser 或等价校验阻止非法 frontmatter 落盘。
- [x] 1.4 确保顶层 Issue `status` 与 `openspec_changes[].status` 语义隔离，项目解析器不再把内层状态提升为顶层状态。

## 2. 已知样本修复

- [x] 2.1 修复 `issues/requirements/archive/REQ-0120-webp-derived-image-variants/trace.md` frontmatter 的缺父键缩进列表项。
- [x] 2.2 校验修复后的 `REQ-0120` frontmatter 可被标准 YAML parser 解析。
- [x] 2.3 校验项目解析器读取 `REQ-0120` 后顶层 `status` 仍为 Issue 主状态，`openspec_changes[].status` 仍为 Change 状态。

## 3. 回归测试

- [x] 3.1 补充 `req.generate` / `bug.generate` frontmatter 合法性和 `lifecycle.generated` 父子结构测试。
- [x] 3.2 补充 `req.opsx` / `bug.opsx` linked Change 回填 frontmatter 合法性、父键存在和幂等测试。
- [x] 3.3 补充 `opsx.apply` 更新 Change 状态时顶层 Issue 状态不漂移测试。
- [x] 3.4 确认测试不只断言 `generated:` 或 `change_id:` 出现次数，还断言标准 YAML parser 可解析和结构语义正确。

## 4. 文档与验证

- [x] 4.1 运行聚焦 pytest，覆盖 Workflow Sync trace frontmatter 回归。
- [x] 4.2 运行 `python scripts/validate-openspec-language.py`。
- [x] 4.3 运行 `openspec validate fix-workflow-sync-trace-frontmatter-invalid-yaml --strict`。
- [x] 4.4 运行 `python scripts/validate-directory-structure.py`。
- [x] 4.5 回填 BUG-0138 trace、acceptance 与 Change trace，记录验证命令、结果和剩余风险。
- [x] 4.6 说明本 Change 不影响 API、数据库、Web、小程序、管理端，不需要 Orval 和 Docker Compose 验证。
