---
requirement_id: REQ-0120-webp-derived-image-variants
title: 图片上传生成 WebP 展示图和缩略图 - 业务流程
created_at: 2026-08-22 21:45:57
updated_at: 2026-08-22 21:45:57
---

# 业务流程

## 1. 新上传图片流程

```text
管理端选择图片
  ↓
后端校验 MIME / 扩展名 / 大小 / 权限
  ↓
写入 original 对象（保留上传格式）
  ↓
判断是否支持 WebP 派生
  ├─ JPEG / PNG / WebP
  │    ↓
  │  生成 thumbnail.webp
  │    ↓
  │  生成 display.webp
  │    ↓
  │  返回 original_url + thumbnail_url + display_url
  │
  └─ SVG / PDF / GIF / HEIC / TIFF / BMP 等首期不转码类型
       ↓
     记录跳过原因
       ↓
     返回 original_url，并按端侧 fallback 展示
```

## 2. 端侧消费流程

```text
接口返回图片 URL
  ↓
按场景选择目标规格
  ├─ 列表 / 卡片：thumbnail_url
  ├─ 详情普通展示：display_url
  ├─ 高清预览 / 下载：original_url
  └─ 分享封面：按平台限制选择 original 或 display
  ↓
加载目标 URL
  ├─ 成功：展示 WebP 派生图
  └─ 失败 / 缺失：回退 display → thumbnail → original → 占位
```

## 3. 历史对象补生成流程

```text
运维触发维护任务 dry-run
  ↓
扫描历史图片记录和对象存储
  ↓
分类统计
  ├─ 已有 WebP 派生图
  ├─ 可补生成
  ├─ 不支持格式，跳过
  ├─ 原图缺失
  └─ 对象存储不可达或读取失败
  ↓
输出脱敏摘要和预计写入数量
  ↓
人工确认备份与执行窗口
  ↓
apply 补生成 WebP 派生对象
  ↓
幂等复跑并输出 key / object / URL / render / benefit 摘要
```

## 4. 与父需求差异

| 维度 | REQ-0115 已完成能力 | REQ-0120 本次增强 |
|---|---|---|
| 三规格模型 | 建立 `thumbnail / display / original` 语义 | 沿用三规格模型，不新增规格 |
| 派生格式 | 派生图默认沿用原图格式 | `thumbnail / display` 统一 WebP |
| 原图策略 | 保留原图用于预览和高清场景 | 明确原图不被 WebP 替换 |
| key 规则 | 同目录 `.thumb` / `.display` suffix | 派生 key 与 MIME 一致，推荐 `.thumb.webp` / `.display.webp` |
| 端侧策略 | 多端按场景选择规格 | 端侧优先消费 WebP 派生 URL 并保留 fallback |
| 历史维护 | 已有多规格维护基础 | 补生成 WebP 派生图，要求 dry-run / apply / 幂等 |

## 5. 边界声明

- 本需求不改变上传鉴权、对象存储 Bucket、业务资源目录或原图访问语义。
- 本需求不新增视频转码或 AVIF 多格式协商。
- 本需求不要求保存系统设置时自动重建历史对象。
- 本需求可能影响 API 示例、OpenAPI / Orval 生成物和前端测试期望，后续 OpenSpec 阶段需逐项确认。
