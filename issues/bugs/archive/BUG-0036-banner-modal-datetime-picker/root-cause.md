---
bug_id: BUG-0036-banner-modal-datetime-picker
status: pending_review
created_at: 2026-06-28 16:20:00
updated_at: 2026-06-28 16:20:00
root_cause_type: code
---

# 根因分析

## 1. 直接原因

### 1.1 `BannerFormModal` 使用原生 `datetime-local` 作为有效期控件

`BannerFormModal.tsx` 中「有效期开始」「有效期结束」为：

```tsx
<input className="input" type="datetime-local" value={validFrom} … />
<input className="input" type="datetime-local" value={validTo} … />
```

问题：

1. **HTML5 规范**：`datetime-local` 值为 `YYYY-MM-DDTHH:mm`，**不包含秒**；浏览器原生 UI 通常无法选择秒。
2. **交互不稳定**：在暗色管理端（`globals.css` `color-scheme: dark` + `.admin-shell .input` 自定义样式）下，Chrome / Safari 等环境下时间选择器可能难以操作或表现为「仅能选日期」。
3. **与项目 DS 策略不符**：`rules/ui-design.md` 与 AGENTS.md 要求优先复用 `shared/ui` / shadcn 复合组件；项目 **无** DateTime 选择器（无 Calendar、`react-day-picker` 等依赖），`add-banner-management` 实现时直接采用原生控件捷径。

### 1.2 提交与回填逻辑固化秒值、丢弃精度

`handleSubmit`：

```tsx
valid_from: validFrom ? `${validFrom}:00+00:00` : null,
valid_to: validTo ? `${validTo}:59+00:00` : null,
```

- 用户无法通过 UI 指定任意秒；开始恒为 `:00`，结束恒为 `:59`。
- 编辑回填：`banner.valid_from?.slice(0, 16)`，秒与时区展示信息被丢弃。

### 1.3 列表展示仅到分钟

`banner-display.ts` → `formatBannerDateTime`：`value.replace('T', ' ').slice(0, 16)`，列表「有效期」列不展示秒，与 capture 中 `yyyy/mm/dd hh:mm:ss` 不一致。

### 1.4 弹窗字段形态未对齐 prototype HTML

REQ-0016 弹窗 HTML（`banner-management-modal-*.html`）为 **单个**「有效期」输入，示例值：

`2026-06-01 00:00 至 2026-07-01 23:59`

当前实现为 **两个** 独立 `datetime-local` 字段（「有效期开始」「有效期结束」），字段数量与展示格式均未 port。

### 1.5 `add-banner-management` 未验收有效期 DateTime 交互

`openspec/changes/add-banner-management/trace.md` 侧重列表、jump_type、640px 弹窗等，**未**关闭 AC-027 有效期字段的可操作 DateTime 验收；BUG-0036 在 REQ-0016 产品验收阶段暴露。

## 2. 根本原因

### 2.1 管理端 DateTime 输入模式未在 Design System 沉淀

品牌、SKU、类目等模块暂无统一 DateTime 组件；Banner 首版实现时选用零成本 `datetime-local`，未对照 prototype HTML 中的区间展示与分钟级运营语义做组件化设计。

### 2.2 CSS Port 与交互验收 gate 缺失

与 BUG-0033（modal scroll）、BUG-0032（上传按钮）同类：`sprint-apply` 交付 Banner 弹窗时，公共字段「有效期」仅满足「有输入框」，未验证 **能否稳定选择时分**、是否与 HTML 原型字段形态一致。

### 2.3 需求文档与 capture 表述歧义未在 apply 前消化

- `requirement.md`：存储为 ISO TEXT，`valid_from` / `valid_to` 语义清晰。
- `capture.md`（BUG-0036）：要求 `yyyy/mm/dd hh:mm:ss` 且可选秒。
- **prototype HTML**（优先级最高）：单字段区间、`YYYY-MM-DD HH:mm` 分钟展示。

实现未按 HTML 原型裁定，导致 UI、展示与产品预期三方不一致。

## 3. 触发条件

满足以下条件可 **稳定复现**「无法按需配置时分 / 格式不符」：

1. admin 或 employee 登录 Web 管理端，打开 `/admin/banners` 新增/编辑弹窗。
2. 点击「有效期开始」或「有效期结束」控件，尝试通过 UI 选择小时、分钟、秒。
3. 观察：秒不可选；部分环境下时分选择困难；展示为 `YYYY-MM-DDTHH:mm` 而非原型 `YYYY-MM-DD HH:mm 至 …`。
4. 保存后列表「有效期」列仅显示到分钟；再次编辑时秒为硬编码策略而非用户输入。

**后端路径正常**：若通过 API 直接提交带秒的 ISO，`validate_validity` 与 `time_status` 计算可正常工作——缺陷集中在 **前端输入与展示**。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | code / frontend-ui |
| 是否接口缺陷 | 否（ISO 解析已就绪） |
| 是否数据库缺陷 | 否 |
| 是否权限缺陷 | 否 |
| 是否回归 | 否（`add-banner-management` 交付即存在） |
| 主要修复面 | `BannerFormModal.tsx`、可能新增 `shared/ui` DateTime 或区间选择组件、`banner-display.ts`、`banner-management.css` |
| 关联需求 AC | AC-027、AC-013（列表有效期列）、AC-051 |
| 建议 Change | `fix-banner-modal-datetime-picker`（可与 BUG-0031～0035 合并为 `fix-banner-modal-ui`） |

## 5. 后续修复建议

1. **裁定（acceptance 已定稿）**：按 prototype HTML 优先 — 单字段「有效期」区间展示 `YYYY-MM-DD HH:mm 至 YYYY-MM-DD HH:mm`；UI 精度到 **分钟**；秒由提交策略填充（开始 `00`、结束 `59`），**不要求**用户 UI 选秒（与 HTML 一致，MODIFIED 消化 capture 的 `yyyy/mm/dd hh:mm:ss` 秒级交互）。
2. 替换 `datetime-local`：Popover + 日期选择 + 时/分步进（或受控文本 + 校验），使用 semantic token，对齐 `rules/ui-design.md`。
3. 统一 `formatBannerDateTime` 与弹窗展示格式；列表「有效期」列保持两行（开始 / 结束）或区间文案与 AC 一致。
4. 保留 `valid_from` / `valid_to` 双字段 API 语义；单字段 UI 在提交时拆分为两个 ISO 时间。
5. Vitest：解析/格式化、提交 payload 秒策略、编辑回填。
6. 建议 Change：`fix-banner-modal-datetime-picker`；与 BUG-0031～0035 合并降低回归成本。
