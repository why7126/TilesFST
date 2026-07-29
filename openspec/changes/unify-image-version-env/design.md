## Overview

本变更只调整部署配置契约，不改变镜像构建脚本的核心流程。`scripts/build-images.sh` 已支持从 `IMAGE_BUILD_TAG` 推导 `IMAGE_BUILD_RELEASE_DIR` 和 `IMAGE_BUILD_TAR_NAME`，因此示例文件改为保留默认推导并把覆盖项注释化。

生产 Compose 由两个完整镜像引用变量调整为“仓库名 + 统一 tag”拼接：

```text
${TILESFST_BACKEND_IMAGE_REPOSITORY:-tilesfst-backend}:${TILESFST_IMAGE_TAG:-v0.0.4}
${TILESFST_WEB_IMAGE_REPOSITORY:-tilesfst-web}:${TILESFST_IMAGE_TAG:-v0.0.4}
```

## Decisions

- 使用 `TILESFST_IMAGE_TAG` 作为生产 Compose 的统一版本输入。
- 使用 `TILESFST_BACKEND_IMAGE_REPOSITORY` 与 `TILESFST_WEB_IMAGE_REPOSITORY` 表达镜像仓库名，避免把仓库名和 tag 重新耦合为两个完整镜像变量。
- 不修改 `PRODUCT_VERSION` 策略；用户可见产品版本仍按发布规范由 `src/shared/product-version.ts` 人工维护。
- 不修改 `scripts/build-images.sh` 的默认推导逻辑，仅同步示例与文档，降低发版配置出错概率。

## Risks

- 运维若仍使用旧变量 `TILESFST_BACKEND_IMAGE` / `TILESFST_WEB_IMAGE`，新 Compose 不再读取这两个变量。部署文档和 `.env.example` 已同步新变量名。
- 私有仓库路径包含端口时可放入 repository 变量，例如 `registry.example.com:5000/tilesfst-backend`，Compose 拼接后仍形成合法镜像引用。

## Validation

- `bash -n scripts/build-images.sh`
- 使用示例生产密钥占位与 `TILESFST_IMAGE_TAG=v9.8.7` 执行 `docker compose -f docker-compose.prod.yml config`，确认镜像为 `tilesfst-backend:v9.8.7` 与 `tilesfst-web:v9.8.7`。
- 使用示例生产密钥占位与 `TILESFST_IMAGE_TAG=v9.8.7` 执行 `docker compose -f docker-compose.prod.external.yml config`，确认镜像为 `tilesfst-backend:v9.8.7` 与 `tilesfst-web:v9.8.7`。
