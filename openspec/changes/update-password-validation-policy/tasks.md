## 1. 后端密码策略

- [ ] 1.1 定位现有密码校验函数和随机密码生成器，确认修改密码、创建用户、重置密码的调用路径。
- [ ] 1.2 将统一基础密码策略调整为 5-32 位、包含 ASCII 英文字符、包含 ASCII 数字。
- [ ] 1.3 更新策略失败项，至少输出 `min_length`、`max_length`、`missing_letter`、`missing_digit`。
- [ ] 1.4 确认弱密码表、限流、新旧密码不得相同、受保护账号、token_version 失效逻辑不回退。

## 2. API 与管理端集成

- [ ] 2.1 更新 `POST /api/v1/admin/profile/password` 的策略错误 message / data，使前端可识别具体失败项。
- [ ] 2.2 更新用户创建初始密码生成，确保 `data.initial_password` 满足新规则。
- [ ] 2.3 更新管理员重置密码生成，确保 `data.password` 满足新规则。
- [ ] 2.4 如 OpenAPI schema、错误码或 API 文档示例受影响，同步 OpenAPI、Orval、`docs/03-api-index.md` 与错误码文档。

## 3. Web 管理端提示与交互

- [ ] 3.1 更新修改密码弹窗规则提示为 5-32 位、英文字符、数字。
- [ ] 3.2 搜索并清除管理端密码相关旧提示：`8-32 位`、大小写、特殊字符等不再适用文案。
- [ ] 3.3 确保字段级错误显示在对应密码字段或规则区，不只依赖全局 Toast。
- [ ] 3.4 按 `admin-form`、`admin-modal` 横切 AC 检查 fixed toast、无原生 confirm、520px computed width、矮视口 body scroll。

## 4. 测试与验收

- [ ] 4.1 后端测试覆盖 4 位失败、5 位成功、32 位成功、33 位失败。
- [ ] 4.2 后端测试覆盖纯英文失败、纯数字失败、英文数字成功、符号加英文数字成功。
- [ ] 4.3 API 测试覆盖修改密码策略失败不更新 hash / 不递增 token_version。
- [ ] 4.4 API 测试覆盖创建用户和重置密码生成结果满足新规则。
- [ ] 4.5 前端测试覆盖修改密码弹窗规则提示、具体错误提示和旧文案清除。
- [ ] 4.6 运行相关 pytest / Vitest；如触及 Orval，运行生成和类型校验。

## 5. 文档与追溯

- [ ] 5.1 更新 change `trace.md` 的验收 evidence 与 PNG/HTML checklist 结果。
- [ ] 5.2 更新 REQ trace / Workflow Sync 状态。
- [ ] 5.3 实现完成后准备 `/opsx-archive` 所需 acceptance 和测试摘要。
