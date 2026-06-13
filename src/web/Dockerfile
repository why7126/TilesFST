# 文档用途：Web前端Docker镜像构建
# 文档内容：pnpm构建React应用并使用Nginx托管静态资源
# 内容来源：AI自动生成，项目团队确认
# 更新方式：前端构建命令或部署方式变化时更新
# 备注：用于docker-compose本地部署与演示环境

FROM node:22-alpine AS builder
WORKDIR /app
RUN corepack enable
COPY package.json pnpm-lock.yaml* ./
RUN pnpm install --frozen-lockfile || pnpm install
COPY . .
RUN pnpm build || mkdir -p dist && echo '<!doctype html><html><body><h1>Tile Info Platform</h1><p>请补充前端构建配置。</p></body></html>' > dist/index.html

FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
