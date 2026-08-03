## 1. 目录与规则治理

- [x] 1.1 更新 `AGENTS.md`，加入 `mintlify/` 文档站源目录、release 快照和 Docker Compose 文档站服务边界。
- [x] 1.2 更新 `rules/directory-structure.md`，允许并说明 `mintlify/` 顶层目录、站点资产、构建产物禁止提交边界。
- [x] 1.3 更新 `rules/document-governance.md`，区分 `releases/<version>/usage-docs/` 快照与 `mintlify/` 站点投影源。
- [x] 1.4 更新 `rules/release.md`，加入 Mintlify 站点源目录、共享截图资产、站点投影校验和发布门禁。
- [x] 1.5 更新 `rules/environment.md` 与 `rules/port-management.md`，说明 Mintlify Compose 服务变量和端口策略。

## 2. Mintlify 站点目录与同步

- [x] 2.1 创建受治理的 `mintlify/` 基础结构、站点配置和公开资产目录，不提交构建产物。
- [x] 2.2 实现或扩展 release usage docs 到 `mintlify/docs/<version>/` 的同步 / 投影脚本。
- [x] 2.3 实现 `latest` 指针和无 usage docs 历史版本的公告 / 不可用说明生成规则。
- [x] 2.4 将发布公告投影到 `mintlify/releases/<version>/` 或等价站点路径。

## 3. 共享截图资产与 Manifest

- [x] 3.1 扩展 `usage-docs/manifest.json` schema，记录站点目标路径、截图引用、hash、来源、覆盖和同步状态。
- [x] 3.2 将系统截图写入或迁移到 `mintlify/assets/screenshots/`，按内容 hash 去重。
- [x] 3.3 实现截图复用记录，包括 `first_used_in`、`used_by_versions`、`covered_pages`、`source_type` 和 `reuse_reason`。
- [x] 3.4 更新已有 usage docs 模板和生成逻辑，默认不在 release usage docs 目录内复制大体积截图。

## 4. Docker Compose 文档站服务

- [x] 4.1 为本地 / 演示 Docker Compose 增加 `docs-site` 或等价 profile 的 Mintlify 文档站服务。
- [x] 4.2 在 `.env.example` 中新增 `HOST_PORT_MINTLIFY_DOCS` 或等价端口变量，并补充安全注释。
- [x] 4.3 按场景决定生产 Compose 是否包含文档站服务或仅记录外部托管替代方案。
- [x] 4.4 更新 `docs/02-deployment.md`，说明 Compose profile 启动、外部托管、反向代理和发布证据边界。

## 5. 校验与测试

- [x] 5.1 扩展 `scripts/validate-directory-structure.py`，校验 `mintlify/` 目录边界和禁止提交构建产物 / 敏感文件。
- [x] 5.2 扩展 usage docs 校验，检查 release 快照、站点投影、Mintlify 导航、broken links、截图 hash 和复用依据。
- [x] 5.3 扩展 release 校验，覆盖站点目录状态、生产承载方式、Compose 文档站服务和 publish gate。
- [x] 5.4 增加 pytest 覆盖目录结构、manifest、截图复用、公开安全、Compose profile 和 release gate。
- [x] 5.5 运行目录结构、OpenSpec、usage docs、release、Docker Compose config 和相关 pytest 校验。

## 6. 收尾与追溯

- [x] 6.1 更新 `releases/README.md` 和 usage docs 相关 Skill，说明 `releases/` 与 `mintlify/` 的职责边界。
- [x] 6.2 更新 Change trace、REQ trace、AI usage hook 和验证证据摘要。
- [x] 6.3 若变更进入发布范围，按发布规范执行 `/image-prepare`、`/image-build` 或记录不适用原因。

## 验收返修记录

| 时间 | 反馈 | 调整 | 验证 |
|---|---|---|---|
| 2026-08-03 19:40:00 | 已有历史 usage docs 未迁移到 `mintlify/` 站点目录。 | 新增 `scripts/generate-usage-docs.py --project-existing <version>`，可在不重生成 release 快照的前提下将既有 `releases/<version>/usage-docs/` 投影到 `mintlify/docs/<version>/`、`mintlify/docs/latest/`、`mintlify/releases/<version>/` 和 `mintlify/assets/screenshots/`；已迁移 `v0.3.3`。 | `python scripts/generate-usage-docs.py v0.3.3 --project-existing`；`python scripts/validate-usage-docs.py --release-dir releases/v0.3.3`；pytest 覆盖历史迁移。 |
