---
created_at: 2026-09-10 20:38:13
updated_at: 2026-09-10 22:51:56
---

# 知识模型生命周期操作

## 固定来源与提交边界

Python 3.12 和项目既有 PyYAML 提供本地工具运行环境。格式契约为 `tilesfst-structural-v1` 的显式子集，不声称实现 JSON Schema、OWL 或推理引擎。模型只支持声明式 eq、in、exists、all 条件；缺值返回 unknown。

先完成 OpenSpec 归档及 Issue promotion，再自动同步。工具核对源文件与指定 Git Commit 的字节一致性，包括本体、映射、覆盖和归档资料。归档新增文件尚未进入 Git 时返回 `source_revision_pending`；既有模型不变，归档成果不回滚。按项目 Git 流程提交来源后重试，不由工具自动提交用户工作区。

```bash
python scripts/validate-knowledge-model.py
python scripts/sync-knowledge-model.py sync --change add-knowledge-model-lifecycle-sync --revision HEAD --dry-run
python scripts/sync-knowledge-model.py sync --change add-knowledge-model-lifecycle-sync --revision HEAD
python scripts/validate-knowledge-model.py check --sprint sprint-030
```

已归档 Change 的恢复入口为 sync。独立 Change 和多 Change Issue 均按 Change 身份处理；Issue 未整体归档时允许引用 review 中的主文档，随后迁移产生的路径漂移必须重验。普通移动文件和 PR 不触发生成。

## 事务与恢复

trace 来源使用 knowledge-trace-v1 规范化，仅忽略工具回执区与 updated_at；其余内容仍与来源 Commit 比对。每条事实携带本体版本与映射版本。

每个 Change 持有自己的抽取结果；新增同步在锁内合并，重复事件按规范化摘要收敛到同一 generation。ID 在命名空间中稳定，跨 Change 不允许含糊覆盖同一事实；共享事实需由一个映射负责，其他映射建立引用。映射删除对象会移除旧事实，必要反向引用无法解析时阻断。Python 符号绑定文件路径与符号名，禁止按裸名称合并。

`generated/generations/<sha256>/` 保存不可变完整代，`generated/current.yaml` 经 os.replace 原子切换。读者先读指针再读取不可变代。切换前错误不改变正式指针；切换后回执失败重试补记，既有代不重复生成。写进程由 fcntl 文件锁串行化。此实现保障进程并发与进程异常恢复，不承诺断电后的文件系统持久性事务。

运行回执位于 Git 忽略的 `data/knowledge-model/runs/`，只保留错误码、数量、标识和摘要；不写异常堆栈、原文、密钥或客户运行实例。Change trace 写同步摘要；Sprint 已冻结时只写运行回执，不反向修改冻结 trace。回执默认保留30天，可运行：

```bash
python scripts/sync-knowledge-model.py cleanup
```

历史 generation 保守保留以保护读者；已发布快照不被清理。手工篡改 generated 会阻断校验，先恢复版本控制中的完整代，再重试同步。覆盖项必须由人工确认并绑定当前 source sha256，来源变化后拒绝复用旧审核。

## Sprint 门禁

Sprint readiness 的预归档阶段允许 active Change 尚未生成；已归档且在覆盖范围内的 Change 必须同步且来源未漂移，最终关闭前再次检查所有 Change。类型、必要关系、循环、来源或同版本同条件强规则冲突阻断。candidate 不作强规则推断；缺失条件不直接推断冲突。显式低风险异常只告警，高风险异常阻断。

同步失败由工具写入 `unresolved/sync-<change>.yaml` 并在成功重试时置为 resolved。其他未决项使用 `unresolved/*.yaml` 的 items 列表，每项包含 id、change、risk（high/low）、status（open/resolved/dismissed）、reason、source。记录由人工审阅，不自动把自然语言候选升级为强规则。

## 发布快照

```bash
python scripts/sync-knowledge-model.py prepare --release vX.Y.Z
python scripts/sync-knowledge-model.py snapshot --release vX.Y.Z
python scripts/sync-knowledge-model.py bind --release vX.Y.Z
```

prepare 生成 manifest、entities、relations、rules 四个文件。manifest 记录产品版本、格式/元本体/领域版本、快照摘要、Release/Sprint/Change、各 Change 输入 Commit、所有模型/映射依赖摘要及其原始内容，支持历史还原。当前每快照最多100文件、合计10MiB、单文件2MiB，由 registry 调整。工具不自动 git add/commit；由发布准备的仓库提交流程纳入完整快照。

同输入重复 prepare 返回既有快照。候选范围或输入变化返回 drift，先核对并移除尚未发布的候选目录后再 prepare；已确认发布的版本禁止替换。publish 只校验和绑定候选到 release.json knowledge_model，正式发布状态仍由 publish_confirmation 表达，计划、标签或绑定本身都不代表已发布。历史已发布快照按自身内容验证，不依赖当前领域版本。

## 验证边界

pytest 隔离仓库使用真实 SKU 规格、API 文件和 OpenAPI 作为只读输入，验证同步故障与发布编排。真实 Change 归档、Sprint 关闭和产品发布由相应命令补充证据，不以隔离预演冒充正式验收。无需 API、SQLite/MySQL、Pydantic、Orval、Web、小程序或 Docker Compose 变更。product_data_collection_observability 为 N/A：只有本地治理回执，没有产品请求或运行时采集。
