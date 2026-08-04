---
purpose: 目录结构规范
content: 约束AI与开发人员遵循当前项目目录边界、文件归属和新增文件规则
source: AI自动生成初稿，项目团队确认
update_method: 目录结构调整时由架构负责人确认后更新；AI只能提出建议，不得擅自放宽规则
created_at: 2026-06-13 00:00:00
updated_at: 2026-08-03 19:10:00
note: AGENTS.md 必须强制引用本文档；用于防止AI随意新增目录或把文件放错位置
---

# 目录结构规范

## 1. 目标

本文档用于约束 AI Agent 和开发人员在瓷砖信息管理平台中遵循统一目录结构，避免出现以下问题：

- AI 随意创建新目录。
- 后端、前端、小程序、文档、测试文件混放。
- 绕过 OpenSpec 直接新增业务模块。
- 接口变更后未同步前端 Orval 类型。
- Docker、部署、脚本文件分散在错误位置。

## 2. 顶层目录职责

| 目录 | 职责 | 是否允许随意新增同级目录 |
|---|---|---|
| `rules/` | 全局规范 | 否 |
| `docs/` | 产品与技术文档 | 否 |
| `openspec/` | OpenSpec需求与规格事实源 | 否 |
| `issues/` | 原始需求和BUG池 | 否 |
| `iterations/` | 迭代管理 | 否 |
| `releases/` | 产品版本发布对象、公开发布公告源文件与发布校验材料 | 否 |
| `mintlify/` | 公开 Mintlify 文档站源目录、多版本文档投影、公告投影和共享截图资产 | 否 |
| `deploy/` | 部署环境矩阵、环境化 Compose、env 示例、部署脚本和校验工具 | 否 |
| `compatibility/` | 兼容性说明 | 否 |
| `.agents/` | Codex 技能与项目级 Agent 能力（唯一 AI 工具入口） | 否 |
| `src/` | 源码 | 否 |
| `tests/` | 测试 | 否 |
| `scripts/` | 自动化脚本 | 否 |
| `data/` | 本地开发数据卷 | 是，仅本地环境 |

如需新增顶层目录，必须先创建 OpenSpec Change，并在 `rules/directory-structure.md` 中说明新增原因。

### 2.1 `releases/` 产品发布目录

`releases/` 用于承载产品版本发布对象与公开发布公告源文件。它表达“一个对外产品版本发布”，可汇总一个或多个 Sprint 的 REQ、BUG 与 OpenSpec Change。

推荐结构：

```text
releases/
├── README.md
├── mint.json                  # Mintlify 静态文档配置（如采用）
├── templates/
│   ├── release.json           # 产品版本发布对象模板
│   └── announcement.mdx       # 公开公告模板
└── v0.1.0/
    ├── release.json           # 机器可读发布事实源
    ├── announcement.mdx       # Mintlify 公告源文件
    ├── usage-docs/            # 产品使用文档；仅用户确认需要生成或更新时存在
    │   ├── manifest.json
    │   ├── overview.mdx
    │   ├── admin/
    │   └── miniapp/
    ├── image-build-plan.json  # 镜像构建计划；仅 image_required=true 或有镜像治理证据时生成
    └── image-manifest.json    # 镜像构建结果 manifest；仅真实构建或受控外部证据完成后生成
```

边界：

- `releases/` MUST 只存放产品版本发布对象、公开发布公告源文件、发布校验记录和 Mintlify 文档配置。
- `releases/vX.Y.Z/usage-docs/` 只允许在该版本确认需要生成或更新产品使用文档时创建；确认不需要时 MUST NOT 创建空目录。
- `usage-docs/` MUST 只存放该版本公开产品使用文档源文件、`manifest.json` 和必要的 Mintlify 页面源文件，不得替代 `docs/`、`issues/`、`iterations/` 或 `openspec/`。
- `releases/vX.Y.Z/image-build-plan.json` 与 `image-manifest.json` 属于发布校验材料，MUST NOT 包含真实 `.env`、密钥、数据库连接串、Authorization header、Cookie、本机绝对路径或真实客户数据。
- 镜像 tar 包、`.sha256` 与其他大体积交付物 MUST 放在仓库外 `../releases/vX.Y.Z/images/`；仓库内 manifest 只记录相对路径、hash 与验证结论。
- `releases/` MUST NOT 替代 `iterations/` 四件套、`issues/` 需求/BUG 文档、`openspec/changes/` 变更事实源或 `docs/` 长期技术文档。
- `releases/` MUST NOT 存放运行时生成站点、构建产物、真实客户数据、密钥、数据库连接串或不可公开运维信息。
- 若 Mintlify 生成输出目录存在，MUST 在 `.gitignore` 或相邻 README 中声明提交边界。

### 2.2 `mintlify/` 文档站源目录

`mintlify/` 用于承载公开 Mintlify 文档站源文件，不是发布事实源。`releases/vX.Y.Z/usage-docs/` 继续保留该版本全量产品使用文档正文与 `manifest.json`，`mintlify/docs/vX.Y.Z/` 由 release 快照同步或投影生成。

推荐结构：

```text
mintlify/
├── README.md
├── mint.json
├── site-manifest.json
├── assets/screenshots/
├── docs/
│   ├── latest/
│   └── vX.Y.Z/
└── releases/
    └── vX.Y.Z/announcement.mdx
```

边界：

- `mintlify/` MUST 只存放公开站点配置、MD/MDX 页面、公告投影、站点 manifest 和公开截图资产。
- `mintlify/assets/screenshots/` SHOULD 使用 `sha256-<hash>-<semantic-name>.<ext>` 命名，跨版本复用必须在 release manifest 或 site manifest 中记录来源、覆盖页面和复用依据。
- `mintlify/` MUST NOT 存放 `.env`、真实客户数据、密钥、数据库连接串、Authorization header、Cookie、生产私有域名、运行时数据库、日志、构建产物、`node_modules/`、`.mintlify/`、`dist/`、`build/`、`.next/` 或 coverage。
- `mintlify/` 不得替代 `releases/vX.Y.Z/release.json`、`releases/vX.Y.Z/usage-docs/manifest.json`、`docs/`、`issues/`、`iterations/` 或 `openspec/`。

### 2.3 `deploy/` 部署矩阵目录

`deploy/` 用于承载本地和生产部署环境矩阵，不是运行时数据目录，也不是云资源管理目录。

推荐结构：

```text
deploy/
├── README.md
├── local/
│   ├── README.md
│   ├── compose.yml
│   └── *.env.example
├── prod/
│   ├── README.md
│   ├── compose.tencent-cos.yml
│   └── *.env.example
└── scripts/
    ├── up.sh
    ├── down.sh
    └── validate-env.py
```

边界：

- `deploy/` MUST 只存放部署矩阵 README、环境化 Compose、可提交 env 示例、部署脚本和部署校验工具。
- `deploy/local/` MUST 表达本地开发环境矩阵；`deploy/prod/` MUST 表达生产或生产等价部署矩阵。
- `deploy/scripts/` SHOULD 承载环境解析、启动、停止和配置校验逻辑；旧 `scripts/docker-up.sh` 与 `scripts/docker-down.sh` 只保留兼容 wrapper。
- `deploy/` MUST NOT 提交真实 `.env`、真实密钥、真实数据库连接串、对象存储凭据、真实客户数据、运行时数据库文件、MinIO 对象数据、镜像 tar 包或离线交付包。真实 `deploy/**/*.env` MAY 作为本地/生产运行配置存在于工作区，但 MUST 保持 Git ignored / untracked；目录结构归档门禁只阻塞已跟踪或待提交的真实 env。

生命周期：

1. `/release-propose <version>` 创建或更新产品版本发布对象。
2. `/release-prepare <version>` 执行发布前校验并生成/更新公告源文件。
3. 若用户确认需要产品使用文档，生成并校验 `usage-docs/`；若确认不需要，记录 skipped 且不创建空目录。
4. `/image-prepare <version>` 在镜像治理适用时生成或更新镜像构建计划。
5. `/image-build <version>` 在需要真实镜像交付时生成 manifest。
6. `/release-publish <version>` 记录发布确认结果和最终公告位置。

命名：

- 版本目录 SHOULD 使用 SemVer 风格，例如 `v0.1.0/`。
- 公告发布时间字段 MUST 使用 `YYYY-MM-DD HH:mm:ss`。

## 3. 源码归属规则

### 3.1 后端代码

后端代码必须放在：

```text
src/backend/app/
```

推荐归属：

```text
src/backend/app/api/              # FastAPI Router
src/backend/app/core/             # 配置、异常、日志、安全等核心能力
src/backend/app/db/               # SQLite连接、schema、迁移辅助
src/backend/app/models/           # 数据模型或ORM模型
src/backend/app/repositories/     # 数据访问层
src/backend/app/schemas/          # Pydantic Schema
src/backend/app/services/         # 应用服务与业务逻辑
src/backend/app/main.py           # 应用入口
```

禁止把后端业务代码放到 `scripts/`、`docs/` 或项目根目录。

### 3.2 Web前端代码

Web展示端与管理端代码必须放在：

```text
src/web/src/
```

推荐归属：

```text
src/web/src/app/                  # 应用入口、路由、布局
src/web/src/pages/                # 页面
src/web/src/features/             # 业务功能模块
src/web/src/components/           # 通用组件
src/web/src/services/             # Axios与API封装
src/web/src/generated/            # Orval生成代码，不允许手工修改
src/web/src/styles/               # 全局样式
```

`src/web/src/generated/` 只能由 Orval 生成，AI 不得直接手写。

### 3.3 微信小程序代码

微信小程序代码必须放在：

```text
src/miniapp/
```

推荐归属：

```text
src/miniapp/pages/                # 页面
src/miniapp/components/           # 组件
src/miniapp/services/             # API调用
src/miniapp/utils/                # 工具函数
```

### 3.4 共享代码

跨端共享类型、常量、错误码应放在：

```text
src/shared/
```

不得把共享定义复制到多个端中。

## 4. 文档归属规则

- 主文档（`docs/00–07-*.md`）与总索引 `docs/README.md`。
- API/测试等治理细则放入 `docs/standards/`（**禁止**在 `docs/` 根目录新增无序号治理 MD）。
- 产品需求放入 `issues/requirements/{plan|review|archive}/REQ-*`（**禁止** `docs/prd/`；**禁止** 在 requirements 根下新建扁平 `REQ-*`）。
- BUG 分析放入 `issues/bugs/{plan|review|archive}/BUG-*`（**禁止** `docs/bugs/`）。
- 故障知识沉淀放入 `docs/knowledge-base/`。
- 迭代文档放入 `iterations/{change|archive}/sprint-xxx/`（**MUST** 含 `sprint.yaml` 四件套，见 `rules/document-governance.md` §4.1、`rules/iterations-lifecycle.md`）；禁止 `docs/iterations/`。
- 产品版本发布对象和公开发布公告源文件放入 `releases/`；禁止用 `docs/` 或 `iterations/` 临时代替产品发布目录。
- Mintlify 公开文档站源文件、多版本使用文档投影、`latest` 指针、公告投影和共享截图资产放入 `mintlify/`；禁止直接绕过 release 快照改写历史产品语义。
- 正式系统能力放入 `openspec/specs/`。
- 开发中的变更放入 `openspec/changes/`。
- 已完成变更放入 `openspec/archive/`。

### 4.1 OpenSpec 归档根目录（MUST）

- 已归档 Change 的唯一合法目录为 `openspec/archive/YYYY-MM-DD-<change-id>/`。
- `openspec/changes/` 只允许存放 active Change：`openspec/changes/<change-id>/`。
- 禁止创建、恢复或继续写入 `openspec/changes/archive/`。该路径是历史兼容路径，只能在迁移脚本、残留引用扫描或测试 fixture 中作为 legacy 字符串出现，不得作为真实目录存在。
- 若发现真实目录 `openspec/changes/archive/`，MUST 立即迁移其子目录到 `openspec/archive/`，确认目标不存在且文件完整后删除空的 legacy 目录，并运行 `python scripts/validate-directory-structure.py`。
- `/opsx-archive` 与 `/sprint-archive` 后置校验 MUST 确认 `openspec/changes/archive/` 不存在。
- Sprint close stale scan MUST 阻断 Sprint 四件套中新生成或 canonical 语义的 `openspec/changes/archive/` 引用；测试 fixture、迁移脚本和兼容读取逻辑可保留该字符串作为 legacy 例外。

## 5. Docker与部署文件规则

- 根目录只允许存在项目级编排文件：`docker-compose.yml`（本地开发 / demo）、`docker-compose.prod.yml`（VPS 生产，外部 MySQL + 自建 MinIO）与 `docker-compose.prod.external.yml`（VPS 生产，外部 MySQL + 外部 MinIO）。
- `deploy/` 下允许环境化 Compose：`deploy/local/compose.yml`、`deploy/prod/compose.tencent-cos.yml` 以及后续经 OpenSpec Change 批准的部署拓扑 Compose。
- 后端镜像构建文件放入 `src/backend/Dockerfile`。
- Web镜像构建文件放入 `src/web/Dockerfile`。
- Web Nginx配置放入 `src/web/nginx.conf`。
- 新部署启动停止和 env 校验脚本放入 `deploy/scripts/`；`scripts/docker-up.sh` 与 `scripts/docker-down.sh` 仅作为兼容 wrapper。
- 镜像构建脚本与 image plan / manifest validator 放入 `scripts/`，例如 `scripts/build-images.sh`、`scripts/validate-image-build.py`。

## 6. AI新增文件前检查清单

AI 在新增文件前必须回答：

```text
□ 是否已有 OpenSpec Change？
□ 新文件是否属于已有目录职责？
□ 是否需要更新 rules/directory-structure.md？
□ 是否需要更新 AGENTS.md 的目录说明？
□ 是否需要更新 README.md？
□ 是否需要补充测试？
□ 是否需要同步 Orval 生成代码？
```

## 7. 禁止事项

- 禁止在根目录新增业务代码文件。
- 禁止将测试代码放入源码目录外的临时目录。
- 禁止手工修改 Orval 生成代码。
- 禁止在未更新 OpenSpec 的情况下新增业务能力。
- 禁止把 Docker 环境变量硬编码到代码中。
- 禁止用临时目录替代正式目录结构。
- 禁止把已归档 OpenSpec Change 放入 `openspec/changes/archive/`。
