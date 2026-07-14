## Why

`REQ-0032` 已沉淀 Web 管理端 Clipboard copy helper，但后续调用方仍需要一份长期可发现的 best-practice 文档来统一文案、fallback 和敏感值边界。若只依赖 helper 代码或单个 README 小节，新增复制入口仍可能出现提示文案漂移、失败路径无反馈、敏感值被误复制或误写入日志的问题。

## What Changes

- 新增 Clipboard helper best-practice 文档要求，明确文档落位、索引入口和适用范围。
- 规范调用方在 `success`、`failed`、`unavailable`、`empty` 等结果下的文案原则。
- 规范 fallback 策略，包括自动复制失败、Clipboard API 不可用、空值、手动选择文本等场景。
- 明确允许复制、谨慎复制、禁止或默认不复制三类敏感值边界。
- 要求文档提供调用方 checklist、示例与反例，供后续代码评审和 QA 验收使用。
- 不新增后端 API、数据库、Orval、小程序复制适配或 Web 管理端运行时 UI。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `clipboard-copy-helper`: 增加 Clipboard helper best-practice 文档化要求，补齐调用方文案、fallback、敏感值边界和 checklist 的规格约束。

## Impact

- 文档：新增或更新 `docs/knowledge-base/best-practices/clipboard-fallback.md` 或等价 best-practice 文档，并从 `docs/knowledge-base/README.md` 建立入口。
- Web 文档：视实现方案更新 `src/web/README.md`，从 Web 前端使用约定入口链接到 best-practice 文档。
- 测试：不新增自动化测试要求；实现验收以文档内容和索引入口检查为主。
- API / 数据库 / MinIO / Docker / 小程序：无影响。
