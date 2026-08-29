---
requirement_id: REQ-0127-product-data-collection-observability-hard-gate
title: 产品数据采集与链路观测规范硬门禁 - 业务流程
created_at: 2026-08-26 19:55:31
updated_at: 2026-08-26 19:55:31
---

# 业务流程

## 1. 总体门禁链路

```text
用户提出 REQ / BUG / Change / Sprint 范围
  -> 判断是否触发采集规范门禁
      -> API / DB / 日志审计 / 行为埋点 / Task Trace / 端请求封装命中？
          -> 是：读取 docs/standards/product-data-collection-observability.md
              -> 声明适用层级、N/A 原因、API/DB/端/测试影响
                  -> 写入需求、Change 或验收材料
                      -> 运行实现级校验脚本
                          -> 通过后进入评审、实现或归档
          -> 否：记录 not_applicable 原因
              -> 继续原流程
```

## 2. 需求阶段流程

```text
/req-generate
  -> PRD 识别触发范围
      -> /req-complete
          -> user-stories / business-flow / acceptance 写入门禁声明与验收项
              -> trace 记录 knowledge_base_refs 与采集规范事实源
                  -> /req-review 检查是否缺失声明
```

关键规则：

- 需求涉及 API、DB、日志审计、行为埋点、Task Trace 或端请求封装时，必须声明采集规范适用性。
- 不适用时必须说明为什么不影响这些层级。
- `req-complete` 只补齐需求六件套，不创建 OpenSpec Change。

## 3. OpenSpec 阶段流程

```text
/req-opsx 或 /opsx-propose
  -> Change 文档引用采集规范门禁
      -> design / tasks 声明 affected_layers 与 N/A 原因
          -> /opsx-apply 前运行聚焦校验
              -> 实现或治理资产更新
                  -> acceptance / trace 回填校验证据
                      -> /opsx-archive 前复核门禁结果
```

关键规则：

- 触发范围必须在 Change 设计或 trace 中固定格式声明。
- 涉及 API contract 时同步 OpenAPI、Orval、API 文档和测试，或写明不适用依据。
- 涉及 DB 时同步 SQLite / MySQL schema、迁移、数据库设计文档和测试，或写明不适用依据。
- 纯治理 Change 仍必须纳入 Sprint 后才能 apply。

## 4. Sprint 阶段流程

```text
/sprint-propose
  -> 纳入 REQ / BUG / Change
      -> 摘要提示采集规范门禁状态
          -> /sprint-apply
              -> 执行范围内复核适用性或 N/A
                  -> /sprint-archive
                      -> 关闭前复核验收结果和校验脚本摘要
```

关键规则：

- Sprint 只做范围和状态追踪，不替代 Change 设计和验收事实源。
- Sprint 输出使用摘要，不复制 `docs/standards/product-data-collection-observability.md` 正文。
- 归档前发现门禁缺失时，应返回对应 REQ / Change 修复，不手工改 workflow-sync marker 派生块。

## 5. 实现级校验流程

```text
校验脚本启动
  -> 检查 AGENTS.md 是否接入读取路由
  -> 检查相关 rules 是否接入触发条件和声明要求
  -> 检查 req / opsx / sprint 技能是否接入检查清单
  -> 根据目标 Change / REQ / Sprint / diff 识别触发范围
      -> 命中触发范围
          -> 检查 product_data_collection_observability 声明
          -> 检查 affected_layers / reason / validation
      -> 未命中触发范围
          -> 报告 not_applicable 或 skipped 摘要
```

校验输出：

| 结果 | 处理 |
|---|---|
| pass | 报告命中范围、声明位置和验证摘要。 |
| warning | 报告可疑缺失、N/A 理由过短或触发范围不明确。 |
| blocker | 报告缺少入口引用、缺少声明字段、缺少验收证据或敏感输出风险。 |

## 6. 与父 REQ 的差异

| 项 | REQ-0126 | REQ-0127 |
|---|---|---|
| 定位 | 建立通用产品数据采集与链路观测规范正文 | 将该规范接入流程硬门禁 |
| 主要事实源 | `docs/standards/product-data-collection-observability.md` | `AGENTS.md`、`rules/`、技能检查清单、校验脚本和 Change 验收声明 |
| 交付重点 | 字段语义、链路模型、保留周期、脱敏和接入清单 | 必读、必声明、必验收、N/A 原因和脚本校验 |
| 是否改业务实现 | 不直接改业务实现 | 不直接改业务实现 |
| 后续价值 | 提供采集规范基准 | 防止后续相关变更绕过采集规范 |

## 7. Knowledge-base Cross-cutting Report

| 标签 | 引用文档 | 将写入 acceptance 的 AC 条数 | 结论 |
|---|---|---:|---|
| 无匹配 UI 标签 | - | 0 | 本 REQ 为治理门禁和流程规范，不新增管理端列表页、表单页、弹窗或媒体上传 UI；knowledge-base UI gate 为 N/A。 |

复盘参考摘要：

- `sprint-025` 复盘指出 Workflow Sync、OpenSpec、stale scan、residual gate 与 AI usage fresh gate 需要脚本化闭环；本需求把产品数据采集规范也纳入脚本化门禁。
- `sprint-023` 复盘指出观测类页面和治理命令容易遗漏 API、Orval、验收和 Sprint scope；本需求要求相关 Change 在设计与归档前声明采集规范影响。
- `sprint-022` 复盘指出治理 Change 不触碰业务 `src/` 时仍要走 Sprint Inclusion Gate；本需求后续实现也必须先完成评审和 Sprint 纳入。
