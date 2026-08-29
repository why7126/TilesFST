---
review_id: REV-REQ-0125-001
requirement_id: REQ-0125-miniapp-certificate-detail-home-floating-button
date: 2026-08-25 22:43:55
participants:
  - product
result: approved
created_at: 2026-08-25 22:43:55
updated_at: 2026-08-25 22:43:55
---

# 需求评审

## 评审结论

通过。

`REQ-0125` 范围清晰：仅在小程序证书详情页补齐【返回首页】悬浮按钮，复用既有 `home-floating-button`，默认使用 `offset="list"`，不扩展其他页面、不修改组件契约、不涉及 API / DB / 对象存储 / Web / 管理端。

## 评审清单

- [x] 范围清晰，Out of Scope 明确。
- [x] 验收标准可测试，已覆盖正常态、错误态、分享直达、重复点击、截图矩阵和静态检查。
- [x] 优先级与依赖合理，P2，父需求为 `REQ-0085-miniapp-global-home-floating-button`。
- [x] UI 类实现策略已决，复用 `home-floating-button offset="list"`，不新增独立原型视觉稿。
- [x] 无与现有 REQ 重复未说明；本需求是对证书详情页缺口的局部补齐。

## 条件通过项

- [ ] 实现阶段必须保持 `offset="list"` 与其他深层内容页一致；如发现固定底部操作区冲突，需在 OpenSpec design 中说明原因和仍使用既有 offset 枚举的策略。
- [ ] 实现阶段必须补充或更新小程序静态检查，覆盖 `index.json` 组件声明、`index.wxml` 挂载和 `.ts` / `.js` 同步。
- [ ] 验收阶段必须按 `AC-NAV-*` 记录 DevTools 320 / 375 / 430 pt evidence；真机不可用时标记 `blocked` 或 `follow_up`。

## 后续建议

评审通过后，先纳入 Sprint，再创建 OpenSpec Change：

```text
/sprint-propose sprint-xxx --req REQ-0125-miniapp-certificate-detail-home-floating-button
/req-opsx REQ-0125-miniapp-certificate-detail-home-floating-button
```
