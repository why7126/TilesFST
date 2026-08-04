---
req_id: REQ-0095-admin-list-field-display-adapter-checklist
status: done
created_at: 2026-08-04 08:20:03
updated_at: 2026-08-04 09:29:56
recorded_by: product
source: 用户反馈
priority_hint: P1
parent_requirement:
---

# 一句话

管理端列表字段展示需要建立统一的 image / name / fallback adapter 检查表，用于约束各列表页图片、名称与兜底展示的一致性。

# 原始描述

管理端列表字段展示建立统一 image/name/fallback adapter 检查表

# 背景与关联

- 涉及端：Web 管理端
- 业务价值：降低不同管理端列表页在图片字段、名称字段、空值兜底、异常数据展示上的实现差异，提升后台运营识别效率与界面一致性
- 预期后续：梳理管理端各类列表页字段展示现状，形成统一 adapter 检查表，并作为后续开发、验收和回归检查依据

# 待澄清

- [ ] 检查表需要覆盖哪些管理端列表：品牌、证书、SKU、分类、Banner、上传资源、审计日志等
- [ ] image adapter 是否需要统一定义缩略图尺寸、占位图、加载失败态、无图态和多图主图选择规则
- [ ] name adapter 是否需要统一定义显示优先级、截断规则、空值文案、关联对象缺失时的展示策略
- [ ] fallback adapter 是否需要区分空值、无权限、已删除关联对象、接口字段缺失和媒体加载失败等场景
- [ ] 检查表最终落点是需求验收清单、设计系统规范、管理端开发文档，还是测试用例模板

# 探索结论

（/req-explore 后人工确认写入）
