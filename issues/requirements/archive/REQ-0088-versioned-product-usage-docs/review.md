---
review_id: REV-REQ-0088-001
date: 2026-08-01
participants:
  - product
result: approved
created_at: 2026-08-01 09:53:42
updated_at: 2026-08-01 09:53:42
---

# REQ-0088 需求评审

## 评审结论

通过。

REQ-0088「版本化产品使用文档生成与发布治理」范围清晰，已明确产品文档并非每个版本都自动生成，`/release-prepare` 阶段必须先确认本次是否需要生成或更新；需要时才生成 `usage-docs/` 并执行校验，不需要时记录 skipped 状态、确认来源和跳过原因。

本需求属于发布治理 / 产品使用文档 / Mintlify 能力，不直接影响 Web 管理端、小程序、后端 API、数据库或对象存储运行时。需求文档已补齐 `requirement.md`、`user-stories.md`、`business-flow.md`、`acceptance.md` 与 `trace.md`，验收标准可测试，可进入 OpenSpec Change 设计阶段。

## 评审检查清单

- [x] 范围清晰，Out of Scope 明确。
- [x] 验收标准可测试，覆盖生成决策、按需生成、skipped rationale、manifest、Mintlify 导航、公开安全扫描和旧版本维护策略。
- [x] 优先级 P1 合理；该需求影响 release prepare / release publish 治理链路，但不直接影响运行时业务路径。
- [x] UI 类原型不适用；本需求不新增业务 UI，文档站 UI 以 Mintlify 能力为准。
- [x] 与 REQ-0026 产品版本发布与公告管理、REQ-0081 发布镜像准备与构建治理关系已说明，不是重复需求。
- [x] Knowledge-base gate 判定为 N/A；无管理端列表、表单、弹窗或媒体上传 UI 横切标签。

## 条件通过项

- [ ] 后续 `/req-opsx` 生成 OpenSpec Change 时，设计文档需明确 `usage_docs` / `usage_docs_preview` 在 `release.json` 中的字段结构与 skipped / pending_confirmation / generated 状态语义。
- [ ] 后续实现前需确认 `/docs` 访问采用 Mintlify base path、Cloudflare/Vercel/CDN rewrite，还是生产 Nginx 反向代理。
- [ ] 后续实现需避免默认每版生成空文档；必须保留用户确认前置条件。

## 后续建议

```text
/req-opsx REQ-0088-versioned-product-usage-docs
```
