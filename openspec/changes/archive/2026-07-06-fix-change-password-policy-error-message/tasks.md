---
created_at: 2026-07-07 00:04:42
updated_at: 2026-07-07 00:28:52
---

# Tasks

## 1. Baseline

- [x] 1.1 确认 BUG-0061 文档包位于 `issues/bugs/archive/BUG-0061-change-password-policy-error-message-unclear/`，状态为 `in_sprint`。
- [x] 1.2 复现当前“新密码不符合安全策略”泛化提示路径，并记录触发样例：长度不足、缺少特殊字符、满足前端旧规则但不满足后端 effective 策略。
- [x] 1.3 确认当前 effective 密码策略事实源：`security.password_min_length`、`require_uppercase`、`require_lowercase`、`require_digit`、`require_special`。

## 2. Backend / API

- [x] 2.1 调整密码策略校验，返回具体失败项（长度、大小写、数字、特殊字符、弱密码、同原密码）。
- [x] 2.2 调整改密服务错误抛出逻辑，保持既有错误码语义，并提供前端可识别的具体失败信息。
- [x] 2.3 确认受保护账号、原密码错误、限流、弱密码、同原密码路径无回归。
- [x] 2.4 若 API 错误响应结构变化，更新 Pydantic/OpenAPI schema。

## 3. Web Admin

- [x] 3.1 调整 `ChangePasswordModal`，展示与当前 effective 策略一致的规则提示或在失败后展示服务端具体失败项。
- [x] 3.2 调整 API 错误映射，使策略失败详情显示在新密码字段或规则区。
- [x] 3.3 保持原密码错误在原密码字段、确认不一致在确认字段、受保护账号和限流 message 可理解展示。
- [x] 3.4 确保错误提示不引发布局明显抖动，且错误区域具备可访问语义。

## 4. Docs / OpenAPI / Orval

- [x] 4.1 若 API schema 变化，运行 `./scripts/generate-openapi-client.sh`。
- [x] 4.2 同步 `docs/03-api-index.md` 修改密码错误响应说明。
- [x] 4.3 按需同步错误码或 API governance 文档，说明策略失败详情字段。
- [x] 4.4 确认 Orval 生成文件未被手工编辑。

## 5. Regression Tests

- [x] 5.1 后端测试覆盖长度不足、超过最大长度、缺少大写、缺少小写、缺少数字、缺少特殊字符。
- [x] 5.2 后端测试覆盖弱密码、同原密码、原密码错误、限流、受保护账号不可改密无回归。
- [x] 5.3 前端测试覆盖具体策略失败提示可见，且不再只展示泛化“新密码不符合安全策略”。
- [x] 5.4 前端测试覆盖规则展示/错误提示与有效策略一致（至少覆盖默认 12 位 + 大小写 + 数字 + 特殊字符）。
- [x] 5.5 前端测试覆盖成功改密流程、确认密码不一致、受保护账号 message 无回归。

## 6. Validation

- [x] 6.1 运行后端修改密码相关 pytest。
- [x] 6.2 运行前端 `ChangePasswordModal` 相关 Vitest。
- [x] 6.3 如 API schema 变化，运行 OpenAPI/Orval 生成并检查 diff。
- [x] 6.4 运行 `openspec validate fix-change-password-policy-error-message --strict`。
- [x] 6.5 运行 `python scripts/validate-directory-structure.py`。

## 7. Trace / Knowledge

- [x] 7.1 更新 BUG-0061 trace，记录 apply 结果、测试结果和验收状态。
- [x] 7.2 更新 sprint-005 acceptance-report 中 BUG-0061 验收项。
- [x] 7.3 若修复暴露可复用模式，补充 `docs/knowledge-base/incidents/` 或 Sprint 复盘行动项。
