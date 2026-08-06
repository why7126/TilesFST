ARG DOCS_SITE_NODE_BASE_IMAGE=node:22-alpine
FROM ${DOCS_SITE_NODE_BASE_IMAGE}

ARG MINTLIFY_CLI_VERSION=4.2.45

# /home/node/.mintlify is an ephemeral container cache; Compose must not mount it as a volume.
RUN npm install -g mintlify@${MINTLIFY_CLI_VERSION} \
    && mkdir -p /home/node/.mintlify /workspace/mintlify \
    && chown -R node:node /home/node/.mintlify /workspace

USER node
WORKDIR /workspace/mintlify
ENV HOME=/home/node
ENV NODE_ENV=development

EXPOSE 3000

CMD ["mintlify", "dev", "--host", "0.0.0.0", "--port", "3000"]
