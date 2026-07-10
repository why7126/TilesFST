---
created_at: 2026-07-07 00:04:42
updated_at: 2026-07-07 00:04:42
---

# Test Plan

## Backend

- `src/backend/tests/test_password_change.py`
  - 新增/更新策略失败详情测试：长度不足、超过最大长度、缺少大写、缺少小写、缺少数字、缺少特殊字符。
  - 保留弱密码 `40022`、同原密码 `40023`、原密码错误 `40020`、限流 `42901`、受保护账号 `403` 回归。
  - 若错误响应 `data` 增加结构化字段，断言字段稳定且不包含明文密码。

## Frontend

- `src/web/src/features/admin/components/ChangePasswordModal.test.tsx`
  - 断言具体策略失败文案展示在新密码字段或规则区。
  - 断言默认 effective 策略下规则包含 12 位、大小写、数字、特殊字符。
  - 断言 API 返回策略失败详情时，前端显示具体失败项。
  - 断言原密码错误、确认密码不一致、受保护账号 message、成功提交无回归。

## Contract / Generated Client

- 若 OpenAPI schema 变化：
  - 运行 `./scripts/generate-openapi-client.sh`。
  - 检查 `src/web/openapi.json` 和 Orval 生成代码 diff。
  - 确认生成文件未手工编辑。

## Commands

```bash
uv run pytest src/backend/tests/test_password_change.py
pnpm --dir src/web vitest run src/features/admin/components/ChangePasswordModal.test.tsx
openspec validate fix-change-password-policy-error-message --strict
python scripts/validate-directory-structure.py
```

