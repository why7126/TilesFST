---
purpose: 接口文档
content: API索引和接口维护规则
source: AI自动生成初稿，项目团队确认
update_method: 项目初始化后由人工确认；后续由AI辅助更新并经人工Review
note: 适用于瓷砖信息管理平台项目模板
---

# API接口索引


## 接口来源

API 以 FastAPI 自动生成的 OpenAPI 为事实源。

## 主要接口

- `GET /api/v1/tiles`：查询瓷砖列表
- `GET /api/v1/tiles/{tile_id}`：查询瓷砖详情
- `POST /api/v1/admin/tiles`：新增瓷砖
- `PUT /api/v1/admin/tiles/{tile_id}`：更新瓷砖
- `POST /api/v1/admin/uploads`：上传图片
