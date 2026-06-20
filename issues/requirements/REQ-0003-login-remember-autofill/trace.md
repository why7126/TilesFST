---
title: 需求追踪
purpose: REQ-0003-login-remember-autofill 分析与追溯（含 /requirement-to-change 产出）
content: 关联文档、影响分析、建议 Change、测试映射
source: AI 根据 PRD 生成，项目团队确认
update_method: 状态或迭代变更时同步更新
owner: product
status: done
note: add-login-remember-autofill archived（2026-06-20）
readiness: ready
---

# 需求追踪

## 1. Requirement Readiness Report

| 检查项 | 结果 |
|---|---|
| `requirement.md` | ✓ |
| `user-stories.md` | ✓ |
| `business-flow.md` | ✓ |
| `acceptance.md` | ✓ |
| `trace.md` | ✓ |
| `prototype/web/login-form-enhancements-context.md` | ✓ |
| 状态 / 优先级 / 负责人 / 来源 | ✓（见 §2） |
| 用户故事与 FR 映射 | ✓ |
| 可测试验收标准（AC） | ✓ AC-001 ~ AC-021 |
| 实现触点与代码基线 | ✓ |

**结论：Ready** — 可进入 `/requirement-to-opsx`（用户本次不要求创建 OpenSpec）。

> **编号说明**：本项目存在两个 `REQ-0003-*` 目录（`login-left-panel-refine` 与 `login-remember-autofill`），以完整目录名区分，互不覆盖。

---

## 2. 基本信息

```yaml
requirement_id: REQ-0003-login-remember-autofill
requirement_name: login-remember-autofill
requirement_type: 管理端 / 登录体验 Enhancement
priority: P1
status: done
owner: 产品负责人
source: 产品对管理端登录页交互优化（记住凭证自动填充 + 密码显隐）
target_users:
  - 企业内部员工（运营、管理员）
target_clients:
  web_admin: 本期
  web_catalog: 不涉及
  wechat_miniapp: 不涉及
iteration: sprint-002
change_type: Enhancement
suggested_change_id: add-login-remember-autofill
openspec_changes:
  - change_id: add-login-remember-autofill
    type: add
    status: archived
    iteration: sprint-002
    requirement_id: REQ-0003-login-remember-autofill
    strategy: login-css-port-extension
related_requirements:
  - REQ-0001-user-login
  - REQ-0002-product-brand-login-simplify
  - REQ-0003-login-left-panel-refine
```

---

## 3. Requirement Analysis

### 业务目标

减少企业员工重复登录时的输入成本；补齐 REQ-0001 中已声明但未落地的密码显隐能力。

### 用户

企业内部运营、管理员（`/admin/login`）。

### 核心能力

| ID | 能力 |
|---|---|
| F-01 | 勾选「记住登录状态」且登录成功后，本地保存用户名/密码，下次自动填充 |
| F-02 | 密码框显隐切换（眼睛图标） |

### 非功能需求

| 维度 | 要求 |
|---|---|
| 安全 | 密码仅 localStorage 客户端明文；登出清除；不上传服务端存明文 |
| 兼容 | 不改变 `remember_me` JWT 策略；localStorage 不可用时静默降级 |
| 可维护性 | 独立 `login-credentials.ts` 工具模块 + 单元测试 |
| UI | 登录页 CSS Port；不改左栏（REQ-0003-login-left-panel-refine） |

---

## 4. Impact Analysis

```yaml
impact:
  backend: false      # 无 API / Schema 变更
  web: true           # LoginForm、auth-store、login-page.css
  miniapp: false
  admin: true         # 管理端登录页
  database: false
  storage: false      # 无 MinIO
  api: false          # 复用 POST /api/v1/auth/login
  algorithm: false
  test: true          # vitest：凭证工具 + LoginForm
  docs: false         # 可选更新 authentication.md
  design_system: false  # 登录 CSS Port 局部样式，非 DS 新组件
```

---

## 5. 功能映射与代码基线

| 功能 | PRD | 现状 |
|---|---|---|
| 记住 · 自动填充 | FR-001 ~ FR-003 | `rememberMe` 仅影响 JWT；无凭证存储 |
| 密码显隐 | FR-004 | `LoginForm` 固定 `type="password"` |

| 模块 | 路径 | 动作 |
|---|---|---|
| LoginForm | `src/web/src/features/auth/components/LoginForm.tsx` | mount 读凭证、显隐 UI、成功/失败写凭证 |
| 凭证工具 | `src/web/src/features/auth/utils/login-credentials.ts` | **新建** |
| Auth store | `src/web/src/features/auth/store/auth-store.ts` | 登出 `clearLoginCredentials()` |
| Token | `src/web/src/features/auth/utils/auth-token.ts` | 不变 |
| 样式 | `src/web/src/features/auth/styles/login-page.css` | `.password-wrap`、`.password-toggle` |
| 测试 | `login-credentials.test.ts`、`LoginForm.test.tsx` | 新增/扩展 |

**Storage key（定稿）：** `stonex_login_credentials`

---

## 6. 关联文档

| 文档 | 路径 | 状态 |
|---|---|---|
| PRD | `requirement.md` | ✓ |
| 用户故事 | `user-stories.md` | ✓ |
| 业务流程 | `business-flow.md` | ✓ |
| 验收标准 | `acceptance.md` | ✓ |
| 测试计划 | `test-plan.md` | ✓ |
| 表单增强说明 | `prototype/web/login-form-enhancements-context.md` | ✓ |
| 登录页 HTML 基线 | `../REQ-0001-user-login/prototype/web/user-login.html` | 引用 |
| 登录页 PNG | `../REQ-0001-user-login/prototype/web/user-login.png` | 实现后可选更新 |

---

## 7. 工作量与 Sprint 建议

| 项 | 预估 |
|---|---|
| Story Points | 3 ~ 5 SP |
| 人天 | 1.5 ~ 2.5 人天 |
| 建议 Sprint | sprint-002（已纳入） |

**风险**

- 明文密码 localStorage：共享设备需依赖登出清除（FR-003）。
- 与 REQ-0001「记住我」语义扩展：归档 spec 时需 MODIFIED web-client 场景。

---

## 8. 安全确认

| 项 | 说明 |
|---|---|
| 明文 localStorage | 产品明确要求自动填充密码；登出清除 |
| 服务端 | 密码仍 bcrypt 哈希；本需求不写库明文 |
| rules/security.md | 不放宽鉴权；仅客户端便利存储 |

---

## 9. 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-15 | 需求入库 | 创建六件套（初版编号 REQ-0007，已迁至 REQ-0003-login-remember-autofill） |
| 2026-06-15 | `/requirement-to-change` | 统一编号、补 trace 分析、test-plan |
| 2026-06-15 | `/requirement-to-opsx` | 创建 `add-login-remember-autofill` OpenSpec |
| 2026-06-15 | 纳入 sprint-002 | 更新 `iterations/sprint-002/` 四件套与本 trace |
| 2026-06-20 | opsx-archive | 归档至 `openspec/changes/archive/2026-06-20-add-login-remember-autofill/` |

---

## 10. 后续动作

1. **`/opsx-apply add-login-remember-autofill`** → 实现 + 测试。
2. 可选：更新 `user-login.png` 含显隐图标状态。
3. 完成后 **`/opsx-archive add-login-remember-autofill`**。
