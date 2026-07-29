## 1. Implementation

- [x] 1.1 Update production Compose image references to use `TILESFST_IMAGE_TAG`.
- [x] 1.2 Update `.env.example` with unified image tag and repository variables.
- [x] 1.3 Update `scripts/build-images.env.example` so release dir and tar name default to tag-derived values.
- [x] 1.4 Update deployment documentation and production image release guide.

## 2. Validation

- [x] 2.1 Run `bash -n scripts/build-images.sh`.
- [x] 2.2 Render `docker-compose.prod.yml` with `TILESFST_IMAGE_TAG=v9.8.7` and confirm backend/web images use that tag.
- [x] 2.3 Render `docker-compose.prod.external.yml` with `TILESFST_IMAGE_TAG=v9.8.7` and confirm backend/web images use that tag.
