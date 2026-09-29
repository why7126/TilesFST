---
note: workflow-sync — 11/13 Change 已 archive；0 applied；待人工 sign-off
title: sprint-029 验收报告
created_at: 2026-08-30 15:36:34
updated_at: 2026-09-11 09:17:40
---

# sprint-029 验收报告

## 验收范围

### REQ-0132 远程协议与部署准备（2026-09-11）

扩大回归后的聚焦复跑 116 passed；品牌媒体测试独立运行仍有三项 404/429（22 passed / 3 failed），根因 unknown，未自动创建 Issue。不可据此认定全仓回归通过，复现命令和独立建议见远程验收记录。

官方 MCP SDK 通过真实 loopback HTTP 完成初始化、通知、工具发现/调用及 ping；协议测试 25 项、既有连接器回归 61 项通过。独立非 root Compose 七类检查通过，含鉴权拒绝与卷重启后同键阻断。证据和边界见 `openspec/changes/add-workbuddy-custom-connector/remote-acceptance.md`；不是 HTTPS/真实账号/WorkBuddy 原生远程或跨主机验收，8.1、8.3 仍 pending。

### REQ-0132 本地隔离验收（2026-09-08）

独立 Docker / SQLite / MinIO 与真实 stdio 驱动完成全部写入、五种只读、六种预览、1 MiB 测试边界、对象/URL、四进程同键单写、容器重启、实际请求日志及全部管理写请求 Trace/spans 关联。补齐品牌/类目 Trace，修正 DISABLED 下架语义及媒体前置防护。详细证据、根因与复跑入口见 `openspec/changes/add-workbuddy-custom-connector/local-acceptance.md`。

本地任务 8.2 完成；8.1 HTTPS 原生、8.3 跨主机共享目录及企业保留/恢复策略仍未完成。不是原生远程客户端、生产大文件/视频播放或 MySQL 验收；REQ 仍 pending。下列 2026-09-06 段落为历史证据，其未完成项以本节及最新证据为准。

### REQ-0132 安全与完整性返修

本地 pytest 52 passed：覆盖 Pydantic 参数/基础 payload 校验、预览缺失字段、确认与 scope、持久化同键去重/并发/跨进程/未知结果、远程用户凭据隔离与撤销、后端过期/角色拒绝、限流和审计脱敏。中文 Skill、幂等恢复与远程凭据迁移文档已同步。

证据边界：本轮为本地自动化测试；HTTPS 原生客户端、实际多主机共享卷、全部业务写入、媒体对象/URL 和 request_logs/Task Trace 落库仍未完成。REQ acceptance 保持 pending，不能依据此前任务全勾选整体归档。详细 AC 对照位于 REQ-0132 acceptance，根因及测试入口位于 Change trace。

### REQ-0132 原生连接器验证

2026-09-06 14:31:56，本机配置修正、凭据刷新和 MCP 文本内容块修复后，WorkBuddy App 原生验证报告显示搜索 ok=true、分页大小及条数均为 10，目录摘要 ok=true、sample_count=5。证据入口为 Change trace 的原生连接器验收返修记录；本地回归测试 30 passed。仅确认这两项本机只读调用，远程 HTTPS 与其他能力不据此判定通过。

### REQ-0132 分页返修证据

本次修复 search_tile_skus 分页 schema 与后端不一致，以及 summarize_catalog 样本数直接用作分页的问题。修复前聚焦测试 12 failed / 15 passed；修复后结果见 `openspec/changes/add-workbuddy-custom-connector/trace.md` 的分页验收返修记录。证据来自本地 pytest 与后端枚举契约检查，未重新执行 WorkBuddy 原生连接器或 HTTPS 企业部署验收；整体仍待人工验收。

观测适用层级为 backend_api、request_logs，沿用来源头与 API adapter；无新增行为事件、DB、Task Trace、UI、部署或对象存储变更。

| 类型 | 编号 | 标题 | 状态 | 说明 |
|---|---|---|---|---|
| REQ | REQ-0132-workbuddy-custom-connector | 腾讯 WorkBuddy 自定义连接器支持 | in_progress（`add-workbuddy-custom-connector` 42/44） | 已纳入 sprint-029；待 `/req-opsx` 创建 OpenSpec Change 后进入实现与验收 |
| BUG | BUG-0148-miniapp-product-list-card-image-fit | 小程序商品列表 grid 卡片图片无法完整显示 | done，已归档（`fix-miniapp-product-grid-image-fit` archived 2026-09-07 22:55:02） | 已纳入 sprint-029；待 `/bug-opsx` 创建 OpenSpec Change 后进入实现与验收；key/object/URL 为 n/a，渲染证据待实现阶段补齐 |
| Change | enforce-product-version-release-gates | 产品版本号发布强门禁 | archived | release validator、image input hash、技能、规则和治理校验已同步 |
| Change | simplify-single-release-target-governance | 单一项目发布治理收敛 | archived | release / upgrade validator、技能、规则、v1.2.2 无后缀升级计划和治理校验已同步 |
| Change | automate-product-version-release-prepare | PRODUCT_VERSION 发布准备自动同步 | applied | release-prepare 自动同步版本源、release metadata 与公告版本状态；image-prepare 前置阻断版本源不一致 |
| Change | make-release-propose-next-step-prepare | release-propose 下一步收敛 | archived | release-propose 默认下一步调整为 release-prepare，release-status 保持只读排查入口 |
| Change | converge-release-prepare-automation | 发布准备自动化策略收敛 | applied | release-propose 声明公告、usage docs、升级路径决策；release-prepare 统一生成和校验；release-publish 只确认 |
| Change | define-connector-directory-boundaries | 连接器目录边界 | applied | `src/mcp/<connector>/` 与 `connectors/<connector>/` 边界已写入规则、入口说明、文档索引和目录校验 |

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-30 15:47:12
accepted_by: Codex / spec-opt
evidence:
  - "聚焦测试：tests/test_release_validation.py 4 passed。"
  - "当前 v1.2.2 development publish validation 通过。"
  - "OpenSpec validate、目录结构、上下文预算、Sprint scope、Workflow Sync 和 AI Usage hook 通过。"
  - "文档卫生校验仅返回既有启发式 warning，无阻断。"
pending_items: []
failed_items: []
notes: 纯治理 Change；API、DB、Web、小程序业务实现、管理端、Orval 与 Docker Compose 不适用。
```

```yaml
acceptance_status: passed
accepted_at: 2026-08-31 09:17:22
accepted_by: Codex / spec-opt
change: converge-release-prepare-automation
evidence:
  - "脚本编译：validate-release、validate-release-upgrade、generate-usage-docs、validate-usage-docs 通过。"
  - "聚焦测试：tests/test_release_validation.py 与 tests/test_release_upgrade_validation.py 共 51 passed。"
  - "OpenSpec validate converge-release-prepare-automation 通过。"
  - "上下文预算、OpenSpec 语言、目录结构、Sprint scope 校验通过。"
  - "文档卫生校验仅返回兼容旧字段和历史状态相关启发式 warning，无阻断。"
pending_items: []
failed_items: []
notes: 纯治理 Change；API、DB、Web、小程序业务实现、管理端、Orval 与 Docker Compose 不适用。
```

```yaml
acceptance_status: passed
accepted_at: 2026-08-30 22:41:57
accepted_by: Codex / spec-opt
change: automate-product-version-release-prepare
evidence:
  - "脚本编译：validate-release 与 validate-image-build 通过。"
  - "聚焦测试：release validator PRODUCT_VERSION 自动同步与 image prepare 前置阻断相关 5 passed。"
  - "当前 v1.2.2 release prepare、publish、status、image plan 和 image manifest 校验通过。"
  - "OpenSpec、目录结构、上下文预算、Sprint scope、Workflow Sync 和 AI Usage hook 通过。"
pending_items: []
failed_items: []
notes: 纯治理 Change；API、DB、Web、小程序业务实现、管理端、Orval 与 Docker Compose 不适用。
```

```yaml
acceptance_status: passed
accepted_at: 2026-08-30 22:01:44
accepted_by: Codex / spec-opt
change: simplify-single-release-target-governance
evidence:
  - "聚焦测试：release target 收敛相关 pytest 15 passed。"
  - "当前 v1.2.2 release publish/status、两条无后缀 upgrade plan 和 image manifest 校验通过。"
  - "旧 --target production 入参仅兼容读取，未触发生产专属发布门禁。"
  - "OpenSpec validate、目录结构、上下文预算、Sprint scope、Workflow Sync 和 AI Usage hook 通过。"
  - "文档卫生校验仅返回启发式 warning，无阻断。"
pending_items: []
failed_items: []
notes: 纯治理 Change；API、DB、Web、小程序业务实现、管理端、Orval 与 Docker Compose 不适用。
```

## REQ-0133 验收计划

状态：not_started。事实源为 `issues/requirements/archive/REQ-0133-miniapp-price-red-display/acceptance.md`，10条功能、4条原型证据和3条观测边界AC均待执行。重点覆盖跨入口状态切换、独立推荐与收藏价格、实际背景对比度、TS/JS一致性及其他端无变化。

既有单项通过记录不覆盖REQ-0133。HTML候选及静态计算不作为真机或体验版通过证据；UI Contract、Skeleton、实际样式、PNG和视觉验证由关联Change承接。当前Sprint包含未验收范围，不能据早期单项passed认定整体通过。

## REQ-0134 验收计划

状态：开发验收通过。事实源为 `issues/requirements/archive/REQ-0134-miniapp-public-page-sharing/acceptance.md`；Change 14/14项，28条开发AC通过、AC-023真机豁免。JS/TS各30项及pytest98项通过；异常素材原生双渠道证据、HTTP摘要与设置恢复见Change evidence/media-acceptance.md。Change已于2026-09-08归档。

观测适用miniapp、usage_events；请求封装复用，API/DB/request_logs/保留周期无契约变化，Task Trace因无新复杂任务为N/A，Orval与Docker无需新增验证。既有单项passed不覆盖本需求，不能表示Sprint整体验收通过。

## REQ-0135 验收计划

状态：not_started。事实源为 `issues/requirements/review/REQ-0135-authorized-cos-direct-upload/acceptance.md`：18条功能/非功能及6条横切AC均待执行。C-001～004为对应阶段实现前条件，C-005为UI实施及交付证据。视频验收不能代表整个REQ通过。

覆盖越权、分片总大小与类型伪装、续期、重复确认、确认后覆盖、取消晚到、重启、复制/DB补偿与清理竞态，以及图片派生和全入口回显。按对象、API字段、响应、render四联留脱敏证据；Mock、Compose、生产及真机分别声明。API/DB/Orval/日志/行为/任务观测由AC-016～018约束，暂无运行时通过证据。性能阈值与样本数先冻结后测试。
