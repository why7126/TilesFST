---
requirement_id: REQ-0052-miniapp-device-evidence-template
title: 小程序 DevTools/真机验收 evidence 模板业务流程
status: done
created_at: 2026-07-19 17:08:59
updated_at: 2026-07-19 19:05:20
---

# REQ-0052 小程序 DevTools/真机验收 evidence 模板业务流程

## 1. evidence 判定流程

```text
小程序 REQ / BUG / Change 进入实现或验收
  |
  v
是否影响小程序页面渲染、导航、安全区、触控或真实运行入口？
  |
  +-- 否：miniapp_device_evidence 标记 not_applicable
  |       |
  |       +-- 写明 N/A reason
  |
  +-- 是：识别设备验收范围
          |
          +-- 静态测试 / 脚本测试 evidence
          |     |
          |     +-- 记录命令摘要，但不等同 DevTools/真机通过
          |
          +-- DevTools evidence
          |     |
          |     +-- 记录工具版本、基础库、页面路径、视口、截图和结论
          |
          +-- 真机 evidence
                |
                +-- 记录机型、系统、微信版本、安全区、截图/录屏和结论
```

## 2. 设备验收状态流

```text
required
  |
  +-- 执行通过 --> passed
  |
  +-- 执行失败 --> failed
  |                 |
  |                 +-- 形成修复或 follow-up
  |
  +-- 暂无法执行 --> blocked
  |
  +-- 不适用 ------> not_applicable
  |
  +-- 可发布但保留 --> follow_up
```

## 3. evidence 记录结构

| 层级 | 记录重点 | 示例 |
|---|---|---|
| 自动化 / 静态测试 | 命令、结果摘要、覆盖边界 | `tests/test_miniapp_static.py` 通过，但不证明真机安全区 |
| DevTools | 工具版本、基础库、模拟器设备、页面路径、视口、截图 | 375 pt 下首页首屏不被导航遮挡 |
| 真机 | 机型、系统、微信版本、基础库、安全区、触控、截图/录屏 | iPhone 真机胶囊避让通过 |
| N/A | 不适用原因 | 仅新增模板文档，不改小程序运行时代码 |
| follow-up | 剩余风险、责任人、后续承接 | 已 DevTools 通过，缺 Android 真机 |

## 4. 与相关 REQ 差异

| 对比项 | REQ-0039 XL 管理端页面分层验收模板 | REQ-0052 小程序设备 evidence 模板 |
|---|---|---|
| 端 | Web 管理端 | 微信小程序 |
| 关注对象 | DB/API/上传/Orval/Web/Docker/横切 UI gate | DevTools、真机、设备环境、截图/录屏和人工 follow-up |
| 证据边界 | 命令、接口、截图、Docker 和 UI gate 摘要 | 自动化、DevTools、真机必须分层，不可互相替代 |
| 沉淀位置 | `docs/standards/xl-admin-page-acceptance-template.md` | 建议 `docs/standards/miniapp-device-evidence-template.md` |
| 是否回填历史 | 不处理历史页面 | 允许引用 sprint-008 残留作为案例，但不强制回填 |

## 5. 典型引用位置

| 位置 | 引用方式 |
|---|---|
| REQ `acceptance.md` | 在测试与验证 AC 中要求后续引用 `miniapp_device_evidence`。 |
| OpenSpec `tasks.md` | 将 DevTools / 真机 evidence 作为人工验收任务。 |
| Change `trace.md` / `acceptance.md` | 记录每条 evidence 状态、结论和剩余风险。 |
| Sprint `acceptance-report.md` | 汇总哪些设备验收通过，哪些为 follow-up。 |
| Release note | 只记录用户可理解的设备验收结论和剩余风险，不复制完整证据。 |

## 6. 风险控制

| 风险 | 控制方式 |
|---|---|
| 静态测试被误写为真机通过 | evidence 来源分层，未记录真机时不得写“真机通过”。 |
| 设备证据散落在 tasks / acceptance / report | 建议以 `docs/standards/miniapp-device-evidence-template.md` 为事实源，各处引用摘要。 |
| 截图含敏感信息 | 截图路径仅用仓库相对路径；含敏感信息时脱敏或记录不可公开原因。 |
| 强制关闭遗漏 follow-up | `follow_up` 状态必须写剩余风险和后续承接方式。 |
| 设备矩阵无限扩大 | 本模板定义记录结构，不强制覆盖所有机型；具体 Change 按风险选择设备和视口。 |
