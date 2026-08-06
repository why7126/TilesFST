---
name: "build-api-standard"
description: "建立 API Governance（统一响应 / 错误码 / OpenAPI / Orval）"
---

# build-api-standard

Use this skill when the user asks to run the workflow command `build-api-standard`.

## Context Budget Guardrails（MUST）

### Force-proceed Follow-up Guardrails（MUST）

- `force-proceed` 仅允许继续当前命令的非阻断部分，MUST NOT 默认自动创建 follow-up REQ/BUG；除非用户在当前命令中明确授权自动 capture，否则只输出标准 capture 文案，并明确“未自动创建 Issue”。
- 标准 capture 文案 MUST 分条包含：建议命令、类型倾向、标题、背景、影响范围、建议验收或复现要点、来源 Change/Sprint/命令；多个 follow-up 事项 MUST 逐条输出，且每条可独立用于后续 capture。
- 如用户明确授权并实际创建 follow-up Issue，MUST 按 `/req-capture`、`/bug-capture` 或 `/capture` 规则落盘，并运行对应 `req.capture` 或 `bug.capture` Workflow Sync。

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则和 Skill 用摘要承接，不重复全量读取。
- 检索先定位再分段读取；大范围 `rg/find` 默认排除 Harness、模板 assets、历史 agent 目录、archive、generated、node_modules、dist、coverage。
- 命令输出优先 `max_output_tokens <= 8000`；大 diff、OpenAPI/Orval 生成物、测试日志、Workflow Sync 输出先给摘要或命中数。


## Command Template

将 `rules/api.md` 落地为可执行 API 治理：文档、Schema、校验脚本与 FastAPI 分层约定。

**关联 REQ**：`REQ-0000-build-api-standard`（`change_id: build-api-standard`，已归档见 `openspec/specs/api-governance/`）

**Input**：`--verify` 仅校验

---

## 必须读取

```text
AGENTS.md
rules/api.md
rules/security.md
rules/testing.md
rules/coding.md
openspec/specs/api-governance/spec.md
src/backend/app/**
src/web/orval.config.ts
docs/03-api-index.md
```

---

## 与 req / opsx 关系

| 场景 | 做法 |
|------|------|
| 新业务 API | 对应业务 REQ 的 `/sprint-propose` → `/req-opsx` → `add-*` |
| 治理规范变更 | 新 REQ + `/sprint-propose` + `/req-opsx`（MODIFIED `api-governance`） |
| 接口实现后 | **MUST** 更新 OpenAPI + `scripts/generate-openapi-client.sh` |

---

## Step 1 — 治理文档

核对/更新：

```text
docs/standards/api-governance.md
docs/standards/error-codes.md
docs/standards/openapi-rules.md
docs/standards/authentication.md
docs/standards/file-upload.md
docs/03-api-index.md
```

---

## Step 2 — 统一结构

```text
src/backend/app/schemas/common/     # response, pagination, error
src/backend/app/core/error_codes.py
src/backend/app/api/v1/
```

统一响应：`{ code, message, data }`；分页 `page` / `page_size` / `items` / `total`。

---

## Step 3 — OpenAPI First

- 路由须 `response_model`、`summary`、`tags`
- 导出 `src/web/openapi.json` 为契约
- Orval → `src/web/src/shared/api/generated.ts`

---

## Step 4 — 测试与校验

```text
src/backend/tests/                  # 集成测试
scripts/validate-api-standard.py
```

每接口：成功、失败、权限、边界。

---

## Step 5 — OpenSpec

已归档 **勿重建** `build-api-standard`。新治理需求走 `/sprint-propose` 后再 `/req-opsx`。

---

## 验收

```text
□ validate-api-standard.py pass
□ Orval 生成无报错
□ error_codes 与 rules/api.md 一致
```

## Final Output Contract（MUST）

命令结束前，最终回复 MUST 明确包含：

```text
下一步：<可直接执行的命令；若没有则写“暂无可推进下一步”>
待用户决策/处理：
- <需要用户选择、确认、补充或处理的事项；若没有则写“无”>
```

- 如果存在明确可推进的下一步，MUST 给出可复制执行的命令，例如 `/bug-review BUG-0122 --approve`。
- 如果下一步取决于用户选择，MUST 用条件化条目列出选项；已在「下一步」中给出的命令或动作，不得在「待用户决策/处理」中重复。
- 「待用户决策/处理」只列缺失输入、需用户选择的范围/策略/证据/验收/发布确认、阻塞项或需人工处理事项；没有则写“无”。
- 不得因为输出了下一步引导而自动执行下一命令；除非用户明确授权。
