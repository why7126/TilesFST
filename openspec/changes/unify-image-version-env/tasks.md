## 1. 实现

- [x] 1.1 更新生产 Compose 镜像引用，统一使用 `TILESFST_IMAGE_TAG`。
- [x] 1.2 更新 `.env.example`，补充统一镜像 tag 和仓库变量。
- [x] 1.3 更新 `scripts/build-images.env.example`，让 release dir 和 tar 名称默认由 tag 推导。
- [x] 1.4 更新部署文档和生产镜像发布指南。

## 2. 验证

- [x] 2.1 运行 `bash -n scripts/build-images.sh`。
- [x] 2.2 使用 `TILESFST_IMAGE_TAG=v9.8.7` 渲染 `docker-compose.prod.yml`，确认 backend/web 镜像使用该 tag。
- [x] 2.3 使用 `TILESFST_IMAGE_TAG=v9.8.7` 渲染 `docker-compose.prod.external.yml`，确认 backend/web 镜像使用该 tag。
