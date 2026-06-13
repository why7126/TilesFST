# 文档用途：Web前端Docker镜像构建
# 文档内容：npm构建React应用并使用Nginx托管静态资源
# 内容来源：AI自动生成，项目团队确认
# 更新方式：前端构建命令或部署方式变化时更新
# 备注：构建上下文为项目根目录，需同时包含 src/web 与 src/shared

FROM node:22-alpine AS builder
WORKDIR /app/src/web
COPY src/web/package.json ./
RUN npm install
COPY src/web/ .
COPY src/shared/ ../shared/
RUN npm run build

FROM nginx:1.27-alpine
COPY src/web/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/src/web/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
