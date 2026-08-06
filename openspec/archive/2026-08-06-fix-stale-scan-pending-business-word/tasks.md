## 任务清单

- [x] 调整 `scripts/sprint_close_stale_scan.py` 的 Issue 子文档中间态识别逻辑，区分普通业务正文与结构化状态上下文。
- [x] 保留 legacy archive path、active Change path、待 `/opsx-apply`、待 `/opsx-archive`、`proposed`、`applied`、`in_sprint`、`待验收`、`待实现`、`待归档` 等真实中间态阻断。
- [x] 在 `tests/test_sprint_close_stale_scan.py` 增加普通正文 `SKU pending 图片正式化` 放行回归测试。
- [x] 在 `tests/test_sprint_close_stale_scan.py` 增加结构化 `status: pending_review` 或 `acceptance_status: pending` 继续阻断的回归测试。
- [x] 验证 `python scripts/check-sprint-close-stale-scan.py --sprint <fixture>` 与 `python scripts/validate-sprint-archive-readiness.py --sprint <fixture>` 对该问题判断一致。
- [x] 运行聚焦测试：`python -m pytest tests/test_sprint_close_stale_scan.py`。
- [x] 运行 OpenSpec 文档语言校验：`python scripts/validate-openspec-language.py`。
- [x] 复核是否需要将该治理经验沉淀到 `docs/knowledge-base/incidents/`；本问题为流程治理脚本误报，未造成生产事故，暂不新增 incident。
