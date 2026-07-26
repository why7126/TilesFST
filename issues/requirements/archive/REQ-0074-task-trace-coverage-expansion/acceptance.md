---
requirement_id: REQ-0074-task-trace-coverage-expansion
title: 任务型接口 Task Trace 覆盖扩展 - 验收标准
status: done
owner: product
created_at: 2026-07-26 13:02:05
updated_at: 2026-07-26 16:56:01
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-010-retrospective.md
cross_cutting_tags: []
---

# 验收标准

## 功能 AC

- [ ] AC-001 系统 MUST 输出首批 Task Trace 接入接口清单，至少评估保存 SKU、批量操作、导入导出、媒体处理、异步任务和复杂查询六类场景。
- [ ] AC-002 首批清单中每个接口 MUST 标注任务类型、接入优先级、关键步骤、预期 span、是否异步、是否批量、是否涉及对象存储或外部依赖。
- [ ] AC-003 未纳入首批的候选接口 MUST 记录未接入原因和后续排期建议。
- [ ] AC-004 首批任务型接口 MUST 生成或接收可信 `task_trace_id`，并在响应、请求日志、审计日志和 task span 中保持一致。
- [ ] AC-005 前端、子请求或异步任务传入的 `task_trace_id` MUST 做格式校验，不得作为权限判断依据。
- [ ] AC-006 异步任务和后台 worker MUST 继承原始用户请求的 `task_trace_id`；无法继承时 MUST 记录降级 span 或关联缺失原因。
- [ ] AC-007 系统 MUST 提供统一 Task Trace helper 或等价封装，支持生成、透传、上下文绑定和 span 写入。
- [ ] AC-008 每个 span MUST 至少包含 `task_trace_id`、`span_name`、`status`、开始时间、结束时间或耗时。
- [ ] AC-009 span SHOULD 包含 `request_id`、`actor_user_id`、`resource_type`、`resource_id`、错误码、摘要和脱敏 metadata。
- [ ] AC-010 复杂保存类任务 MUST 覆盖参数校验、业务校验、主记录保存、关联资源保存、媒体关联、审计记录和响应阶段。
- [ ] AC-011 批量任务 MUST 覆盖批量解析、单项处理、成功 / 失败计数、部分失败摘要和最终结果阶段。
- [ ] AC-012 导入导出任务 MUST 覆盖文件接收或生成、解析、校验、持久化、结果文件生成和任务状态更新阶段。
- [ ] AC-013 媒体处理任务 MUST 覆盖校验、对象存储、元数据提取、后处理、数据库更新和失败回滚或补偿阶段。
- [ ] AC-014 复杂查询任务 SHOULD 覆盖查询条件解析、权限过滤、数据库查询、聚合统计和响应序列化阶段。
- [ ] AC-015 任务失败时 MUST 写入失败 span，并记录统一错误码或失败摘要。
- [ ] AC-016 超时任务 MUST 能区分用户请求超时、后台处理超时和外部依赖超时。
- [ ] AC-017 批量任务出现部分成功时 MUST 记录成功数、失败数和失败分类摘要。
- [ ] AC-018 系统 SHOULD 能标识最慢 span 或超过阈值的慢节点。
- [ ] AC-019 管理端复杂任务成功、失败或处理中反馈 SHOULD 展示 `task_trace_id` 或提供复制入口。
- [ ] AC-020 复制 `task_trace_id` 的成功或失败反馈 MUST 不造成页面布局位移。
- [ ] AC-021 没有 Task Trace 的旧任务或普通操作 MUST 保持现有交互，不出现空错误态。
- [ ] AC-022 首批任务型接口产生的请求日志、审计日志和 task span MUST 能通过 `task_trace_id` 串联。
- [ ] AC-023 日志审计详情 SHOULD 能展示新增任务类型的 span 时间线，并复用 `REQ-0069` 的权限和脱敏边界。
- [ ] AC-024 若接口响应新增 `task_trace_id` 或任务摘要字段，MUST 同步 OpenAPI、Orval 和前端类型。
- [ ] AC-025 若新增或调整 Task Trace 存储字段，MUST 同步 SQLite / MySQL schema、数据库文档和迁移策略。
- [ ] AC-026 后端 MUST 补充首批任务型接口的单元或集成测试，验证 `task_trace_id` 生成、透传、span 写入、失败节点和部分成功记录。
- [ ] AC-027 Web 管理端 SHOULD 补充追踪标识展示、复制反馈和错误提示的最小测试。
- [ ] AC-028 Docker Compose 或生产 smoke 是否必须执行，MUST 在后续 OpenSpec tasks 中按涉及的后端、Web、对象存储、异步任务范围明确；涉及真实上传、生产 DB 或对象存储边界时，不得只留到 archive 阶段补证据。
- [ ] AC-029 Task Trace metadata MUST 不保存 Authorization、Cookie、AccessKey、SecretKey、数据库 DSN、`.env` 内容、真实客户数据、完整敏感请求体、用户本地绝对路径或未授权对象存储地址。
- [ ] AC-030 管理端 Task Trace 查询与详情查看 MUST 复用系统管理员权限边界，非授权用户不得通过直链查看。

## 横切 AC（knowledge-base）

N/A。本 REQ 不是管理端 CRUD 列表页、表单页、弹窗 CRUD 或上传回显类 UI 需求，未命中 `admin-list`、`admin-form`、`admin-modal`、`media-upload` 标签，因此不生成 AC-XCUT。后续若 OpenSpec design 将日志审计列表筛选、上传控件或弹窗纳入实际改动范围，MUST 重新读取对应 best-practices 并补充 AC-XCUT。
