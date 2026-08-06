---
change_id: improve-mintlify-docs-site
status: applied
change_type: update
created_at: 2026-08-05 14:39:06
updated_at: 2026-08-05 23:29:59
source_requirement: REQ-0100-mintlify-docs-site-ia-content-experience
expected_sprint: null
---

# Change 追踪

## 基本信息

```yaml
change_id: improve-mintlify-docs-site
status: applied
change_type: update
source_requirement: REQ-0100-mintlify-docs-site-ia-content-experience
capabilities:
  modified:
    - product-release-management
impact:
  backend: false
  web: false
  miniapp: false
  admin: false
  database: false
  storage: false
  api: false
  docs_site: true
  release_governance: true
openspec_artifacts:
  - proposal.md
  - design.md
  - specs/product-release-management/spec.md
  - tasks.md
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-017-retrospective.md
  - docs/knowledge-base/retrospectives/sprint-018-retrospective.md
  - docs/knowledge-base/retrospectives/sprint-019-retrospective.md
prototype_refs:
  - issues/requirements/archive/REQ-0100-mintlify-docs-site-ia-content-experience/prototype/web/context.md
  - issues/requirements/archive/REQ-0100-mintlify-docs-site-ia-content-experience/prototype/web/index-wireframe.html
```

## 冲突处理记录

| 输入 | 优先级 | 处理 |
|---|---|---|
| `prototype/web/index-wireframe.html` | 最高 | 作为 Mintlify 首页信息架构线框，不转换为 `src/web` 应用源码。 |
| `prototype/web/context.md` | 高 | 作为角色入口、导航结构和内容约束来源。 |
| `acceptance.md` | 中 | 约束链接、版本上下文、参考项目裁剪、公开安全和事实源边界。 |
| `rules/ui-design.md` | 中 | 仅用于品牌和内容气质参考，不触发 Web DS 实现。 |
| `openspec/specs/product-release-management/spec.md` | 基线 | 通过 MODIFIED requirements 扩展 Mintlify 导航、站点门禁和目录治理。 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-05 23:29:59 | `/opsx-modify` | 验收返修：新增本地可复用 docs-site 镜像，预装 Mintlify CLI；Compose 使用 Dockerfile build 和 named volume 缓存运行时 Mintlify client，删除旧静态目录服务器，避免宿主机 `~/.mintlify*` 权限污染 |
| 2026-08-05 18:40:00 | `/opsx-modify` | 验收返修：从 `mint.json` 扁平导航升级到 `docs.json` 产品化文档站结构，新增角色/任务/版本/治理入口、站点 metadata、colors、favicon，并通过 Mintlify broken-links 与静态校验；不照搬参考项目品牌与外部内容 |
| 2026-08-05 18:23:43 | `/opsx-modify` | 验收返修：Mintlify 配置显式加入 `"theme": "mint"`，生成器保持同样输出，站点校验新增主题必检；不影响 API、DB、Web、小程序或管理端业务逻辑 |
| 2026-08-05 18:14:27 | `/opsx-apply` | 实施 Mintlify 首页、导航、版本上下文、site manifest、生成器导航模板与专项站点校验；验证通过 `validate-mintlify-site.py`、`validate-directory-structure.py`、`validate-usage-docs.py --release-dir releases/v0.3.4` |
| 2026-08-05 14:39:06 | `/req-opsx` | 从 REQ-0100 创建 OpenSpec Change，并生成 proposal/design/spec/tasks/trace |
