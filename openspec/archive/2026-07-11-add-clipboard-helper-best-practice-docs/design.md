## Context

来源需求：`REQ-0036-clipboard-helper-best-practice-docs`。

`clipboard-copy-helper` 现有正式规格已经覆盖 helper 本体、复制安全边界和代表场景测试；`design-system` 与 `web-client` 规格也已要求新增复制入口优先复用共享 helper。当前缺口不是再新增 helper 能力，而是将调用方最佳实践沉淀到长期文档中，使开发、评审、QA 能稳定找到文案、fallback 和敏感值边界。

Sprint 006 复盘已提出 `best-practices/clipboard-fallback.md` 后续新建建议。本 change 将该行动项产品化为 OpenSpec 约束。

## Decisions

### D1. 修改现有 `clipboard-copy-helper` capability

本 change 不新建 capability。所有新增规格放入 `clipboard-copy-helper`，因为 best-practice 文档服务于同一能力边界：Web 管理端 Clipboard helper 及其调用方。

### D2. 文档落位优先级

实现阶段优先新增：

```text
docs/knowledge-base/best-practices/clipboard-fallback.md
```

并同步更新：

```text
docs/knowledge-base/README.md
src/web/README.md
```

若实现阶段选择等价路径，必须在任务或验收中说明为什么该路径更容易被调用方发现。

### D3. 文档内容边界

best-practice 文档必须覆盖：

- 适用范围：Web 管理端 Clipboard helper 调用方；
- 调用方文案：`success`、`failed`、`unavailable`、`empty`；
- fallback：手动选择文本、禁用复制入口、明确失败提示；
- 敏感值：允许、谨慎、禁止或默认不复制；
- checklist：授权可见、敏感值分类、文案、fallback、空值、日志/埋点、测试覆盖；
- 示例与反例：必须使用脱敏或虚构值。

文档不得复制真实密钥、真实 Token、真实客户隐私数据或真实生产签名 URL。

### D4. Conflict Resolution

本 REQ 没有 `prototype/web/`，不涉及 HTML / PNG / context 与 acceptance 的视觉冲突。优先级链路结论：

```text
acceptance.md > rules/security.md > docs/knowledge-base/README.md > src/web/README.md
```

`src/web/README.md` 已有 Clipboard helper 小节；本 change 不要求删除该小节，而是要求它链接到长期 best-practice 文档或保留入口摘要。

## Impact Analysis

```yaml
impact:
  backend: false
  web: true
  miniapp: false
  admin: false
  database: false
  storage: false
  api: false
  docs: true
capabilities:
  new: []
  modified:
    - clipboard-copy-helper
```

## Risks

| 风险 | 缓解 |
|---|---|
| 文档不可发现 | 更新知识库 README，并从 Web README 建立入口。 |
| 文档只写原则不可验收 | 将 checklist、示例、反例写入 tasks 与 AC。 |
| 敏感值示例泄露 | 示例必须使用脱敏或虚构值，不得出现真实凭据。 |
| 与 `REQ-0032` 重复 | 文档明确只约束调用方，不替代 helper 实现。 |

## Verification

- 检查 best-practice 文档存在，且 frontmatter 含 `created_at` / `updated_at`。
- 检查知识库 README 或等价索引包含 Clipboard best-practice 入口。
- 检查 Web README 有入口链接或摘要。
- 检查文档包含调用方文案、fallback、敏感值三类边界、checklist、示例与反例。
- 检查文档示例不包含真实密钥、Token、客户隐私或生产签名 URL。
