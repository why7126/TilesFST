---
requirement_id: REQ-0036-clipboard-helper-best-practice-docs
title: Clipboard helper best-practice 文档验收标准
status: done
created_at: 2026-07-11 23:47:07
updated_at: 2026-07-12 00:32:47
---

# Acceptance Criteria

## 功能 AC

- [x] AC-001 文档落位：新增或更新一份长期维护的 Clipboard helper best-practice 文档，位置符合 `docs/`、知识库或 Web 前端说明的目录职责。
- [x] AC-002 入口可发现：文档应从 `docs/knowledge-base/README.md`、`src/web/README.md` 或等价索引建立可发现入口，避免只停留在 issue 文档内。
- [x] AC-003 适用范围：文档开头必须说明其适用于 Web 管理端 Clipboard helper 调用方，不替代 `REQ-0032` 的 helper 实现要求。
- [x] AC-004 文案映射：文档必须覆盖 `success`、`failed`、`unavailable`、`empty` 四类结果的调用方文案原则。
- [x] AC-005 业务语义：文档必须要求成功/失败提示保留业务对象名称，例如 `request_id`、随机密码、版本号，不得全部写成无差别的“复制成功/复制失败”。
- [x] AC-006 fallback 策略：文档必须说明自动复制失败和 Clipboard API 不可用时的手动复制、文本选中、禁用入口或明确提示策略。
- [x] AC-007 空值策略：文档必须说明空值场景优先隐藏或禁用复制入口，或展示“当前内容为空，无法复制”类提示。
- [x] AC-008 敏感值分类：文档必须定义允许复制、谨慎复制、禁止或默认不复制三类数据，并给出典型示例。
- [x] AC-009 禁止复制边界：AccessKey、SecretKey、Token、Cookie、Authorization、客户隐私原文等必须被列为禁止或默认不复制类别，除非后续有专门安全流程。
- [x] AC-010 原文记录限制：文档必须要求 helper 和调用方不得把复制内容写入日志、埋点 payload、测试快照、控制台输出或错误消息。
- [x] AC-011 权限边界：文档必须要求复制入口只能复制用户已授权查看的内容，不得通过 helper 绕过权限边界。
- [x] AC-012 调用方 checklist：文档必须提供代码评审 / QA checklist，覆盖授权可见、敏感值分类、结果文案、fallback、空值、日志/埋点和测试覆盖。
- [x] AC-013 示例与反例：文档应提供推荐示例和反例，且示例必须使用脱敏或虚构值，不得引入真实密钥、真实客户数据或真实生产 URL。
- [x] AC-014 知识库追溯：文档或 trace 应引用 Sprint 006 复盘中 `best-practices/clipboard-fallback.md` 建议后续新建的行动项。

## 非功能 AC

- [x] AC-015 范围控制：本需求实现不得新增后端 API、数据库字段、OpenAPI / Orval 生成物、小程序复制适配或 Docker Compose 配置。
- [x] AC-016 安全性：文档不得包含真实密钥、真实 Token、真实客户隐私数据、真实生产签名 URL 或可复用敏感凭据。
- [x] AC-017 可维护性：文档应明确 owner / update_method / created_at / updated_at 等长期文档元数据，符合文档治理要求。
- [x] AC-018 可测试性：OpenSpec 阶段应将文档 checklist 转化为可验收任务，避免仅写原则而无法验证。
- [x] AC-019 一致性：`requirement.md`、`user-stories.md`、`business-flow.md`、`acceptance.md` 与 `trace.md` 状态已由 Workflow Sync 保持 `in_sprint` 一致。

## 横切 AC（knowledge-base）

本 REQ 判定为文档治理需求，不涉及管理端 CRUD 列表页、表单页、弹窗新建/编辑或媒体上传链路，因此无 `admin-list`、`admin-form`、`admin-modal`、`media-upload` 横切 AC。

Knowledge-base 参考：

- `docs/knowledge-base/README.md`：确认 best-practices 目录职责。
- `docs/knowledge-base/retrospectives/sprint-006-retrospective.md`：Sprint 006 行动项建议后续新建 Clipboard fallback / best-practice 文档。
