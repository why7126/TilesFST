## Context

生产镜像包构建目前主要记录在 `docs/08-production-image-release.md`，操作人员需要手动执行后端构建、Web 构建、镜像验证、`docker save`、压缩和 sha256 生成等命令。项目已有 `scripts/docker-up.sh`、`scripts/docker-down.sh` 作为 Docker Compose 启停入口，因此镜像构建脚本和同级 env 示例应放入 `scripts/`，并通过独立 env 文件管理交付参数。

## Goals / Non-Goals

**Goals:**

- 提供一个可重复执行的 shell 脚本，完成后端镜像、Web 镜像构建。
- 通过 env 文件配置版本、平台、镜像名、builder、导出目录与是否导出离线包。
- 构建后执行基础验证：镜像架构检查、后端依赖导入检查、Web Nginx 配置检查。
- 支持导出包含后端和 Web 镜像的 gzip 离线包，并生成 sha256 校验文件。

**Non-Goals:**

- 不改变 Dockerfile、Compose 服务拓扑或运行时容器环境变量。
- 不引入 CI/CD、远程推送、镜像仓库登录或生产服务器部署自动化。
- 不修改 API、数据库、权限、MinIO 访问策略或前端业务功能。

## Decisions

1. 构建脚本放在 `scripts/build-images.sh`。
   - 原因：符合 `rules/directory-structure.md` 中 Docker 启停和自动化脚本归属 `scripts/` 的规则。
   - 备选：放到项目根目录。缺点是会增加根目录入口噪音，不符合脚本归属边界。

2. env 示例放在 `scripts/build-images.env.example`。
   - 原因：该配置是镜像构建脚本的同级参数示例，比藏在 `scripts/docker/` 更容易发现，同时不会混入运行时 `.env.example` 或新增根目录文件。
   - 备选：放入 `scripts/docker/build-images.env.example`。缺点是配置文件像脚本文档，入口不够直观。

3. 脚本默认读取 `scripts/build-images.env`，也允许通过第一个参数传入自定义 env 文件。
   - 原因：便于本地复制示例后长期复用，也便于一次性指定不同版本的构建参数。
   - 备选：只支持命令行参数。缺点是命令会再次变长，无法达到“sh 脚本 + env”的目标。

4. 默认使用 `docker buildx build --load`，平台默认 `linux/amd64`。
   - 原因：与现有生产镜像包文档一致，构建结果进入本地 Docker image store，后续可直接验证和 `docker save`。
   - 备选：使用普通 `docker build`。缺点是跨架构参数与现有文档不一致。

## Risks / Trade-offs

- [Risk] 构建机没有可用 buildx builder → 脚本先检查 `docker buildx version`，并在 `IMAGE_BUILD_CREATE_BUILDER=true` 时创建/启用 builder。
- [Risk] env 文件中版本或输出目录写错导致交付包命名不一致 → 脚本集中打印配置摘要，并按变量统一生成 tar 与 sha256 文件名。
- [Risk] 构建成功但镜像不可运行 → 脚本在构建后执行后端依赖导入和 Nginx 配置检查。
- [Risk] 离线包较大，不应进入 Git → 文档继续要求输出目录放在项目目录外，脚本默认输出到项目外相邻 `releases/` 路径。

## Migration Plan

1. 复制 `scripts/build-images.env.example` 为 `scripts/build-images.env` 或任意自定义 env 文件。
2. 修改版本、平台和输出目录。
3. 执行 `./scripts/build-images.sh` 或 `./scripts/build-images.sh <env-file>`。
4. 旧的手工 `docker buildx` 命令仍可作为排障参考保留在部署文档中。
