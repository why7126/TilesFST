---
bug_id: BUG-0100-thumbnail-size-equals-original
title: 缩略图尺寸与原图一致导致加载优化失效
status: done
severity: high
review_result: approved
reviewed_at: 2026-08-01 07:34:26
reviewer: AI
created_at: 2026-08-01 07:34:26
updated_at: 2026-08-01 08:19:33
---

# BUG Review

## 评审结论

批准修复。

该问题属于后端媒体缩略图生成能力的行为缺陷。当前系统已经为 SKU 图片创建同目录 `.thumb` 缩略图对象，并在商品卡片、列表、搜索结果、品牌详情商品区等公开展示场景优先使用缩略图 URL，但实际写入逻辑只是复制原图 bytes，没有进行 resize、压缩或真实派生处理，导致缩略图优化名义存在、实际加载收益缺失。

## 评审清单

- [x] 可复现或根因充分：已确认 SKU 图片上传会传入 `.thumb` key，`save_upload_file()` 将原图 `content` 原样写入缩略图对象；临时复现结果显示原图与缩略图 `same_bytes=True`。
- [x] 严重等级合理：`high`，问题影响公开商品浏览核心路径的图片加载性能，并增加对象存储容量与移动端流量成本。
- [x] 回归验收明确：acceptance.md 已覆盖真实缩略图生成、体积下降、小图边界、多格式处理、公开卡片 URL、历史重生成、安全边界和回归测试。
- [x] 是否需 hotfix 路径：暂不需要 hotfix；建议作为高优先级常规 BUG 进入 `/bug-opsx` 与 Sprint 规划。若生产环境首屏或商品列表图片加载性能已明显劣化，可升级为 hotfix。

## 处理建议

- 后续通过 `/bug-opsx BUG-0100-thumbnail-size-equals-original` 创建 OpenSpec Change。
- 修复应优先在后端媒体模块封装统一缩略图生成函数，明确最大宽高、质量、格式、透明图和失败降级策略。
- 修复必须覆盖新增上传和历史 `.thumb` 对象重生成，避免只修新增数据。
- 修复测试必须从“缩略图对象存在”提升到“像素尺寸、文件体积或 bytes 与原图不同”的行为验证。
- 如引入图片处理依赖，需要同步 Docker 镜像构建与部署验证边界。
