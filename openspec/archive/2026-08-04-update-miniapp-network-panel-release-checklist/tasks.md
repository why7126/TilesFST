## 1. 标准与命令文档

- [x] 1.1 更新 `docs/standards/miniapp-device-evidence-template.md`，新增 `network_devtools` 与 `network_trial` evidence 来源、字段、安全边界和示例。
- [x] 1.2 更新 `.agents/skills/miniapp-prepare/SKILL.md`，在 Gates / Output 中区分自动门禁与人工 Network checklist。
- [x] 1.3 更新 `.agents/skills/miniapp-confirm/SKILL.md`，说明确认记录需承接 DevTools Network、体验版 Network、阻塞项和剩余风险。
- [x] 1.4 更新 `src/miniapp/README.md`，补充 release/miniapp 准备中的 Network evidence 边界。

## 2. 脚本与测试

- [x] 2.1 更新 `scripts/miniapp-env.py` 的 `checklist()`，加入 DevTools Network 和体验版 Network 人工检查项。
- [x] 2.2 补充 `tests/test_miniapp_static.py` 或等价静态测试，确认 checklist 包含 Network evidence 项。
- [x] 2.3 补充测试断言，确认人工 Network checklist 不被描述为自动通过。

## 3. 验证与工作流

- [x] 3.1 运行 `uv run pytest tests/test_miniapp_static.py` 或聚焦小程序静态测试。
- [x] 3.2 运行 `python scripts/validate-openspec-language.py`。
- [x] 3.3 更新 Change trace / acceptance 记录，说明本 Change 不影响 API、数据库、Orval、Docker Compose 或小程序业务页面。
