---
created_at: 2026-09-10 10:52:33
updated_at: 2026-09-10 10:56:24
---

# Apply持续执行行为验收

来源：BUG-0149-opsx-apply-premature-stop，Change为fix-apply-continuous-execution-behavior，Sprint为sprint-030。

共享执行契约和两个apply入口增加结束前逐项核对、集中人工问题、四维进度与两次同类失败切换；同步AGENTS、上下文规则和静态校验。新增真实Agent场景采集器、行为证据重放校验器及正反测试。

48项单测与两个入口共14次实际受控运行通过，分别覆盖首次失败自主修复、单项阻塞继续、问进度继续、合法暂停、明确停止、有限重试与压缩恢复。证据与失败重跑记录位于issues/bugs/archive/BUG-0149-opsx-apply-premature-stop/logs/behavior/；方法和证明边界见openspec/archive/2026-09-10-fix-apply-continuous-execution-behavior/behavior-evidence.md。

初始权限问题通过自动授权审查解决；采集器输入和并发通知问题已修复后重跑。单次受控运行不保证所有未来业务会话，夹具测试不冒充真实运行。历史REQ-0137运行因果仍未确认。

仅治理资产，无业务API、数据库、Orval或Compose影响。OpenSpec、语言、目录、上下文预算、Sprint范围及观测N/A验证在Change收尾核对；人工归档独立执行，无自动follow-up。
