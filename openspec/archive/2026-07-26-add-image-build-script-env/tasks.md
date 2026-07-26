## 1. 脚本与配置

- [x] 1.1 新增 `scripts/build-images.sh`，支持读取默认或指定 env 文件并构建后端/Web 镜像
- [x] 1.2 新增 `scripts/build-images.env.example`，提供构建参数示例和注释
- [x] 1.3 为脚本补充构建后镜像平台、后端依赖和 Web Nginx 配置验证
- [x] 1.4 为脚本补充可选离线镜像包导出和 sha256 校验文件生成

## 2. 文档与校验

- [x] 2.1 更新 `docs/02-deployment.md`，说明脚本化镜像构建入口
- [x] 2.2 更新 `docs/08-production-image-release.md`，将主流程改为 `sh + env` 方式并保留手工命令作为参考
- [x] 2.3 执行 shell 语法检查与 OpenSpec 校验
