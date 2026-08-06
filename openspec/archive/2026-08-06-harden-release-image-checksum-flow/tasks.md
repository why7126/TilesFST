## 1. 实现

- [x] 1.1 强化 `scripts/validate-image-build.py validate-manifest`，计算 tarball sha256 并与 manifest 和 `.sha256` sidecar 对比。
- [x] 1.2 补充 sidecar 缺失、sidecar 不匹配和 tarball 内容不匹配的定向测试。
- [x] 1.3 更新 image-build / release-publish 技能说明，展示最终 sha，并要求公告或稳定输入变更后重新运行。
- [x] 1.4 更新发布规则和生产镜像发布文档，说明最终 checksum 工作流。

## 2. 验证

- [x] 2.1 运行 `python -m pytest tests/test_release_validation.py`。
- [x] 2.2 运行 `python scripts/validate-image-build.py validate-manifest --release v0.3.2`。
- [x] 2.3 运行 `python scripts/validate-release.py --release-dir releases/v0.3.2 --stage publish`。
- [x] 2.4 运行 `openspec validate harden-release-image-checksum-flow --strict`。
