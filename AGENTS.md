---
purpose: AI行为入口
content: AI开发流程、rules规范加载机制、OpenSpec执行规则、目录结构约束、Docker部署约束
source: AI自动生成初稿，项目团队确认
update_method: 项目初始化后由人工确认；后续由AI辅助更新并经人工Review
note: 适用于瓷砖信息管理平台项目模板；AI执行任何任务前必须优先阅读本文档
---

# AI Agent 工作指南

## 1. 项目定位

本项目采用 OpenSpec + AI Agent 规范编程方式开发。

系统包含：

- 面向瓷砖零售店店主的 Web 展示端。
- 面向瓷砖零售店店主的微信小程序。
- 面向企业内部员工的 Web 管理端。
- FastAPI 后端服务。
- SQLite 数据库。
- MinIO 对象存储。
- Docker Compose 本地开发与演示部署环境。

## 2. AI 必须优先读取的文档

AI Agent 在执行任何需求、BUG、代码修改、文档修改、部署修改前，必须按顺序读取：

```text
1. AGENTS.md
2. openspec/project.md
3. rules/global.md
4. rules/language.md
5. rules/coding.md
6. rules/testing.md
7. rules/security.md
8. rules/api.md
9. rules/database.md
10. rules/ui-design.md
11. rules/compatibility.md
12. rules/release.md
13. rules/directory-structure.md
14. rules/document-governance.md
15. rules/data-management.md
16. rules/environment.md
17. rules/media.md
18. 当前任务对应的 openspec/changes/<change-id>/
```

如果任务涉及 Docker 部署，还必须读取：

```text
docs/02-deployment.md
docker-compose.yml
src/backend/Dockerfile
src/web/Dockerfile
src/web/nginx.conf
```

如果任务涉及接口变更，还必须读取：

```text
docs/03-api-index.md
src/web/orval.config.ts
scripts/generate-openapi-client.sh
```

## 3. rules 目录使用规则

`rules/` 是全局研发规范目录，不是参考资料，而是强制约束。

| 文件 | AI使用方式 |
|---|---|
| `rules/global.md` | 判断是否允许执行当前任务 |
| `rules/language.md` | 控制输出语言、文档语言、代码命名 |
| `rules/coding.md` | 控制代码结构、命名、复杂度 |
| `rules/testing.md` | 判断是否需要新增或更新测试 |
| `rules/security.md` | 检查认证、上传、输入、权限、敏感信息 |
| `rules/ui-design.md` | 控制Web和小程序UI一致性 |
| `rules/api.md` | 控制API路径、参数、响应、错误码 |
| `rules/database.md` | 控制SQLite schema、迁移、查询规范 |
| `rules/compatibility.md` | 控制Web、小程序、Docker、本地环境兼容性 |
| `rules/release.md` | 控制发布、回滚、变更说明 |
| `rules/directory-structure.md` | 控制新增文件位置和目录边界 |
| `rules/document-governance.md` | 控制 docs、issues、iterations、openspec 的生成/更新/归档 |
| `rules/data-management.md` | 控制 data 目录、样例数据、运行时数据和提交边界 |
| `rules/environment.md` | 控制 .env.example、环境变量和密钥安全 |
| `rules/media.md` | 控制图片、视频、文档媒体资产上传、存储和展示 |

AI 生成代码或文档时，必须在输出中说明遵循了哪些 `rules/` 文件。

## 4. AI 开发流程

```text
需求 / BUG
↓
issues/
↓
iterations/
↓
openspec/changes/
↓
proposal / design / tasks / spec
↓
src/ 实现
↓
tests/ 验证
↓
openspec/archive/ 归档
```

## 5. 强制规则

- 不允许绕过 OpenSpec Change 直接开发功能。
- 不允许直接修改 `openspec/specs/` 中的正式规范，除非是归档合并动作。
- 不允许在根目录新增业务代码。
- 不允许绕过 `rules/directory-structure.md` 新增目录。
- 后端必须使用 Python3.12、FastAPI、Pydantic、uv、SQLite、MinIO。
- 前端必须使用 React19、TypeScript、Tailwind、shadcn/ui、Axios、Orval、pnpm。
- 部署必须优先支持 `docker-compose.yml`。
- API 修改后必须同步 OpenAPI，并通过 Orval 生成前端类型与请求客户端。
- 图片上传必须走后端授权与 MinIO 存储，不允许前端直连未授权对象存储。
- 管理端与店主端必须区分权限边界。

## 6. 目录结构执行要求

AI 新增或修改文件时，必须遵守：

```text
rules/directory-structure.md
```

推荐执行目录校验：

```bash
python scripts/validate-directory-structure.py
```

若需要新增顶层目录或调整模块边界，必须先创建 OpenSpec Change，并说明：

- 为什么现有目录无法承载。
- 新目录职责是什么。
- 会影响哪些文档、测试、脚本和部署文件。

## 7. Docker Compose 部署要求

本项目默认提供 Docker Compose 本地开发与演示环境。

启动：

```bash
./scripts/docker-up.sh
```

停止：

```bash
./scripts/docker-down.sh
```

服务地址：

```text
Web: http://localhost:3000
Backend API Docs: http://localhost:8000/docs
MinIO Console: http://localhost:9001
```

AI 修改 Docker 部署时，必须同步检查：

```text
docker-compose.yml
src/backend/Dockerfile
src/backend/.env.docker
src/web/Dockerfile
src/web/nginx.conf
docs/02-deployment.md
README.md
```

## 8. 输出要求

AI 回复默认使用中文。

涉及代码必须说明：

- 文件路径。
- 修改原因。
- 是否影响接口。
- 是否影响数据库。
- 是否影响 Web / 小程序 / 管理端。
- 是否需要执行 Orval。
- 是否需要执行 Docker Compose 验证。

涉及接口必须说明请求、响应和错误码。

涉及数据模型必须说明 SQLite 表结构和 Pydantic Schema。


## 9. data目录使用规范

根目录 `data/` 用于本地开发、演示、测试样例和运行时数据承载。

AI涉及以下任务时必须读取并更新 `rules/data-management.md` 和 `data/README.md`：

- SQLite本地数据文件
- 图片上传
- 视频上传
- 文件导入导出
- 样例数据
- 测试fixtures
- 本地运行日志或缓存

禁止提交真实客户数据、真实门店素材、运行时数据库文件和临时处理文件。

## 10. 环境变量规范

根目录必须保留 `.env.example`，用于说明本项目运行所需环境变量。

AI新增或修改以下内容时必须同步更新 `.env.example`：

- Docker Compose服务
- 后端配置
- 前端API地址
- SQLite数据库路径
- MinIO存储桶
- 上传大小限制
- 图片/视频MIME类型
- 视频处理开关

`.env` 文件禁止提交。

## 11. 视频与媒体资产规范

本项目初始化即包含视频相关目录和规范，原因是瓷砖业务天然涉及产品展示视频、铺贴效果视频和工艺说明视频。

AI处理媒体相关需求时必须读取：

```text
rules/media.md
docs/06-video-asset-management.md
openspec/specs/media-assets/spec.md
```

基础版本应支持：

- 图片上传
- 视频上传
- 视频封面
- MinIO存储
- SQLite媒体元数据
- Web/小程序展示

视频转码、压缩、多清晰度属于可选增强能力，必须通过OpenSpec Change进入开发。

## 12. V4项目规则强化

V4模板相比V3新增：

- `data/` 目录及数据治理规范。
- 根目录 `.env.example` 及环境变量治理规范。
- 视频资产管理文档和媒体OpenSpec。
- 面向瓷砖项目深化后的 rules 规范。

AI不得删除上述能力；如需裁剪，必须先创建 OpenSpec Change 并说明影响范围。

## V5 对象存储与端口规范

AI Agent 在处理文件、图片、视频、导入导出能力时，必须遵守：

```text
rules/object-storage.md
rules/media.md
rules/data-management.md
rules/port-management.md
```

### MinIO 规则

V5 采用：

```text
一个项目一个 Bucket
桶内使用目录前缀区分资源
```

AI 不得随意新增多个 Bucket。除非 OpenSpec Change 明确要求，否则必须使用：

```text
MINIO_BUCKET
MINIO_PREFIX_*
```

### 端口规则

V5 默认保留开发友好端口：

```text
Backend: 8000
Web: 3000
```

但必须通过 `.env.example` 提供宿主机端口覆盖：

```text
HOST_PORT_BACKEND
HOST_PORT_WEB
```

AI 不得为了本机端口冲突随意修改应用内部端口；应优先修改宿主机端口映射。
