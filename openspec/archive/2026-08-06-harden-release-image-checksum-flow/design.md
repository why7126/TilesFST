## 背景

`/image-build` 当前会导出离线 tar 包和 `.sha256`，并把 sidecar 中的 sha 写入 `image-manifest.json`。但 `validate-manifest` 只校验 manifest 结构、plan/input hash 和 manifest 与 plan 的 input_hashes，未重新计算 tarball sha，也未检查 sidecar 与 manifest 是否一致。发布过程中如果公告或 release stable input 在 image build 后被修改，再重建或替换了部分产物，人工可能拿到不匹配的 tar/sidecar 组合。

## Decisions

- D1：`validate-manifest` 必须把 tarball 作为真实发布产物复核，而不是只信任 manifest 中的 `exists` 和 `sha256` 字段。
- D2：校验顺序为：plan 未漂移 → manifest 结构合法 → manifest input_hashes 等于 plan input_hashes → tarball 路径存在 → sidecar 路径存在 → sidecar sha 等于 manifest sha → 实际 tarball sha 等于 manifest sha。
- D3：错误信息使用明确分类文本，如 `tarball sha256 mismatch`、`tarball sidecar sha256 mismatch`、`tarball missing`，便于 release-publish 输出 blocker。
- D4：发布命令与发布规范明确：公告或 release stable input 在 image build 后发生任何变更，必须重新执行 `/image-prepare` 与 `/image-build`，并以最新 manifest sha 为唯一发布 sha。
- D5：不把仓库外 tar 包提交到 Git；仅在仓库内 manifest 记录相对路径和 sha。

## 风险

- 重新计算 164MB 左右 tarball sha 会增加少量时间，但相对镜像构建成本可接受。
- 旧版本发布对象若 tarball 已被清理，publish 阶段会失败；这是正确阻断，需补外部构建证据或重建镜像。

## 验证

- 增加单元测试覆盖 sidecar 缺失、sidecar 与 manifest 不一致、实际 tarball 与 manifest 不一致。
- 用 v0.3.2 当前 manifest 执行 `validate-manifest`，确认真实产物通过。
