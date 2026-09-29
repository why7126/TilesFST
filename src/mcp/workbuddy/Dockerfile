# Reuse the backend image's locked Python 3.12 dependency environment.
# Production builds must supply a reviewed image digest.
ARG WORKBUDDY_BASE_IMAGE=tilesfst-tilesfst-backend:latest
FROM ${WORKBUDDY_BASE_IMAGE}
USER root
WORKDIR /app
COPY src/mcp /app/src/mcp
RUN mkdir -p /app/data/workbuddy/idempotency /run/secrets \
    && chown -R 10001:10001 /app/data/workbuddy
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
USER 10001:10001
EXPOSE 8010
CMD ["/app/.venv/bin/python", "-m", "uvicorn", "src.mcp.workbuddy.http_server:app", "--host", "0.0.0.0", "--port", "8010", "--workers", "1", "--no-proxy-headers", "--no-access-log"]
