---
requirement_id: REQ-0095-admin-list-field-display-adapter-checklist
created_at: 2026-08-04 08:35:48
updated_at: 2026-08-04 08:35:48
owner: product
source: requirement.md
---

# 业务流程

## 1. 主流程

```text
需求确认
  ↓
选择首批管理端列表
  ↓
盘点每个列表的 image / name / fallback 字段
  ↓
识别已有 helper、页面内判断、样式兜底
  ↓
建立 adapter 检查表
  ↓
按检查表生成验收清单和回归样例
  ↓
后续 OpenSpec design 决定是否抽公共 adapter / 组件 / 模板约束
```

## 2. 列表覆盖流程

```text
品牌列表
  ├─ image：Logo / 缩略图 / 首字母兜底
  ├─ name：品牌名称
  └─ fallback：无 Logo、名称异常、状态未知

证书列表
  ├─ image：证书图片 / 缩略图 / PDF 或文件类型标识
  ├─ name：证书名称 / 编号 / 发证机构
  └─ fallback：未设置有效期、无证书图片、文件缺失

SKU 列表
  ├─ image：主图 / 图片集合第一张 / 缺主图
  ├─ name：SKU 名称 / 品牌 / 分类
  └─ fallback：素材缺失、未知状态、时间为空

Banner 列表
  ├─ image：Banner 图 / SKU 主图 / 品牌 Logo / 自定义上传图
  ├─ name：Banner 标题 / 展示位置 / 跳转目标
  └─ fallback：未设置时间、无跳转、关联对象缺失
```

## 3. 与父需求或相邻需求差异

| 关联项 | 差异 |
|---|---|
| 品牌管理 | 品牌需求关注品牌 CRUD；本需求关注品牌列表展示规则是否可迁移为统一检查项。 |
| 证书管理 | 证书需求关注证书资料维护；本需求关注证书列表图片、文件和空值展示口径。 |
| SKU 管理 | SKU 需求关注商品资料维护；本需求关注 SKU 列表主图、名称、状态和素材缺失展示规则。 |
| Banner 管理 | Banner 需求关注投放配置；本需求关注 Banner 图、跳转目标和有效期兜底展示规则。 |
| REQ-0092 | REQ-0092 关注真实缩略图生成；本需求只检查管理端列表如何选择和兜底展示图片。 |

## 4. 风险与控制点

| 风险 | 控制点 |
|---|---|
| 检查表过宽，变成无法验收的规范口号 | 每个 adapter 项必须写出适用列表、期望表现和验证方式。 |
| 误以为本需求必须立即重构所有列表 | 在范围外明确“不立即重构所有列表”，后续 OpenSpec 再评估实现策略。 |
| 图片字段治理滑向上传链路改造 | 本需求只覆盖列表展示，不调整上传、缩略图生成或对象存储策略。 |
| 横切列表一致性再次遗漏 | acceptance.md 保留 knowledge-base 横切 AC。 |
