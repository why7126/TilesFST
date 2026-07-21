## 1. 标准文档

- [x] 1.1 新增 `docs/standards/miniapp-device-evidence-template.md`，包含标准 frontmatter、背景、适用范围、术语和证据边界。
- [x] 1.2 在标准文档中提供 `miniapp_device_evidence` YAML 示例，覆盖 `template_ref`、`target`、`pages`、`evidence_items` 和 `summary`。
- [x] 1.3 在标准文档中提供 Markdown 表格示例，覆盖 DevTools、真机、自动化、N/A、blocked 和 follow-up 记录方式。
- [x] 1.4 在标准文档中写明 `required`、`passed`、`failed`、`blocked`、`not_applicable`、`follow_up` 六类状态含义和必填原因。

## 2. 设备证据字段与安全边界

- [x] 2.1 文档化 DevTools evidence 字段：开发者工具版本、基础库版本、模拟器设备、视口宽度、页面路径、关键 query、场景、截图/录屏/报告引用和结论。
- [x] 2.2 文档化真机 evidence 字段：设备型号、系统版本、微信版本、基础库版本、页面路径、用户状态、视口、安全区、状态栏、胶囊避让、执行人、执行时间、截图/录屏和剩余风险。
- [x] 2.3 文档化自动化/静态测试、脚本/单元测试、DevTools 预览和真机验收的不可替代边界。
- [x] 2.4 文档化 evidence 安全规则：禁止本机绝对路径、token、Cookie、Authorization header、`.env`、真实密钥、DSN、MinIO 凭据、真实客户数据和未脱敏隐私。

## 3. 流程引用与本 Change evidence

- [x] 3.1 在标准文档中给出 REQ `acceptance.md`、OpenSpec `tasks.md`、Change trace/acceptance、Sprint `acceptance-report.md` 和 release note 的引用示例。
- [x] 3.2 在本 Change `trace.md` 或 `acceptance.md` 中记录本 Change 的设备验收 N/A evidence：仅新增模板文档，不修改小程序运行时代码。
- [x] 3.3 引用 `docs/knowledge-base/retrospectives/sprint-008-retrospective.md` 中的小程序设备验收独立 Gate 经验。
- [x] 3.4 若实现阶段发现需要自动化截图、真机云测或命令 Skill 自动插入模板，停止扩大范围并输出 follow-up capture 文案，不在本 Change 内实现。

## 4. 校验

- [x] 4.1 补充或更新轻量校验，确认 `docs/standards/miniapp-device-evidence-template.md` 存在并包含关键字段、状态和安全禁止项。
- [x] 4.2 运行相关文档/规则校验脚本；若无专用脚本，至少运行覆盖本模板的新增测试或校验命令。
- [x] 4.3 运行 `openspec validate add-miniapp-device-evidence-template --strict` 并修复校验问题。
- [x] 4.4 确认本 Change 未修改 `src/miniapp/`、API、数据库、Orval、Docker Compose、MinIO 或环境变量。
