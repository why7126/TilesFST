---
sprint_id: sprint-002
title: Sprint 002 迭代经验复盘
status: draft
created_at: 2026-06-27 16:15:00
updated_at: 2026-06-27 16:15:00
owner: product
related_iteration: iterations/sprint-002/
related_requirements:
  - REQ-0004-admin-home
  - REQ-0005-user-management
  - REQ-0005-user-management-list-refine
  - REQ-0003-login-remember-autofill
  - REQ-0005-brand-management
  - REQ-0005-tile-category-management
  - REQ-0006-tile-sku-management
  - REQ-0007-tile-category-management-refine
  - REQ-0008-brand-status-confirm
  - REQ-0010-product-version-display
  - REQ-0011-admin-sidebar-expand-collapse
related_bugs:
  - BUG-0001-tile-category-enable-missing
  - BUG-0002-brand-ui-inconsistency
  - BUG-0003-brand-image-display-layout-shift
  - BUG-0004-brand-logo-upload-progress-missing
  - BUG-0005-login-fails-after-service-restart
  - BUG-0006-object-storage-upload-not-minio
  - BUG-0007-brand-logo-not-displayed-after-storage-fix
  - BUG-0008-object-storage-legacy-upload-residue
  - BUG-0009-tile-sku-list-ui-inconsistency
  - BUG-0010-tile-sku-modal-subtitle-inconsistency
  - BUG-0011-tile-sku-modal-content-overflow
  - BUG-0012-tile-sku-modal-form-field-rules
  - BUG-0014-tile-sku-publish-action-missing
  - BUG-0015-admin-list-status-tips-layout-shift
  - BUG-0016-admin-list-status-action-confirm-missing
  - BUG-0017-user-reset-password-confirm-ui-inconsistency
  - BUG-0018-tile-sku-modal-video-upload-display
  - BUG-0019-user-modal-avatar-upload-display
  - BUG-0020-tile-sku-modal-video-upload-413
related_changes:
  - add-admin-home
  - add-user-management
  - fix-user-management-list-refine
  - add-login-remember-autofill
  - add-brand-management
  - add-tile-category-management
  - fix-tile-category-enable-action
  - add-tile-sku-management
  - fix-tile-category-management-refine
  - fix-brand-ui-consistency
  - fix-brand-image-display-layout-shift
  - fix-brand-logo-upload-progress
  - fix-object-storage-upload-not-minio
  - fix-brand-logo-display-after-storage-fix
  - fix-brand-status-confirm
  - fix-admin-login-service-restart
  - fix-object-storage-legacy-upload-residue
  - fix-tile-sku-modal-content-overflow
  - fix-tile-sku-list-ui-inconsistency
  - fix-tile-sku-modal-subtitle-inconsistency
  - fix-tile-sku-modal-form-field-rules
  - fix-tile-sku-publish-action-missing
  - fix-tile-sku-modal-video-upload-display
  - add-product-version-display
  - add-admin-sidebar-collapse
  - fix-admin-list-status-toast-layout
  - fix-admin-list-status-action-confirm
  - fix-user-reset-password-confirm-ui
  - fix-user-modal-avatar-upload-display
  - fix-tile-sku-modal-video-upload-413
source: /sprint-exps
note: 由 AI 初稿生成，须人工 Review 后改为 published
---

# Sprint 002 迭代经验复盘

## 1. 迭代概况

| 指标 | 值 |
|------|-----|
| 周期 | 2026-06-15 ~ 2026-06-28（`iterations/sprint-002/sprint.yaml`） |
| 容量规划 | 150 SP / 98 人天；2 开发 + 1 测试 |
| REQ | 11（registry/trace 均为 **done**） |
| BUG | 19（Sprint 内；registry 均为 **done**） |
| Change | 30（**8 add-*** + **22 fix-*** / update-*） |
| Change archived | **30/30**（`openspec list` 无 active change） |
| Sprint 状态 | **completed**（`sprint.yaml`） |
| 发布 | **Published**（`release-note.md`） |
| 验收 sign-off | **细项 AC 大量未勾选**（`acceptance-report.md` §功能验收） |
| 延后项 | Dashboard 真实统计、Banner 管理、店主端目录等（`sprint.md` §不包含） |

**时间线体感（来自 trace / archive 目录日期）：**

- 2026-06-15 ~ 06-20：首页、用户、类目、登录增强等 **add-*** 密集交付
- 2026-06-25 ~ 06-26：品牌与对象存储 **fix 链**（BUG-0002 ~ BUG-0008）
- 2026-06-27：SKU 弹窗/列表 **fix 集群** + 管理端交互统一（BUG-0009 ~ BUG-0020）

## 2. 流程复盘

### 做得好的

- **OpenSpec + workflow-sync 闭环可运行**：30 个 change 全部归档，`issues/*/trace.md` 与 Sprint Scope 表基本同步。
- **BUG 与 REQ 边界清晰**：对象存储、SKU 弹窗等问题均走独立 `fix-*` change，未污染原 `add-*` 归档包。
- **原型驱动有效**：带 HTML 原型的 REQ（首页、用户、品牌、类目、SKU）开发速度可接受，trace 中 HTML 并排 checklist 有记录。

### 问题

| 问题 | 证据 | 影响 |
|------|------|------|
| **Sprint 容量过载** | 11 REQ + 19 BUG + 30 change；估算 98 人天 | 后期 fix 集群集中爆发，archive 顺序与 spec 合并压力大 |
| **add-* 未 archive 前 fix-* 已改主 spec** | `add-tile-sku-management` archive 时 `ADDED` 与 `openspec/specs/` 冲突，需 `--skip-specs` + 手工合并 | archive 卡点；MODIFIED 标题对齐成本高 |
| **验收与实现脱节** | `acceptance-report.md` 大量 `- [ ]`；结论写「待 sign-off」 | 发布状态 Published 与 AC 勾选不同步 |
| **UAT 规则晚于实现** | BUG-0012 表面工艺/参考价格规则在 UAT 后才 capture | 额外 fix change + acceptance delta |

### 优化建议（下一 Sprint）

1. **Sprint propose 上限**：建议单 Sprint **≤6 add-*** 主能力 + **预留 30% 容量**给 fix；本 Sprint fix 占比 73%（22/30）。
2. **Archive 顺序写进 sprint.md**：父 `add-*` 优先 archive，再批量 `fix-*`；避免 fix delta 先写入 `openspec/specs/`。
3. **Sprint-archive 前跑 `acceptance-report` 勾选门禁**：至少核心 REQ 的 P0 AC 由测试勾选后再 `status: published`。
4. **子需求/ refine 尽量在 review 前并入父 REQ acceptance**，减少 `fix-user-management-list-refine` 类并行 change。

## 3. 需求与设计

### PRD 与原型

- **REQ-0006 SKU 管理**体量最大（880px 弹窗、多图多视频），上线后产生 **7 个直接关联 BUG**（列表、弹窗 overflow、副标题、字段规则、上架、视频回显、413），说明 add 阶段 acceptance 对「列表 DOM 对齐」「弹窗滚动」「上传全链路」覆盖不足。
- **HTML 原型 > PNG**：有 `tile-sku-management-list.html` 仍出现分页 DOM 不一致（BUG-0009），说明 **逐页 port CSS** 未强制复用同一列表骨架。
- **REQ-0008 品牌启停确认**交付后，用户/SKU 列表仍缺 confirm（BUG-0016），说明 **「状态变更二次确认」未上升为横切 AC**。

### 评审深度

- **BUG-0001**（类目启用）本可在 `req-review` 对照品牌页操作列模式发现。
- **BUG-0005**（重启后登录）属于 **环境/初始化策略** 缺口，PRD 未要求可审计的 admin 密码策略。

### 文档模板建议

| 字段/门禁 | 建议 |
|-----------|------|
| `acceptance.md` | 管理端列表页 MUST 含「分页 DOM 与用户管理一致」横切 AC |
| `acceptance.md` | 含上传的弹窗 MUST 含「上传状态机 + 即时回显」AC |
| `req-complete` | 大弹窗 MUST 含矮视口滚动 AC（≤900px） |
| `bug-complete` | 关联 `related_bug` 时 MUST 声明与父 BUG scope 边界 |

## 4. 开发与质量

### 重复 BUG 模式

| 模式 | 次数 | 关联 BUG | 根因摘要 |
|------|------|----------|----------|
| **管理端列表 UI 不一致** | 4+ | BUG-0002, BUG-0009, BUG-0015 | 各页独立 port CSS；分页/notice 未抽象 |
| **弹窗副标题/结构不一致** | 2 | BUG-0010, BUG-0017 | 未统一 `.modal-desc` / confirm modal |
| **弹窗内容溢出无滚动** | 1 | BUG-0011 | 未采用 flex 滚动布局 gate |
| **上传无进度/无回显** | 4 | BUG-0004, BUG-0018, BUG-0019, BUG-0007 | 未复用 Brand Logo 上传状态机 |
| **对象存储全链路** | 5 | BUG-0006~0008, 0007, 0020 | 本地 UPLOAD_DIR、URL 回显、Nginx 413、legacy 清理 |
| **状态操作缺 confirm** | 2 | BUG-0016, BUG-0017 | 横切交互未在首版列表实现 |
| **启停/上架按钮逻辑** | 2 | BUG-0001, BUG-0014 | 操作列条件与品牌页未对齐 |

### 测试缺口

- **Vitest**：列表分页 DOM、modal `role="dialog"` 本可组件级断言（部分 fix 已补）。
- **Pytest**：对象存储写入 MinIO、oversize 上传（`test_upload_settings.py` 在 BUG-0020 后补强）。
- **E2E / Docker**：413 仅经 Nginx 反代暴露；tasks 应 recurring 含 `docker compose` + `localhost:3000` 大文件 POST。

### 归档质量

- `add-tile-sku-management`：`openspec archive` 因 delta `ADDED` 与已合并 fix spec 冲突失败（见 `openspec/changes/archive/2026-06-27-add-tile-sku-management/` 归档记录）。
- 建议：fix change archive 时若 MODIFIED 父 capability，在 change `design.md` 注明「父 add 未 archive 时的 spec 预合并风险」。

## 5. 可复用抽象

| 机会 | 涉及页面/REQ | 建议 |
|------|--------------|------|
| **`AdminListPage` 模板落地** | 用户、品牌、类目、SKU | 统一 hero、筛选、table-card、分页、`FixedAdminToast` |
| **`AdminConfirmModal` + 状态机** | 启停、冻结、上架、删除、重置密码 | 禁止 `window.confirm`；单一 modal 组件 |
| **`MediaUploadField` 状态机** | 品牌 Logo、用户头像、SKU 图/视频 | 从 `BrandFormModal` 提取 idle/uploading/done/failed |
| **对象存储上传 checklist** | 所有上传能力 | 见 `best-practices/admin-media-upload-chain.md` |
| **Design System 验收页** | 列表分页、弹窗、toast | `/design-system` 增加 Admin 列表/弹窗/上传区块 |
| **OpenSpec tasks 模板** | 所有 UI change | 默认含 HTML 并排、Docker Web 验证、PNG 可选 |

**说明**：实现须走 `/req-capture` + OpenSpec，本复盘仅记录建议。

## 6. 行动项

| ID | 优先级 | 描述 | 建议下一步 | 负责人建议 | 状态 |
|----|--------|------|------------|------------|------|
| A-001 | P0 | 完成 Sprint 002 `acceptance-report.md` 核心 AC 人工勾选与验收人 | 测试牵头对照 trace checklist | QA | open |
| A-002 | P1 | 抽象管理端列表页模板，消除分页/notice 重复 fix | `/req-capture` AdminListPage 统一模板 | 前端 | open |
| A-003 | P1 | 抽象上传状态机组件（图/视频/头像） | `/req-capture` MediaUploadField | 前端 | open |
| A-004 | P1 | 横切「状态变更二次确认」纳入 rules/ui-design 与管理端 AC 模板 | 团队评审后 `/req-capture` 更新规范 | 产品+前端 | open |
| A-005 | P2 | 对象存储/大文件上传部署 checklist（Nginx + env + Docker 重建） | 已部分写入 `docs/standards/file-upload.md`；推广到 `rules/release.md` 建议项 | 后端+DevOps | open |
| A-006 | P2 | Sprint 容量：单迭代 add change ≤6，预留 fix 缓冲 | 下一 `/sprint-propose` 采用 | 项目经理 | open |
| A-007 | P2 | OpenSpec archive：父 add 优先于 fix；delta 冲突预检脚本 | `/req-capture` 工具化或 AGENTS.md 补充 | 架构 | open |
| A-008 | P2 | 更新 `minio-upload-timeout.md` 纳入 413 与 env 对齐案例 | 编辑 `docs/knowledge-base/incidents/` | 后端 | open |

## 7. 知识库沉淀清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `retrospectives/sprint-002-retrospective.md` | 新建 | 本文档 |
| `best-practices/admin-list-page-consistency.md` | 新建 | 列表分页、toast、操作列模式 |
| `best-practices/admin-media-upload-chain.md` | 新建 | MinIO + 回显 + Nginx + env |
| `incidents/minio-upload-timeout.md` | 建议更新 | 补充 BUG-0020 413 案例（行动项 A-008） |

## 8. 变更记录

| 时间 | 说明 |
|------|------|
| 2026-06-27 16:15:00 | 初稿（`/sprint-exps sprint-002`） |
