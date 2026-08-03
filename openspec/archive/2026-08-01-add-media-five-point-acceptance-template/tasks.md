## 1. Template Documentation

- [x] 1.1 确认媒体五联验收模板长期落点，并在 design 或 implementation 中记录选择理由。
- [x] 1.2 新增或更新长期模板文档，包含 key、object、URL、thumbnail benefit、miniapp render 五联样例表。
- [x] 1.3 在模板文档中定义 `pass`、`fail`、`n/a`、`blocked` 状态、N/A 理由、blocked 重试条件和失败转 BUG 信息要求。
- [x] 1.4 在模板文档中加入媒体上传横切 gate：状态机、同会话即时回显、Docker Web `http://localhost:3000` 边界文件验收和失败信息位置。
- [x] 1.5 明确该模板不新增上传接口、缩略图生成、视频转码、对象存储架构、API、DB 或运行时 UI。

## 2. Traceability

- [x] 2.1 在 Change trace 中引用 REQ-0090、`docs/knowledge-base/best-practices/admin-media-upload-chain.md` 和 `docs/knowledge-base/retrospectives/sprint-016-retrospective.md`。
- [x] 2.2 在实现记录中说明后续 REQ、BUG、Sprint 和 Release 如何引用模板。
- [x] 2.3 若选择不放在 `docs/standards/`，在 trace 或 implementation 中说明替代位置符合目录边界。

## 3. Validation

- [x] 3.1 运行 `openspec validate add-media-five-point-acceptance-template --strict`。
- [x] 3.2 检查模板文档不包含真实客户数据、密钥、Authorization header、Cookie、`.env` 内容或本机绝对路径。
- [x] 3.3 确认无 API、DB、Orval、Web、小程序、管理端运行时和 Docker Compose 实现变更；若后续实现中出现变化，补充对应 docs/tests 并说明原因。
- [x] 3.4 在归档前确认 `media-acceptance-template` 正式 spec 已包含五联维度、失败记录、横切 gate 和引用方式。

## 验收返修记录

- [x] 2026-08-01 11:13:14 `/opsx-modify REQ-0090`：复核首次 apply 完整性；补充模板整体结论四态说明，并校准 Sprint 验收报告中的 REQ-0090 五联口径。
