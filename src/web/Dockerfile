# 文档用途：Web 前端 Docker 镜像构建
# 文档内容：npm 构建 React 应用并使用 Nginx 托管静态资源
# 内容来源：AI自动生成，项目团队确认
# 更新方式：前端构建命令、共享资源路径、Nginx 配置或端口变化时必须同步更新注释
# 备注：构建上下文为项目根目录，需同时包含 src/web 与 src/shared

# 构建阶段基础镜像可由 Compose build args 覆盖；默认使用官方镜像，避免单一镜像源故障阻断构建。
ARG WEB_NODE_BASE_IMAGE=node:22-alpine
# 运行阶段基础镜像可由 Compose build args 覆盖；默认使用官方镜像，避免单一镜像源故障阻断构建。
ARG WEB_NGINX_BASE_IMAGE=nginx:1.27-alpine
# Node 22 Alpine 构建 React 19 / TypeScript 前端产物。
FROM ${WEB_NODE_BASE_IMAGE} AS builder

# Web 子项目工作目录；npm 命令在该目录下执行。
WORKDIR /app/src/web
# 先复制 package.json，以便 Docker 构建缓存复用依赖安装层。
COPY src/web/package.json ./
# 安装前端依赖；如后续引入 lockfile，需要同步复制并改为可复现安装命令。
RUN npm install
# 复制 Web 源码。
COPY src/web/ .
# 复制共享设计系统与跨端类型，供 Vite 构建解析 @shared 引用。
COPY src/shared/ ../shared/
# 生成生产静态资源到 /app/src/web/dist。
RUN npm run build

# Nginx 运行时仅承载静态资源与 API / media 反代配置。
FROM ${WEB_NGINX_BASE_IMAGE}
# 仅渲染上传配置变量，保留 $host、$remote_addr 等 Nginx 运行时变量。
ENV NGINX_ENVSUBST_FILTER="^UPLOAD_"
# 上传反代默认值；Compose 可按生产环境覆盖。
ENV UPLOAD_CLIENT_MAX_BODY_SIZE="512m"
ENV UPLOAD_CLIENT_BODY_TIMEOUT_SECONDS="600"
ENV UPLOAD_PROXY_CONNECT_TIMEOUT_SECONDS="60"
ENV UPLOAD_PROXY_SEND_TIMEOUT_SECONDS="600"
ENV UPLOAD_PROXY_READ_TIMEOUT_SECONDS="600"
ENV UPLOAD_SEND_TIMEOUT_SECONDS="600"
ENV UPLOAD_PROXY_REQUEST_BUFFERING="off"
# 运行时渲染站点配置，允许通过环境变量调整上传路径的 body 限制与反代超时。
COPY src/web/nginx.conf.template /etc/nginx/templates/default.conf.template
# 从构建阶段复制静态产物，避免把 node_modules 带入运行镜像。
COPY --from=builder /app/src/web/dist /usr/share/nginx/html
# 声明容器内 Nginx 监听端口；宿主机映射由 docker-compose 控制。
EXPOSE 80
# 前台运行 Nginx，作为容器主进程。
CMD ["nginx", "-g", "daemon off;"]
