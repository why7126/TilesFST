---
created_at: 2026-08-05 14:39:06
updated_at: 2026-08-05 23:29:59
---

# 任务清单

- [x] 1. 盘点现有 `mintlify/`、`releases/v*/usage-docs/manifest.json` 和 `mintlify/site-manifest.json`，确认 latest 目标版本、页面清单、公告入口和截图资产引用。
- [x] 2. 优化 Mintlify 首页或等价开始入口，加入产品定位、角色入口、常用任务、当前版本和最近发布公告，且所有链接指向真实页面。
- [x] 3. 调整 Mintlify 主配置，使当前版本导航完整挂载 overview、admin、miniapp、public 和 faq 页面，并按“开始 / 当前版本 / 历史版本 / 发布公告”或等价结构组织。
- [x] 4. 为关键版本页面补充版本上下文，说明 `latest` 指向、固定版本语义、历史版本冻结和缺少 usage docs 时的不可用说明。
- [x] 5. 使用 Mintlify MDX 组件增强首页、FAQ 或聚合页表达，清理模板文案、空链接和参考项目无关内容。
- [x] 6. 更新 `mintlify/README.md` 或等价治理文档，记录 release 快照与站点投影关系、`latest` 更新、历史版本冻结、截图资产规则和敏感信息边界。
- [x] 7. 更新 `mintlify/site-manifest.json` 或等价文件，记录当前 latest、页面 hash 或一致性证据、人工覆盖和截图资产引用。
- [x] 8. 增加或更新 Mintlify 文档站校验，覆盖导航缺页、broken links、图片引用、`latest` 指针漂移、site manifest 漂移、`.DS_Store`、构建产物和公开安全。
- [x] 9. 运行文档站相关校验和 OpenSpec 语言校验，修复 blocker 并记录无法运行项。
- [x] 10. 同步 REQ trace、Change trace、长期文档或发布治理说明中的实现影响和验证结果。

## 验收返修记录

| 时间 | 反馈 | 调整 | 验证 |
|---|---|---|---|
| 2026-08-05 18:23:43 | Mintlify 配置需要显式使用主题，例如 `"theme": "mint"`。 | 临时在 `mintlify/mint.json` 中加入 theme；后续 18:40 返修已将 `mint.json` 废弃并迁移到 `docs.json` 唯一主配置。 | `python scripts/validate-mintlify-site.py`、`python scripts/validate-directory-structure.py`、`openspec validate improve-mintlify-docs-site --strict`、`python scripts/validate-openspec-language.py` |
| 2026-08-05 18:40:00 | 当前效果与预期差距仍大，需从扁平投影升级为参考 promptt / Dify Docs 的产品化文档站结构。 | 新增 `mintlify/docs.json` 作为唯一主配置，补站点 metadata、colors、favicon、tabs/groups 分层导航、角色入口、常用任务、版本索引、治理页；删除 `mintlify/mint.json`；生成器、站点校验、目录校验、release/usage docs 校验同步改为 docs.json。 | `python scripts/validate-mintlify-site.py`、`python scripts/validate-directory-structure.py`、`python scripts/validate-usage-docs.py --release-dir releases/v0.3.4`、`python scripts/validate-usage-docs.py --release-dir releases/v0.3.3`、`mintlify broken-links`；`python -m pytest tests/test_release_validation.py tests/test_validate_directory_structure.py` 为 34/38 通过，剩余失败来自测试 fixture 仍使用 release-local screenshots 和 docker compose 服务名 `docs-site` 旧假设 |
| 2026-08-05 23:29:59 | 需要构建本地可复用 docs-site 镜像，预装 Mintlify CLI，避免 `mintlify dev` 污染宿主机 `~/.mintlify*`。 | 新增 `deploy/docs-site/Dockerfile` 预装 `mintlify@4.2.45`；根、local、prod Compose 改为 build/image 方式启动 `mintlify dev --host 0.0.0.0 --port 3000`；Mintlify cache 改用 Docker named volume；删除旧静态目录服务器；同步 env 示例、部署文档和目录校验。 | `docker compose --profile docs-site config --quiet`、local/prod Compose config、`python scripts/validate-directory-structure.py`、`python scripts/validate-mintlify-site.py`、`python -m pytest tests/test_validate_directory_structure.py`；实际 `docker compose --profile docs-site build tilesfst-docs-site` 两次均卡在 `npm install -g mintlify@4.2.45`，已中断，需网络/registry 正常后重跑 |
