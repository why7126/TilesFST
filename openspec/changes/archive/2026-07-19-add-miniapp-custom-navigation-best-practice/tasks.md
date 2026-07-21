## 1. 文档沉淀

- [x] 1.1 新增 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md`，包含适用范围、导航结构、状态栏与胶囊、返回兜底、页面 offset、截图验收矩阵、接入 checklist 和引用示例。
- [x] 1.2 在 best-practice 中引用 REQ-0048、REQ-0052 与 sprint-008 复盘，说明经验来源和复发预防点。
- [x] 1.3 更新 `docs/knowledge-base/README.md` 的最佳实践索引，加入小程序自定义导航 best-practice。

## 2. 验收矩阵与 evidence 边界

- [x] 2.1 在 best-practice 中定义页面、入口、DevTools 视口、真机类型、页面状态和结论字段的截图验收矩阵。
- [x] 2.2 明确 DevTools evidence 与真机 evidence 分层记录；无真机记录时不得写作真机通过。
- [x] 2.3 明确 `blocked`、`not_applicable`、`follow_up` 的填写要求和 N/A reason。
- [x] 2.4 明确截图、录屏、报告和人工摘要不得记录本机绝对路径、密钥、token、Cookie、`.env` 内容或真实客户隐私。

## 3. 流程引用

- [x] 3.1 在 Change trace 或 acceptance 中记录 best-practice 路径、REQ-0053 和 sprint-009 的追溯关系。
- [x] 3.2 确认 sprint-009 验收报告可引用 REQ-0053 的 AC-STRUCT、AC-SAFEAREA、AC-CAPSULE、AC-BACK、AC-OFFSET、AC-CHECK、AC-MATRIX、AC-SCOPE 与 AC-REF。
- [x] 3.3 不修改 `src/miniapp/`；若实现阶段发现必须修改自定义导航组件或页面源码，停止并补充 OpenSpec 范围说明。

## 4. 校验

- [x] 4.1 补充或更新轻量测试 / 脚本校验，确认 best-practice 文档存在且包含关键章节。
- [x] 4.2 校验文档不包含本机绝对路径、Authorization、Cookie、`.env` 或真实密钥示例。
- [x] 4.3 运行 OpenSpec 校验和项目相关文档校验，并记录结果。
