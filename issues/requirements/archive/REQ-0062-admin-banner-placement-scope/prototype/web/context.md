---
requirement_id: REQ-0062-admin-banner-placement-scope
title: 管理后台 Banner 投放范围配置优化 - Web 原型说明
status: pending_review
created_at: 2026-07-20 18:40:54
updated_at: 2026-07-20 18:40:54
---

# Web 原型说明

## 目标

表达 Banner 管理页在收敛展示端和展示位置后的信息结构，不替代最终视觉稿。实现时应复用现有 `/admin/banners` 页面、`BannerFormModal`、列表分页和上传控件。

## 页面结构

```text
Banner 管理
├── 指标卡：Banner 总数 / 当前筛选 / 已上线 / 待生效
├── 筛选区
│   ├── 关键词
│   ├── 展示端：小程序（单项或只读）
│   ├── 展示位置：首页轮播 / 品牌列表页轮播
│   ├── 状态
│   └── 时间状态
├── 表格
│   ├── Banner 缩略图 + 标题
│   ├── 展示位置
│   ├── 展示端
│   ├── 跳转类型
│   ├── 状态
│   ├── 有效期
│   ├── 排序
│   └── 操作
└── 新增/编辑弹窗
    ├── 展示端：小程序
    ├── 展示位置：首页轮播 / 品牌列表页轮播
    ├── Banner 图片上传
    ├── 跳转类型与条件字段
    ├── 排序 / 有效期 / 备注
    └── 保存 Banner
```

## 原型决策

- 展示端只保留“小程序”，建议实现为只读文本或单项 Select；若保留下拉，不得出现其他选项。
- 展示位置为两项 Select 或 segmented control：`首页轮播`、`品牌列表页轮播`。
- 列表仍保留“展示端”列，用于让运营明确当前 Banner 都投放到小程序；后续若产品决定减少列，可在 OpenSpec design 中说明。
- 旧数据删除后不提供旧 Banner 编辑入口。
- Banner 图片上传 UI 沿用现有上传模块，但必须保留上传状态机和即时回显。

## 待后续导出

- PNG Golden Reference：待 OpenSpec design 或实现阶段基于当前页面截图导出。
- 1440x1024 列表对比：对齐用户管理分页 DOM 与 Banner 管理现有视觉。
- 弹窗 Computed width：实现阶段通过浏览器或 Playwright 截图确认。

