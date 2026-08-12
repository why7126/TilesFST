---
requirement_id: REQ-0108-admin-banner-list-display-optimization
created_at: 2026-08-11 08:37:56
updated_at: 2026-08-11 08:37:56
---

# Business Flow

## 1. 当前流程

```text
运营进入 Banner 管理页
  ↓
前端请求管理端 Banner 列表接口
  ↓
接口返回 Banner 基础字段：图片、标题、位置、跳转类型、对象 ID、状态、排序等
  ↓
列表展示 Banner 图片 + 内部识别/标题 + 跳转类型等信息
  ↓
运营如需确认跳转对象名称，可能进入编辑弹窗查看
```

## 2. 目标流程

```text
运营进入 Banner 管理页
  ↓
前端请求管理端 Banner 列表接口
  ↓
后端按 jump_type 关联品牌 / SKU / 专题或复用 external_url
  ↓
接口返回 Banner 基础字段 + jump_target_label
  ↓
列表展示：
  - Banner 列：仅主图/缩略图
  - 跳转对象列：品牌名 / SKU名 / 专题名 / URL / -
  - 其他原有列：展示位置、展示端、跳转类型、状态、有效期、排序、更新时间、操作
  ↓
运营直接在列表中判断素材与跳转目标
```

## 3. 与父需求差异

| 项目 | `REQ-0016-banner-management` | 本需求 |
|---|---|---|
| Banner 列表基础能力 | 提供 Banner 的列表、筛选、状态与操作能力 | 优化列表字段呈现，不改变基础操作 |
| 跳转信息 | 以跳转类型和对象 ID 为主 | 增加可读跳转对象名称/链接 |
| Banner 标题 | 历史上可作为识别字段 | 不作为 Banner 列运营展示内容 |
| API | 返回 Banner 基础字段 | 新增只读展示字段，需同步 OpenAPI/Orval |

## 4. 异常与兜底

| 场景 | 建议处理 |
|---|---|
| 无跳转 | 跳转对象显示 `-`。 |
| 外部链接过长 | 单行截断，保留 title tooltip 或等价完整查看能力。 |
| 关联对象不存在或不可用 | OpenSpec 阶段明确显示 `-` 或“对象不可用”；不得空白或报错。 |
| 图片加载失败 | 沿用 `FallbackListImage` 或等价列表图片 fallback。 |
