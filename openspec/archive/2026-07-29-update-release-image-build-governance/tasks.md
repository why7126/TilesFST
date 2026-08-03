## 1. 发布与镜像契约

- [x] 1.1 扩展 `releases/templates/release.json`，加入 `image_required`、`image_prepare`、`image_build`、image plan / manifest 引用和 blocker 字段。
- [x] 1.2 扩展 `scripts/validate-release.py`，校验 image gates、plan/manifest 引用、版本/tag 一致性、敏感信息和 manifest 过期。
- [x] 1.3 更新 `rules/release.md`，明确镜像准备、镜像构建、外部构建证据和发布确认阻断规则。

## 2. Image Prepare

- [x] 2.1 新增 `.agents/skills/image-prepare/SKILL.md`，定义输入、Must Read、门禁、输出和 AI usage hook。
- [x] 2.2 新增或扩展镜像输入校验脚本，生成 `releases/<version>/image-build-plan.json`。
- [x] 2.3 校验 `PRODUCT_VERSION`、`TILESFST_IMAGE_TAG`、`IMAGE_BUILD_TAG`、Compose image 引用和构建 env 示例的一致性。
- [x] 2.4 将 Dockerfile、Compose、构建脚本、构建 env 示例、Nginx 配置、schema 和 migration 纳入 input hash。

## 3. Image Build

- [x] 3.1 新增 `.agents/skills/image-build/SKILL.md`，定义必须读取 image build plan、禁止猜测构建输入和失败分类。
- [x] 3.2 复用或封装 `scripts/build-images.sh`，执行 backend/web 镜像构建、平台验证、后端依赖验证、Web Nginx 验证、tar 导出和 sha256 生成。
- [x] 3.3 生成 `releases/<version>/image-manifest.json`，记录镜像、平台、tarball、sha256、input hash、validation 和 source plan。
- [x] 3.4 Docker、buildx、网络、基础镜像源或校验失败时记录 blocker，不写成功 manifest。

## 4. Release 命令集成

- [x] 4.1 更新 `.agents/skills/release-prepare/SKILL.md`，在 `image_required=true` 时要求 image prepare 证据，并避免默认执行真实镜像构建。
- [x] 4.2 更新 `.agents/skills/release-publish/SKILL.md`，校验 image manifest 或受控外部构建证据。
- [x] 4.3 更新 AI usage hook 或调用约定，使 `image.prepare`、`image.build` 可归因到 release version。
- [x] 4.4 更新成功路径输出，保持 release/image 命令只输出 compact summary。

## 5. 文档与测试

- [x] 5.1 更新 `docs/08-production-image-release.md` 和部署文档，说明 `/image-prepare`、`/image-build`、plan、manifest 与五命令依赖关系。
- [x] 5.2 补充 release validator、image plan validator、image manifest validator 的单元或集成测试。
- [x] 5.3 补充敏感信息扫描、hash 漂移、版本/tag 不一致、缺失 Docker 环境 blocker 的测试。
- [x] 5.4 运行相关 pytest、OpenSpec validate、发布校验脚本和 Docker Compose config 静态校验。
