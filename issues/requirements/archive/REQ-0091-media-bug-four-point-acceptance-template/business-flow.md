---
requirement_id: REQ-0091-media-bug-four-point-acceptance-template
title: 媒体类 BUG 四联验收模板 - 业务流程
status: done
created_at: 2026-08-01 09:55:10
updated_at: 2026-08-01 11:14:55
---

# 业务流程

## 1. 主流程

```text
媒体类 BUG 修复完成
  ↓
确认原 BUG 场景
  ├─ BUG 编号 / 严重等级 / 影响范围
  ├─ 复现入口 / 受影响端 / 环境
  └─ 修复前实际结果 / 修复后期望结果
  ↓
执行四联验收
  ├─ key：业务记录中的媒体 key 稳定、合规、可追溯
  ├─ object：对象存储真实 object 存在，类型/大小/权限正确
  ├─ URL：接口、Web 或小程序使用的 URL 可访问且失败态可诊断
  └─ render：受影响端正确渲染媒体、占位和失败态
  ↓
记录证据
  ├─ pass：记录关键证据
  ├─ fail：记录实际/期望、复现步骤、影响范围
  ├─ n/a：记录不适用原因
  └─ blocked：记录阻塞原因和下一步
  ↓
形成结论
  ├─ 全部 pass / n/a 有理由 → 可进入评审或发布检查
  ├─ 任一 fail → 回到修复或返修
  └─ 任一 blocked → 补环境、补资源或补 evidence 后重验
```

## 2. 参与角色

| 角色 | 输入 | 输出 |
|---|---|---|
| 产品负责人 | 原 BUG 背景、用户影响、期望结果 | 修复闭环判断、发布风险判断 |
| 测试人员 | 复现步骤、测试环境、媒体样例 | 四联验收记录、截图/日志证据、失败项 |
| 后端 / 平台开发 | object key、对象存储、URL 策略、日志 | key/object/URL 修复说明与排查线索 |
| 前端 / 小程序开发 | 页面入口、组件状态、失败态 | render 证据、端侧兼容说明 |
| 发布负责人 | Sprint / Release 范围、环境状态 | 发布前媒体 BUG 风险确认 |

## 3. 与通用媒体五联模板的差异

| 对比项 | 媒体五联验收模板 | 媒体类 BUG 四联验收模板 |
|---|---|---|
| 使用场景 | 媒体能力交付、回归、发布检查 | 媒体类 BUG 修复、返修、回归 |
| 核心维度 | key、object、URL、thumbnail benefit、miniapp render | key、object、URL、render |
| 关注重点 | 能力完整性和体验收益 | 原 BUG 是否复现、修复是否闭环、证据是否充分 |
| 缩略图 | 独立验证 thumbnail benefit | 如原 BUG 涉及缩略图，则纳入 object / URL / render 证据 |
| 端侧渲染 | 小程序独立维度 | render 可覆盖 Web 管理端、店主 Web、小程序和接口返回 |

## 4. 异常流程

| 异常 | 处理 |
|---|---|
| 缺少测试对象或媒体样例 | 标记 `blocked`，记录缺少的资源、负责人和补齐方式。 |
| 对象存储环境不可用 | 标记 `blocked`，记录 MinIO / 代理 / 域名状态，不将未验证写作通过。 |
| URL 访问失败但 object 存在 | 标记 `fail`，记录 HTTP 状态、业务错误码、签名策略和用户可见表现。 |
| 小程序真机不可验 | 标记 `blocked` 或 `n/a`，必须说明 DevTools、体验版、真机 evidence 的替代或缺失原因。 |
| 仅 UI 展示正常但 key/object 未验证 | 不得判定通过，必须补 key 和 object 证据。 |

## 5. 后续落点建议

- `/req-complete`：在本需求 `acceptance.md` 固化四联验收清单。
- `/req-opsx`：明确模板最终沉淀位置，优先考虑 `rules/media.md`、`rules/object-storage.md`、`docs/standards` 或 BUG acceptance 模板。
- Sprint / Release：若媒体类 BUG 进入迭代或发布范围，验收报告应引用该模板或其落地文档。
