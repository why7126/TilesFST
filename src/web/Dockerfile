# 文档用途：Web 前端 Docker 镜像构建
# 文档内容：npm 构建 React 应用并使用 Nginx 托管静态资源
# 内容来源：AI自动生成，项目团队确认
# 更新方式：前端构建命令、共享资源路径、Nginx 配置或端口变化时必须同步更新注释
# 备注：构建上下文为项目根目录，需同时包含 src/web 与 src/shared

# 构建阶段：官方 Node 镜像备用写法；当前启用国内镜像源以提升本地构建稳定性。
# FROM node:22-alpine AS builder
# Node 22 Alpine 构建 React 19 / TypeScript 前端产物。
FROM m.daocloud.io/docker.io/node:22-alpine AS builder

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

# 运行阶段：官方 Nginx 镜像备用写法；当前启用国内镜像源以提升拉取稳定性。
# FROM nginx:1.27-alpine
# Nginx 运行时仅承载静态资源与 API / media 反代配置。
FROM m.daocloud.io/docker.io/nginx:1.27-alpine
# 覆盖默认站点配置，保持 SPA fallback、API 反代与上传体积限制一致。
COPY src/web/nginx.conf /etc/nginx/conf.d/default.conf
# 从构建阶段复制静态产物，避免把 node_modules 带入运行镜像。
COPY --from=builder /app/src/web/dist /usr/share/nginx/html
# 声明容器内 Nginx 监听端口；宿主机映射由 docker-compose 控制。
EXPOSE 80
# 前台运行 Nginx，作为容器主进程。
CMD ["nginx", "-g", "daemon off;"]
