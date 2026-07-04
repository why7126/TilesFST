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
18. rules/requirement-management.md   # 需求 req-* 命令与状态机
19. rules/bug-management.md            # 缺陷 bug-* 命令与状态机
20. rules/issues-lifecycle.md          # issues plan/review/archive 阶段目录
21. rules/iterations-lifecycle.md      # iterations change/archive 阶段目录
22. 当前任务对应的 openspec/changes/<change-id>/
```

如果任务涉及 Docker 部署，还必须读取：

```text
docs/02-deployment.md
docker-compose.yml
src/backend/Dockerfile
src/web/Dockerfile
src/web/nginx.conf
```

如果任务涉及 Web UI、Design System 或前端样式，还必须读取：

```text
rules/ui-design.md
src/web/README.md
src/web/src/styles/globals.css
src/shared/design-system/tokens/
src/web/src/pages/dev/DesignSystemPage.tsx   # 验收页参考
```

如果任务涉及接口变更，还必须读取：

```text
docs/README.md
docs/03-api-index.md
docs/standards/api-governance.md
docs/standards/error-codes.md
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

### 3.1 文档时间与元数据

AI 新增或更新任何项目文档时：

1. **所有时间属性字段** MUST 使用 `YYYY-MM-DD HH:mm:ss`（24 小时制，默认时区 `Asia/Shanghai`）。见 `rules/document-governance.md` §2.3。
2. **AI 自动生成的 Markdown**（含 YAML Frontmatter）MUST 包含 `created_at` 与 `updated_at`；更新文档时只改 `updated_at`，不得改 `created_at`。见 `rules/document-governance.md` §2.4。

适用范围包括 Frontmatter、`lifecycle`、变更记录、评审记录、Sprint 起止时间、里程碑、验收报告、发布说明、OpenSpec 归档记录等。纯目录名、文件名、版本号、需求/BUG 编号中的日期片段可保持既有命名规则。

## 4. AI 开发流程

```text
需求 / BUG（类型未决时先用 /capture）
↓
issues/（requirements 或 bugs）
↓
/capture  或  /req-capture … /req-review  或  /bug-capture … /bug-review
↓
/req-opsx 或 /bug-opsx  →  openspec/changes/
↓
/sprint-propose  →  iterations/change/（仅 approved REQ/BUG）
↓
/sprint-apply  或  /opsx-apply  →  src/
↓
/sprint-archive  或  /opsx-archive
↓
/sprint-exps（可选）→  docs/knowledge-base/retrospectives/
```

### 4.1 OpenSpec CLI 与 Cursor 命令

**命令源与同步**：`.cursor/commands/` 为 slash 命令的**唯一事实源**。新增或修改命令后运行：

```bash
python scripts/sync-agent-commands.py
```

同步目标：

| 工具 | 路径 | 说明 |
|------|------|------|
| Cursor | `.cursor/commands/*.md` | 源（含 `name` / `id` frontmatter） |
| Claude Code | `.claude/commands/{group}/*.md` | 分组子目录 + 扩展 frontmatter |
| OpenCode | `.opencode/commands/*.md` | 扁平 `description` frontmatter |
| Kiro | `.kiro/prompts/*.prompt.md` | 扁平 prompt 文件 |
| Codex | `.codex/prompts/*.md` | 自定义 slash（deprecated，推荐 `.codex/skills/` 承载 OpenSpec 技能） |

#### 统一入口（类型未决）

| 阶段 | Cursor 命令 | 说明 |
|------|-------------|------|
| 智能收集 | `/capture` | 自动区分 REQ/BUG，按需拆分；分别走 req-capture / bug-capture 落盘 |

类型已知时仍直接使用 `/req-capture` 或 `/bug-capture`。

#### 需求域（req-*）

| 阶段 | Cursor 命令 | 说明 |
|------|-------------|------|
| 记录 | `/req-capture` | 轻量 capture.md，分配 REQ-ID |
| 探索 | `/req-explore` | 只思考，默认不写文档 |
| 生成 PRD | `/req-generate` | **仅** `requirement.md` |
| 完善六件套 | `/req-complete` | user-stories、acceptance、prototype 等 |
| 评审 | `/req-review` | **approved** 后方可 opsx、**写入 Sprint 正式规划** 与 sprint-apply |
| **REQ → Change** | **`/req-opsx REQ-xxxx`** | 须 approved；CLI 生成 OpenSpec |

#### 缺陷域（bug-*）

| 阶段 | Cursor 命令 | 说明 |
|------|-------------|------|
| 记录 | `/bug-capture` | capture.md，分配 BUG-ID |
| 探索 | `/bug-explore` | 只思考，默认不写文档 |
| 生成 | `/bug-generate` | **仅** `bug.md` |
| 完善 | `/bug-complete` | root-cause、acceptance 等 |
| 评审 | `/bug-review` | approved 后方可 opsx、**写入 Sprint 正式规划** 与 sprint-apply |
| **BUG → Change** | **`/bug-opsx BUG-xxxx`** | 须 approved；默认 `fix-*` |

#### Change 级（opsx-*）

| 阶段 | Cursor 命令 | 说明 |
|------|-------------|------|
| 补全 REQ 文档 | `/req-complete REQ-xxxx` | 文档不全时（非 opsx） |
| 视觉/策略未决 | `/opsx-explore` | UI 原型策略 |
| 无 REQ 快速建 change | `/opsx-propose <change-name>` | 探索性改动 |
| 实现（单 Change） | `/opsx-apply <change-name>` | 改 `src/`、测试 |
| 归档（单 Change） | `/opsx-archive <change-name>` | 合并 specs |

#### Sprint 级（sprint-*）

| 阶段 | Cursor 命令 | 说明 |
|------|-------------|------|
| **创建 Sprint** | **`/sprint-propose [sprint-xxx]`** | 四件套；**仅纳入已评审（approved / in_sprint）REQ/BUG**；未评审仅可列「延后项（待评审）」 |
| 探讨 | `/sprint-explore [sprint-xxx]` | 范围/依赖/容量 |
| **开发** | **`/sprint-apply sprint-xxx`** | 排队 opsx-apply；校验已评审 |
| **归档** | **`/sprint-archive sprint-xxx`** | 批量 opsx-archive |
| **经验复盘** | **`/sprint-exps sprint-xxx`** | 总结迭代经验，沉淀 `docs/knowledge-base/retrospectives/` |

推荐链：`/sprint-archive` → `/sprint-exps` → 下一 `/sprint-propose` 参考行动项。

#### 基础设施（Bootstrap）

| 命令 | 说明 |
|------|------|
| `/initialize-project` | 一次性：DS + API + Test + Docker + Sprint-000 |
| `/build-design-system` | Design System 资产与校验 |
| `/build-api-standard` | API 治理与 Orval |
| `/build-test-framework` | 测试治理与 CI |

治理扩展须新 REQ + `/req-opsx`；勿重复创建已归档 `build-*` change。

**已删除的旧命令**（勿再使用；Cursor 命令列表仅保留新名）：

| 旧命令 | 替代 |
|--------|------|
| `/requirement-to-change` | `/req-complete` |
| `/requirement-to-opsx` | `/req-opsx` |
| `/bug-to-change` | `/bug-opsx` |
| `/create-iteration` | `/sprint-propose` |

**命令文件**：`req-*.md`、`bug-*.md`、`sprint-*.md`；`initialize-project.md`、`build-*.md`；规范见 `rules/requirement-management.md`、`rules/bug-management.md`。

### 4.2 Change 类型与命名

| 场景 | 类型 | 命名示例 |
|------|------|----------|
| 新能力 | `add-*` | `add-user-login` |
| 验收/视觉不达标、策略变更 | `fix-*` | `fix-login-css-port` |
| 规范/文案对齐 | `update-*` | `update-login-acceptance-sync` |

已有 archived `add-*` 且原型/PNG 验收未过时，**MUST** 新建 `fix-*` change，禁止在原 change 上无 spec 地硬改代码。

### 4.3 UI 原型优先级（有 prototype 时强制）

存在 `issues/requirements/.../prototype/` 时，design.md **MUST** 声明优先级：

```text
1. prototype/*.html
2. prototype/*.png（Golden Reference）
3. prototype/*-context.md
4. issues/.../acceptance.md
5. rules/ui-design.md
6. openspec/specs/（已归档能力）
```

`acceptance.md` 与 HTML/PNG 冲突时，以 HTML 为准，并在 delta spec 中用 MODIFIED/REMOVED 消化（见 `req-opsx` Step 3）。视觉类 change 的 `tasks.md` **MUST** 含 PNG 并排 checklist 与 `trace.md` 记录。

## 5. 强制规则

- 不允许绕过 OpenSpec Change 直接开发功能。
- 不允许直接修改 `openspec/specs/` 中的正式规范，除非是归档合并动作。
- 不允许在根目录新增业务代码。
- 不允许绕过 `rules/directory-structure.md` 新增目录。
- 产品版本发布对象与公开发布公告源文件必须放入 `releases/`，且 `releases/` 仅可在 OpenSpec Change 明确授权后创建和使用。
- 后端必须使用 Python3.12、FastAPI、Pydantic、uv、SQLite、MinIO。
- 前端必须使用 React19、TypeScript、Tailwind、shadcn/ui、Axios、Orval、pnpm。
- 部署必须优先支持 `docker-compose.yml`。
- API 修改后必须同步 OpenAPI，并通过 Orval 生成前端类型与请求客户端。
- 图片上传必须走后端授权与 MinIO 存储，不允许前端直连未授权对象存储。
- 管理端与店主端必须区分权限边界。
- Web UI MUST 遵守 Design System 应用规范（semantic token、组件优先级、禁止裸 Hex）；见本文 **Design System 应用规范**。

## 6. 目录结构执行要求

禁止创建或恢复：

```text
docs/product/
docs/prd/
docs/bugs/
docs/iterations/
```

如需要产品需求，放入：

```text
issues/requirements/plan/REQ-xxxx-xxx/     # 新建
issues/requirements/review/REQ-xxxx-xxx/   # 已评审、开发中
issues/requirements/archive/REQ-xxxx-xxx/  # 已归档
```

如需要BUG记录，放入：

```text
issues/bugs/plan/BUG-xxxx-xxx/
issues/bugs/review/BUG-xxxx-xxx/
issues/bugs/archive/BUG-xxxx-xxx/
```

阶段目录规则见 `rules/issues-lifecycle.md`。

如需要故障知识沉淀，放入：

```text
docs/knowledge-base/incidents/
```

如需要产品版本发布对象或公开发布公告源文件，放入：

```text
releases/vX.Y.Z/release.json       # 机器可读产品发布对象
releases/vX.Y.Z/announcement.mdx   # Mintlify 公开公告源文件
```

`releases/` 不替代 `iterations/`、`issues/`、`openspec/changes/` 或 `docs/`，不得存放运行时生成站点、密钥、真实客户数据、数据库连接串或不可公开运维信息。

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

## 7. 新需求处理流程

AI 收到新输入且**不确定是需求还是缺陷**时，先执行 **`/capture`**；若已明确为新需求，则：

1. 检查 `issues/requirements/` 是否已有相关需求；
2. 如无，执行 **`/req-capture`**（或经 `/capture` 已落盘则跳过）创建 `REQ-xxxx-name/`（含 `capture.md`）；
3. 可选 **`/req-explore`** 探讨；
4. **`/req-generate`** → `requirement.md`；
5. **`/req-complete`** → 六件套（user-stories、business-flow、acceptance、trace、prototype）；
6. **`/req-review`** → **approved**；
7. **`/req-opsx REQ-xxxx-name`** → OpenSpec Change（**MUST** `openspec new change`）；
8. **`/sprint-propose`** 纳入迭代（**仅 approved**）；
9. **`/sprint-apply`** 或 **`/opsx-apply`**；完成后 **`/opsx-archive`** 或 **`/sprint-archive`**。

UI 类若策略未决，**MUST** `/opsx-explore` 或于 `req-opsx` 内选定 CSS Port 等并写入 `design.md`。

## 8. BUG处理流程

AI 收到新输入且**不确定是需求还是缺陷**时，先执行 **`/capture`**；若已明确为缺陷，则：

1. **`/bug-capture`**（或经 `/capture` 已落盘则跳过）创建 `issues/bugs/BUG-xxxx-name/`；
2. 可选 **`/bug-explore`**；
3. **`/bug-generate`** → `bug.md`；
4. **`/bug-complete`** → root-cause、workaround、acceptance、trace、logs/、screenshots/；
5. **`/bug-review`** → **approved**；
6. **`/bug-opsx BUG-xxxx`** → `openspec/changes/fix-*`；
7. **`/opsx-apply`** + 回归测试；**`/opsx-archive`**；
8. 如有价值，更新 `docs/knowledge-base/incidents/`。

## 9. OpenSpec约束

- `openspec/specs/` 是已生效能力，不得随意直接修改；
- 开发中的变更必须放在 `openspec/changes/`，**MUST** 通过 `openspec new change` 创建（见 `/req-opsx`、`/bug-opsx`）；
- 变更完成后用 **`/opsx-archive`**（`openspec archive`）归档到 `openspec/changes/archive/`；
- 归档时才可将能力合并到 `openspec/specs/`；
- delta spec 中 **MODIFIED** 的 `### Requirement:` 标题 **MUST** 与 `openspec/specs/` 中已有标题一致，否则归档失败；
- 每条 requirement **MUST** 含 MUST/SHALL 与至少一个 `#### Scenario:`。

## 10. Docker Compose 部署要求

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

## 11. 输出要求

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


## 12. data目录使用规范

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

## 13. 环境变量规范

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

AI新增或修改以下配置时，必须同步维护邻近注释，说明用途、取值范围、默认值含义或安全边界：

```text
docker-compose*.yml
src/backend/Dockerfile
src/web/Dockerfile
.env
.env.example
src/backend/.env.example
src/backend/.env.docker
```

`.env` 文件禁止提交。

## 14. 视频与媒体资产规范

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

## 15. 项目规则强化

- `data/` 目录及数据治理规范。
- 根目录 `.env.example` 及环境变量治理规范。
- 视频资产管理文档和媒体OpenSpec。
- 面向瓷砖项目深化后的 rules 规范。

AI不得删除上述能力；如需裁剪，必须先创建 OpenSpec Change 并说明影响范围。

## Design System 应用规范

Web 端采用 **工业石材 · 暗色旗舰风** Design System。视觉规范来源为 `rules/ui-design.md`；可执行实现见下表。

### 资源地图

| 层级 | 路径 | 职责 |
|------|------|------|
| 设计规范 | `rules/ui-design.md` | 色彩、字体、间距、组件与页面结构（事实标准） |
| TS Token | `src/shared/design-system/tokens/` | 跨端 Token 定义（颜色结构、间距、圆角、字体、Tailwind config） |
| CSS 颜色 | `src/web/src/styles/globals.css` | Web 颜色 CSS Variables（`:root` 暗色 + `.light` 浅色预留） |
| CSS 非颜色 | `src/web/src/styles/tokens.generated.css` | 间距/圆角/字体/阴影（`pnpm sync:tokens` 生成） |
| Tailwind | `src/web/tailwind.config.ts` | 引用 `@shared/design-system/tokens/tailwind.config.ts` |
| shadcn 基础 | `src/web/src/components/ui/` | Button、Input、Checkbox、Label、Separator 等 |
| 复合 UI | `src/web/src/shared/ui/` | SearchBar、Sidebar、Pagination、Badge、Card 等 |
| 业务组件 | `src/web/src/shared/business/` | ProductCard、FeaturedCard、ProductGrid、TextureRow |
| 页面模板 | `src/web/src/shared/templates/` | LandingPage、ListPage、DetailPage、AdminListPage、AdminEditPage |
| 跨端类型 | `src/shared/business/`、`src/shared/templates/` | 业务/模板 props 类型（无 React 依赖） |
| 设计验收 | `/design-system`（开发环境） | Token + UI + 业务组件预览 |

详细用法见 `src/web/README.md`、`src/shared/README.md`。

### AI 执行 UI 任务前 MUST

1. 读取 `rules/ui-design.md` 对应章节（组件 §5、页面 §6、登录 §9 等）。
2. 打开或对照 `/design-system` 预览页，确认 Token 与组件形态。
3. 确认是否已有可复用组件/模板，**优先组合而非新建**。

### 组件选用优先级（Web）

```text
1. src/web/src/shared/templates/     # 整页或管理端页面骨架
2. src/web/src/shared/business/      # 目录/商品等领域组件
3. src/web/src/shared/ui/            # 复合 UI（SearchBar、Sidebar…）
4. src/web/src/components/ui/        # shadcn 基础组件
5. 仅在上述无法满足时，才新增组件（须走 OpenSpec Change）
```

新增组件 MUST 放入上表对应目录，MUST NOT 在 `features/` 或 `pages/` 内重复实现已有 DS 组件。

### Token 与样式强制规则

- **禁止裸 Hex**：新增/修改 Web UI 代码 MUST NOT 在 TSX/CSS 中硬编码 `#18160F`、`#C8A055`、`rgba(…)` 等 design token 对应值。
- **必须使用 semantic class**，例如：
  - 背景：`bg-page`、`bg-surface`、`bg-deep`
  - 文字：`text-primary`、`text-secondary`、`text-muted`、`text-brand-gold`
  - 边框：`border-border-default`、`border-border-strong`、`border-border-focus`
  - 圆角：`rounded-industrial`（2px）、`rounded-card`（3px）
- **className 合并**：使用 `cn()` from `@/shared/lib/cn`。
- **主题切换**：默认暗色；浅色通过 `.light` 或 `[data-theme="light"]`，MUST NOT 写死仅暗色 Hex。
- **品牌字体**：Logo/品牌名使用 `font-brand`、`tracking-brand`；正文使用系统 sans-serif。

### Token 修改流程

```text
1. 更新 rules/ui-design.md（若规范变更）
2. 更新 src/shared/design-system/tokens/*.ts
3. 颜色：同步更新 src/web/src/styles/globals.css
4. 非颜色：cd src/web && pnpm sync:tokens
5. 提交 tokens.generated.css（Docker 构建上下文不含 src/shared）
6. 更新 /design-system 预览（若新增 Token 或组件）
7. 在 OpenSpec Change 中说明是否影响 Web / 管理端 / 小程序
```

TypeScript 引用示例：

```typescript
import { getColorTokens } from '@shared/design-system/tokens';
import { ProductGrid } from '@/shared/business';
import { SearchBar } from '@/shared/ui';
import { LandingPage } from '@/shared/templates';
```

### 场景指引

| 场景 | 推荐做法 |
|------|----------|
| 店主端首页/目录 | 使用 `LandingPage` / `ListPage` + `sample-content` 数据结构 |
| 商品详情 | 使用 `DetailPage` 或 `FeaturedCard` / `ProductCard` 组合 |
| 管理端列表 | 使用 `AdminListPage` + shadcn Input/Button |
| 管理端表单 | 使用 `AdminEditPage` + Input/Label/Checkbox |
| 登录页 | 沿用 `features/auth` + `IconInput`/`DividerText`；对照 `user-login.md` 与 PNG |
| 新增 shadcn 组件 | `cd src/web && npx shadcn@latest add <name>`，并 override 为 DS Token |

### 设计验收

- 开发环境访问 `http://localhost:5173/design-system`（或 Docker Web 同等路由）。
- 验收范围：全部 Design Token、shadcn 基础、复合 UI、业务组件。
- UI 相关 Change 完成前，AI MUST 确认预览页可展示新增/变更组件，并在 acceptance 中注明。

### Design System 相关 OpenSpec

- 已归档：`openspec/changes/archive/2026-06-13-add-design-system`
- 新增 Token、组件或模板 MUST 通过 OpenSpec Change 进入开发，MUST NOT 绕过规范直接改生产页面。

## 对象存储与端口规范

AI Agent 在处理文件、图片、视频、导入导出能力时，必须遵守：

```text
rules/object-storage.md
rules/media.md
rules/data-management.md
rules/port-management.md
```

### MinIO 规则

采用：

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

默认保留开发友好端口：

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

## 16. 完成任务后检查清单

```text
□ 是否更新 issues/requirements 或 issues/bugs
□ 是否通过 /req-opsx（或 /bug-opsx）创建 openspec/changes
□ 是否已 /opsx-archive 并同步 openspec/specs（若 change 已完成）
□ 是否更新 iterations（含 `sprint.yaml` 与 `sprint.md`）
□ 产品发布：是否更新 releases/ 发布对象、公告源文件与发布校验记录
□ 是否补充 tests
□ 是否更新 docs 长期文档
□ 是否更新 .env.example
□ 是否遵守 MinIO 单桶策略
□ 是否遵守目录结构
□ 是否未创建禁止目录
□ UI 变更：是否使用 semantic token（无裸 Hex）
□ UI 变更：是否复用 templates / business / shared/ui / shadcn 既有组件（登录页等 fidelity 专项可按 design 采用 port CSS）
□ UI 有 prototype：是否按 HTML > PNG > acceptance 优先级，并填写 trace checklist
□ Token 变更：是否同步 globals.css 或执行 pnpm sync:tokens
□ UI 变更：是否可在 /design-system 或原型 PNG 并排验收
```
