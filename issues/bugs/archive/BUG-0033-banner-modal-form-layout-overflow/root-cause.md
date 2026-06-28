---
bug_id: BUG-0033-banner-modal-form-layout-overflow
status: pending_review
created_at: 2026-06-28 16:17:14
updated_at: 2026-06-28 16:17:14
root_cause_type: design
---

# 根因分析

## 1. 直接原因

### 1.1 `banner-management.css` 未 port 弹窗 flex + 可滚动 body

原型 `banner-management-modal-*.html` 内联 CSS 规定：

```css
.modal-card { width:640px; max-height:92vh; display:flex; flex-direction:column; … }
.modal-body { padding:20px; overflow:auto }
```

当前 `banner-management.css` 中 `.banner-modal-card` 仅有：

```css
width: 640px;
max-height: 92vh;
```

**未**配置 `display: flex`、`flex-direction: column`、`overflow: hidden`，也**未**为 `.banner-modal-card .modal-body` 设置 `flex: 1`、`min-height: 0`、`overflow-y: auto`。

弹窗结构为 `modal-head` + `modal-body` + `modal-footer`（见 `BannerFormModal.tsx`）。内容总高度（Banner 图片区 118px + 双列 grid + 条件 jump 字段）在常见矮视口下超过 `92vh`，超出部分无法滚动，footer 按钮被裁切或不可达——与 BUG-0011（SKU 弹窗）同类缺口。

### 1.2 `banner-management.css` 未 port `.textarea` 表单控件规则

原型规定：

```css
.input,.select,.textarea { width:100%; font-size:12px; … }
.textarea { height:72px; padding:10px 12px; resize:none; line-height:1.6 }
.input::placeholder,.textarea::placeholder { color:var(--weak) }
```

`BannerFormModal.tsx` 运营备注使用 `className="textarea"`，且父级 `banner-form-row full` 已 `grid-column: 1 / -1`，但模块 CSS **未**定义 `.banner-form-grid .textarea` 宽度、高度、字号与 placeholder 样式。

全局 `user-management.css` 的 `.admin-shell .input, .select` 含 `width: 100%; font-size: 12px`，**不包含** `.textarea`。因此备注框按浏览器默认宽度与字号渲染，placeholder 视觉大于同弹窗 input。

### 1.3 `add-banner-management` 弹窗 CSS Port 验收不完整

`openspec/changes/add-banner-management/trace.md` checklist #8 仅验「640px + 无状态块」，**未**关闭 REQ-0016 **AC-024**「内容可滚动」及 textarea 整行 port；#16 四套 modal PNG 并排仍为「待人工复核 ○」。

## 2. 根本原因

### 2.1 CSS Port 策略不完整：只 port 局部业务类，遗漏共享 modal 结构与表单控件规则

`sprint-apply` 从 HTML port 了列表页、`.banner-upload-box`、`.banner-form-grid` 等局部样式，但未同步 port 原型 `<style>` 中与 `.modal-card` flex 布局、`.modal-body` 滚动及 `.textarea` 相关的通用规则；也未参照已验收的 `tile-sku-management.css`（BUG-0011 修复模式）或 `brand-management.css`（`.brand-textarea`）补全等价规则。

### 2.2 长表单弹窗「固定头尾 + 可滚动 body」模式未在 Banner 场景落地

SKU、品牌弹窗已在后续 BUG 中补齐 flex + scroll 模式；Banner 弹窗作为 sprint-003 新交付模块，实现时复制了 `max-height: 92vh` 约束，但未同步该模式，导致 REQ-0016 明确要求的内容区可滚动未满足。

### 2.3 管理端弹窗仍缺少 Port checklist 强制 gate

与 BUG-0028（textarea 宽度）、BUG-0011（modal scroll）同类：新增管理端弹窗时手写 JSX + 局部 CSS，缺少「modal-body MUST overflow + 跨列 textarea MUST width:100%」的人工或自动化 gate，AC-024 未在 merge 前关闭。

## 3. 触发条件

满足以下条件时可 **100% 稳定复现**：

1. 以 admin 登录 Web 管理端（local 或 Docker）。
2. 访问 `/admin/banners`，点击「+ 新增 Banner」或行内「编辑」。
3. 观察「运营备注」`textarea` 宽度未占满整行、placeholder 字号大于「Banner 标题」input。
4. 将视口高度缩小至约 ≤900px，或选择 `jump_type=SKU_DETAIL`（字段最多）。
5. 观察底部「取消」「保存 Banner」超出弹窗或不可点击；在 `.modal-body` 内滚轮无法纵向滚动。

**非缺陷路径：** Banner 标题、展示端等 `.input/.select` 字段宽度正常；矮视口**全屏最大化**时可能勉强触达 footer（不可靠，见 workaround）。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | design / frontend-ui |
| 是否接口缺陷 | 否 |
| 是否数据库缺陷 | 否 |
| 是否权限缺陷 | 否 |
| 是否回归 | 否（`add-banner-management` 交付即存在） |
| 主要修复面 | `banner-management.css`（modal scroll + textarea port）；必要时微调 `BannerFormModal` DOM/class |
| 关联需求 AC | AC-024、AC-027（运营备注字段）、AC-051 |
| 建议 Change | `fix-banner-modal-form-layout-overflow`（可与 BUG-0031～0035 合并为 `fix-banner-modal-ui`） |

## 5. 后续修复建议

1. 在 `banner-management.css` 为 `.banner-modal-card` 补 port（对齐原型 + BUG-0011 模式）：
   - `display: flex; flex-direction: column; overflow: hidden;`
   - `.banner-modal-card .modal-head, .modal-footer { flex-shrink: 0; }`
   - `.banner-modal-card .modal-body { flex: 1; min-height: 0; overflow-y: auto; }`
2. 在 `.banner-form-grid` 作用域内补 port `.textarea`：
   - `width: 100%`、`font-size: 12px`、`height: 72px`、`resize: none`、边框/背景 semantic token
   - `::placeholder { color: var(--admin-weak); }`
3. 矮视口（1440×900、1280×720）下验收四套 `jump_type` 弹窗均可滚动至 footer。
4. 建议 Change：`fix-banner-modal-form-layout-overflow`；可与 BUG-0031～0035 合并。
5. 可选 Vitest：断言 `.banner-modal-card .modal-body` 存在 scroll 相关样式或 class；备注 textarea `width: 100%`。
