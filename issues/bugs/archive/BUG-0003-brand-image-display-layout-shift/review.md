---
bug_id: BUG-0003-brand-image-display-layout-shift
review_id: REV-BUG-0003-001
status: approved
reviewed_at: 2026-06-25 22:19:51
reviewer: ai-agent
decision: approve
severity: high
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0003-brand-image-display-layout-shift` 评审通过，状态变更为 `approved`。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0003-brand-image-display-layout-shift
```

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | `root-cause.md` 已定位到 `/media/{object_key}` 未挂载可访问媒体服务，以及 `admin-notice` 条件插入文档流导致布局位移。 |
| 严重等级合理 | 通过 | 品牌 Logo 是品牌主数据关键展示字段，上传后列表和编辑弹窗均不可见；状态提示影响连续操作体验，`high` 合理。 |
| 回归验收明确 | 通过 | `acceptance.md` 已覆盖上传后可访问 URL、列表展示、编辑回显、提示不引发布局波动、媒体安全、既有功能回归和测试要求。 |
| 是否需 hotfix 路径 | 不需要 | 当前缺陷影响管理端体验和素材确认，但未明确阻断品牌文本维护、状态变更或核心接口调用，不定为 blocker/critical。 |

## 3. 批准理由

1. 缺陷影响品牌管理核心流程中的图片上传确认、列表展示和编辑回显。
2. 根因具备明确代码线索，修复范围可被 OpenSpec `fix-*` Change 承载。
3. 验收标准覆盖用户可见结果、媒体访问安全和页面布局稳定性。
4. 临时规避不能真正解决媒体可访问性问题，因此不建议 defer 或 wont-fix。

## 4. 后续要求

1. 创建 `fix-*` OpenSpec Change 时，必须覆盖后端媒体访问策略和前端提示布局策略。
2. 若修复涉及 API 响应结构变化，必须同步 OpenAPI、Orval 和 API 文档。
3. 若修复涉及 MinIO 或 `/media` 代理，必须遵守 `rules/security.md`、`rules/media.md` 与 `rules/object-storage.md`。
4. 修复阶段必须补充或更新测试，至少覆盖品牌 Logo 展示/回显和 Tips 不推挤页面主体。
