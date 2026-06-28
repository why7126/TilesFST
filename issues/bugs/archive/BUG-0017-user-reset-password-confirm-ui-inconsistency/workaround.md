---
bug_id: BUG-0017-user-reset-password-confirm-ui-inconsistency
status: pending_review
created_at: 2026-06-27 13:29:34
updated_at: 2026-06-27 13:29:34
---

# 临时规避方案

## 1. 操作习惯规避（推荐）

在正式修复前，重置密码功能仍可用；运营可采取：

1. 点击「重置密码」后，**务必阅读浏览器原生确认框**文案（「确认为用户 {username} 重置密码？」），勿习惯性点「确定」。
2. 重置前二次核对目标行用户名与角色，避免误重置他人密码。
3. 重置成功后，在 `ResetPasswordDialog` 中及时复制随机密码并安全交付；关闭后不可再次查看（REQ-0005 AC-023）。

## 2. 无产品内技术规避

本缺陷为纯前端 confirm **形态**不一致，**不存在**配置开关或环境变量可切换为 DS modal。

以下路径**不能**改为 DS confirm：

| 路径 | 说明 |
|---|---|
| 刷新页面 | 仍触发 `window.confirm` |
| 换浏览器 | 仍为原生 confirm，仅样式略有差异 |
| 仅走 API 文档 | 绕过 UI 不能作为运营规避 |

## 3. Golden Reference 对照

若需确认「正确交互」参考：

- **瓷砖类目** `/admin/tile-categories`：启用/停用 confirm modal（REQ-0007）。
- **用户管理同页** 冻结/解冻 confirm modal（BUG-0016 已交付）。

培训时可说明：重置密码确认仍为浏览器弹窗，修复前与同页其他操作视觉不一致。

## 4. 验收规避

修复前相关验收应标注：

- 重置密码 **功能结果**（API 成功、结果弹窗展示密码、复制按钮）可单独验证通过；
- **确认 UI 与类目启停 modal 一致** 应标记为本 BUG 未通过项；
- 冻结/删除 modal、类目/品牌启停 confirm **不应** 计入本 BUG 未通过（已交付或独立 scope）。

## 5. 规避有效期

- **有效期**：自 2026-06-27 起至 `fix-user-reset-password-confirm-ui` 发布并验收通过。
- **修复后**：重置密码确认 MUST 使用 DS modal；本规避仅作修复前参考。

## 6. 风险说明

| 风险 | 说明 |
|---|---|
| 误操作 | 误点原生 confirm「确定」会重置密码；需重新交付新密码给用户 |
| 功能 | **不阻断**；仍有二次确认门槛（原生） |
| 安全/数据 | 无权限绕过；无数据损坏 |
| 关联 | BUG-0016（同页冻结/删除 modal）职责独立；可同 Sprint 编排 |

severity **medium**，建议独立 `fix-*` change 发布，MUST NOT 与 BUG-0016 change 混 scope。
