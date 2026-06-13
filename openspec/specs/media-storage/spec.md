---
purpose: OpenSpec正式规范
content: 已生效系统能力
source: AI自动生成初稿，项目团队确认
update_method: 项目初始化后由人工确认；后续由AI辅助更新并经人工Review
note: 适用于瓷砖信息管理平台项目模板
---

# 图片存储能力规范

系统 SHALL 使用 MinIO 存储瓷砖图片，并在 SQLite 中保存对象Key和元数据。