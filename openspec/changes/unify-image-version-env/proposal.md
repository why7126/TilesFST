## 背景与原因

生产镜像构建与部署示例中同一个版本号需要在多个变量里重复填写，容易出现 backend、web、离线包目录和 tar 包名版本不一致。需要将常规发版路径收敛为只输入一次版本 tag，其余镜像引用与交付包路径自动推导。

## 变更内容

- 生产 Compose 使用统一 `TILESFST_IMAGE_TAG` 生成 backend/web 镜像 tag。
- 保留 backend/web 镜像仓库名变量，支持私有仓库或镜像命名差异，但常规改版本无需修改仓库名。
- 构建镜像 env 示例只要求填写 `IMAGE_BUILD_TAG`，离线输出目录与 tar 包名默认由脚本推导。
- 同步 `.env.example`、部署文档和生产镜像交付手册中的变量说明。

## 能力影响

### 新增能力

- 无。

### 修改能力

- `deployment-image-build`: 构建配置示例必须体现 release dir 与 tar name 可由 `IMAGE_BUILD_TAG` 推导，常规发版只需填写一次版本 tag。
- `deployment`: 生产 Compose 镜像变量必须支持 backend/web 默认共用一个统一镜像 tag。

## 影响范围

- 影响文件：`.env.example`、`scripts/build-images.env.example`、`docker-compose.prod.yml`、`docker-compose.prod.external.yml`、`docs/02-deployment.md`、`docs/08-production-image-release.md`。
- 不影响 API、数据库、对象存储接口、Web UI、小程序或管理端业务逻辑。
- 不需要 Orval。
- 需要执行脚本语法检查与 Docker Compose 配置渲染校验。
