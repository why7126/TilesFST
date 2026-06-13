# AI 审查 UI 提示词

审查 Web UI 变更时检查：

## Design Token

- [ ] 是否使用 semantic class 而非 Hex
- [ ] 是否出现 `#18160F`、`#C8A055`、`bg-[#...]` 等硬编码
- [ ] 圆角是否使用 `rounded-industrial` / `rounded-card`

## 组件

- [ ] 是否绕过 `shared/templates`、`shared/business`、`shared/ui`、`components/ui`
- [ ] 是否重复实现已有组件
- [ ] 登录页是否对齐 `user-login.md` 原型

## 规范一致性

- [ ] 与 `rules/ui-design.md` 是否冲突
- [ ] Token 修改是否同步 `globals.css` 或 `pnpm sync:tokens`
- [ ] 是否可在 `/design-system` 预览验收

## 输出

列出违规文件、行号、原因与修复建议。可运行：

```bash
python scripts/validate-design-system.py
```
