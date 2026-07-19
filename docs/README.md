---
purpose: docs 目录总索引
content: 主文档（编号）与治理细则（standards）导航
source: rules/document-governance.md
update_method: 新增 docs 顶层或 standards 文档时同步更新
created_at: 2026-06-13 00:00:00
updated_at: 2026-07-16 09:24:12
---

# 文档索引

## 层 1：主文档（`docs/00–08`，按阅读顺序）

| 文档 | 说明 |
|------|------|
| [00-product-overview.md](00-product-overview.md) | 产品定位与核心场景 |
| [01-architecture.md](01-architecture.md) | 系统架构 |
| [02-deployment.md](02-deployment.md) | Docker Compose 与部署 |
| [03-api-index.md](03-api-index.md) | **API 接口清单**（实现索引） |
| [04-database-design.md](04-database-design.md) | SQLite 表结构 |
| [05-compatibility-matrix.md](05-compatibility-matrix.md) | 兼容性矩阵 |
| [06-video-asset-management.md](06-video-asset-management.md) | 视频资产 |
| [07-object-storage-strategy.md](07-object-storage-strategy.md) | 对象存储策略 |
| [08-production-image-release.md](08-production-image-release.md) | 生产镜像包构建与云服务器部署手册 |

新增主文档占用下一序号（如 `09-*.md`），**仅**用于根目录导航型文档。

## 层 2：治理细则（`docs/standards/`）

| 文档 | 说明 |
|------|------|
| [standards/api-governance.md](standards/api-governance.md) | REST、统一响应、OpenAPI First |
| [standards/error-codes.md](standards/error-codes.md) | 错误码分段与登记 |
| [standards/openapi-rules.md](standards/openapi-rules.md) | FastAPI 注解与契约 |
| [standards/authentication.md](standards/authentication.md) | JWT 鉴权 |
| [standards/file-upload.md](standards/file-upload.md) | 上传与 MinIO |
| [standards/testing-governance.md](standards/testing-governance.md) | 测试金字塔与治理 |
| [standards/unit-test-standard.md](standards/unit-test-standard.md) | 后端单元测试 |
| [standards/frontend-test-standard.md](standards/frontend-test-standard.md) | 前端 Vitest |
| [standards/test-coverage.md](standards/test-coverage.md) | 覆盖率目标 |
| [standards/xl-admin-page-acceptance-template.md](standards/xl-admin-page-acceptance-template.md) | XL 管理端页面分层验收模板 |

细则文档 **不加** `00–` 序号；新增标准放入 `standards/`。

## 层 3：知识库（`docs/knowledge-base/`）

故障与事故沉淀，按主题命名，见 [knowledge-base/README.md](knowledge-base/README.md)。

## 需求与迭代（不在 docs/ 根目录）

| 类型 | 路径 |
|------|------|
| 需求 | `issues/requirements/REQ-*` |
| 缺陷 | `issues/bugs/BUG-*` |
| 迭代 | `iterations/change/sprint-xxx/`（进行中）、`iterations/archive/sprint-xxx/`（已归档） |
| 产品版本发布 | `releases/vX.Y.Z/` |

禁止恢复 `docs/prd/`、`docs/bugs/`、`docs/iterations/`。
