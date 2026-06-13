---
purpose: 技术文档
content: 系统架构与模块划分
source: AI自动生成初稿，项目团队确认
update_method: 项目初始化后由人工确认；后续由AI辅助更新并经人工Review
note: 适用于瓷砖信息管理平台项目模板
---

# 系统架构


## 架构概览

```text
Web展示端 / 微信小程序 / 管理端Web
        ↓
FastAPI Backend
        ↓
SQLite + MinIO
```

## 模块划分

- 产品展示模块
- 产品管理模块
- 分类规格模块
- 图片上传模块
- 用户权限模块
