---
purpose: 全局规则
content: 团队研发规范和AI约束
source: AI自动生成初稿，项目团队确认
update_method: 项目初始化后由人工确认；后续由AI辅助更新并经人工Review
note: 适用于瓷砖信息管理平台项目模板
---

# 发布规范

发布前必须完成测试、OpenSpec校验、接口生成、变更归档和发布说明。

## 发版检查清单（Web 产品版本）

对外发布 Web 管理端或店主端时，若本次发版包含产品版本语义变更，MUST 人工更新：

```text
src/shared/product-version.ts  →  PRODUCT_VERSION（如 v0.0.1）
```

MUST NOT 依赖 `package.json` 或 FastAPI `version` 作为用户可见产品版本。