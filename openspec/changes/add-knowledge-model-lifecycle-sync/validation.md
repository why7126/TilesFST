---
created_at: 2026-09-10 22:59:13
updated_at: 2026-09-10 22:59:13
source_requirement: REQ-0138-knowledge-model-lifecycle-sync
iteration: sprint-030
---

# 实现验证记录

## 结果与证据边界

证据来源为本地治理实现与隔离 Git 仓库预演。真实 Change 归档、Sprint 关闭和产品发布尚待后续工作流验证。业务 API、数据库、Web、小程序、管理端与对象存储契约均未修改，不需 Orval 或 Docker Compose 验证。

- 相关回归命令：`python -m pytest tests/governance/test_knowledge_model.py tests/test_sprint_archive_readiness.py tests/test_release_validation.py tests/test_validate_directory_structure.py tests/test_archive_change_script.py -q`，113项通过。
- 模型细化后补验：语义、类型绑定、事件载荷、模板与完整隔离闭环6项通过。全部新增测试共42项；其中41项进入上述完整回归，新增事件载荷用例进入补验。
- 模型校验：53个类型、15个领域元素、25个关系定义及能力问题通过。计数来自本仓库实际加载，不引用外部合同示例的未核验数字。
- 目录结构、Agent上下文预算、Sprint scope、OpenSpec strict、OpenSpec语言、产品数据采集门禁和文档表达卫生均通过。

## 验收映射

| AC | 实现与本地证据 |
|---|---|
| 001～003、023 | registry、独立结构Schema、元本体和研发本体；非法类型/关系、必要属性、命名空间及多类型组合测试 |
| 004～005、025～027 | M1/M2/M3/M4/M5实例、对应正式规格来源；SKU品牌/类目/规格基数、历史兼容、类目循环、角色权限与行为绑定测试；M6/M7/ME/M9明确未覆盖 |
| 006～007、029 | 固定Commit、文件摘要、规范化trace来源、本体/映射版本；dirty来源拒绝、覆盖审核过期、候选与强规则分离测试；多前提引用保留在模型依赖中 |
| 008～009 | promotion收尾hook、单Change恢复、源码符号映射与反向引用；自举文档、独立Change、跨Change关系、删除、重命名和发布范围子集测试 |
| 010～012 | Sprint readiness知识报告；stale、failed、高风险未决项和强规则冲突阻断；force不绕过；低风险项和candidate告警 |
| 013～015、028 | 完整快照、依赖文本与摘要、Git基线、模型/映射/提取器版本、发布绑定、输入漂移和发布后冻结；体积/数量等于阈值及超限测试 |
| 016～019 | generation原子切换、文件锁、重复事件、多Change并发、切换前后故障和回执IO故障恢复、generated篡改、冻结trace测试 |
| 020～021 | test_self_change_rehearsal复制本真实Change资料与SKU来源，仅在隔离仓库内模拟完成任务和提交；真实后续流程证据仍未取得 |
| 022、OBS-002 | 固定错误码与结构化回执，不持久化异常原文；清理31天运行回执且保留generation测试 |
| 024 | ownerEntity目标类型、必要引用、未知模板、行为输入与事件载荷绑定正反例 |
| OBS-001 | product_data_collection_observability为not_applicable；无产品请求、业务日志、Task Trace或数据采集层变更；专项门禁通过 |

## 来源固定核对

本地工作区核对基线为 `7a03ff4c97a6e4eab60b9106b55abe42c3b7db68`。下面的摘要描述检查时的工作区内容，不把不一致内容归属到该Commit。正式同步还会要求归档资料、本体、映射和相关Issue来源均可在同一固定输入Commit中核对。

| 来源 | 工作区SHA-256 | 与基线一致性 |
|---|---|---|
| `openspec/specs/tile-sku-management/spec.md` | `67b1bc5a2fbfdb13f70d98a0d599696dc8684520b17cd3ca33dc90fb268d3af3` | 一致 |
| `src/backend/app/api/v1/admin_tile_skus.py` | `503da887c1150808411787234e29113c1a95482a53e852f5cee5190eceb29bd5` | 不一致，正式同步前需固定提交 |
| `src/web/openapi.json` | `87b64bbeeef41f2e5fbfe45cb811f64a1577a53b0e01367c1c6d6c54c6acdb04` | 不一致，正式同步前需固定提交 |

测试仓库为临时隔离Git仓库，使用上述真实资料副本生成独立提交，其Commit只证明预演输入固定，不能作为产品正式发布证据。未提交业务文件为已有工作区内容，本Change没有修改它们。

## 后置证据入口

1. 正常验收与OpenSpec归档后，在既有Git流程提交归档来源；若返回source_revision_pending，使用单Change sync恢复。
2. Change trace记录实际同步generation与输入Commit，独立回执记录恢复状态；冻结后只追加独立回执。
3. sprint-030最终关闭时保存真实一致性报告。
4. 实际版本prepare生成并提交完整快照，publish校验绑定并由发布确认记录正式状态。

## 实现限制

条件验证为白名单声明式规则，不执行任意表达式或真实业务动作。未发布候选漂移时拒绝直接覆盖，需核对后清除旧候选再prepare。进程级锁和原子切换覆盖并发与进程异常，未声称断电事务。历史generation保守保留，运行回执保留30天。当前试点仅此Change，范围外返回原因。

## 执行链路复盘

需求评审、Sprint范围、OpenSpec实施、隔离预演与治理校验已贯通。检查中修复了force绕过知识门禁、领域来源定位过宽及trace回执影响来源幂等的问题，均在本需求范围内处理。后续保持归档输入提交与同步恢复的顺序；无额外范围扩展或自动创建follow-up。
