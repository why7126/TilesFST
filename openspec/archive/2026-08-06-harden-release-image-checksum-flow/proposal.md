## 背景与原因

v0.3.2 发布确认中暴露出镜像公告输入变更后，旧 tar 包、旧 `.sha256` 和新 manifest 可能被人工混用，导致 `shasum -a 256 -c` 出现不一致。现有脚本能发现部分 input hash drift，但对 tarball/sidecar/manifest 三者一致性的强制校验不足，发布命令输出也没有足够突出最终可用 sha。

## 变更内容

- 加强 `validate-image-build.py validate-manifest`：强制校验 tarball 存在、sidecar 存在、sidecar sha 与 manifest sha 一致、实际 tarball sha 与 manifest sha 一致。
- 加强 `release-publish` 流程：发布确认前必须显式校验 manifest、tarball 和 `.sha256`，并在输出与 release evidence 中记录最终 sha。
- 优化 image/release 命令技能说明：公告或 release stable input 在 image build 后变更时，必须重新 image-prepare/image-build，不得沿用旧 sidecar。
- 补充测试覆盖 checksum drift，避免后续脚本回退。

## 能力影响

### 新增能力

- 无。

### 修改能力

- `deployment-image-build`: 镜像 manifest 校验必须验证离线包、sidecar 和 manifest sha256 三者一致；发布确认不得接受 stale manifest 或 checksum drift。

## 影响范围

- 影响文件：`scripts/validate-image-build.py`、`tests/test_release_validation.py`、`.agents/skills/image-build/SKILL.md`、`.agents/skills/release-publish/SKILL.md`、`rules/release.md`、`docs/08-production-image-release.md`。
- 不影响 API、数据库、Web UI、小程序或管理端业务逻辑。
- 不需要 Orval。
- 需要运行 `python -m pytest tests/test_release_validation.py`、`python scripts/validate-image-build.py validate-manifest --release v0.3.2`、`python scripts/validate-release.py --release-dir releases/v0.3.2 --stage publish`。
