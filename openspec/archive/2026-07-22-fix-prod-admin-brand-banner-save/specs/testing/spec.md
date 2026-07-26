---
created_at: 2026-07-21 15:28:51
updated_at: 2026-07-21 15:28:51
---

# testing Specification Delta

## ADDED Requirements

### Requirement: 品牌详情 Banner 保存修复必须有回归测试

The BUG-0075 fix SHALL include focused regression coverage for admin brand-detail Banner save, production MySQL schema compatibility, and public display read consistency.

#### Scenario: Admin 品牌详情 Banner 保存回归

- **WHEN** backend tests run for this change
- **THEN** tests SHALL cover `POST /api/v1/admin/banners` with `jump_type=BRAND_DETAIL` and a valid enabled brand
- **AND** tests SHALL cover editing an existing brand-detail Banner
- **AND** tests SHALL assert `brand_id`, `jump_type`, `image_source`, and `image_object_key` are persisted and returned.

#### Scenario: 品牌详情 Banner 失败场景回归

- **WHEN** backend tests run for this change
- **THEN** tests SHALL cover invalid brand id, disabled brand, missing brand logo, logo object key mismatch, and duplicate title where applicable
- **AND** tests SHALL assert unified error envelope responses with stable business errors or equivalent clear validation messages
- **AND** tests SHALL assert responses do not expose raw SQL, database DSNs, MinIO credentials, or internal stack traces.

#### Scenario: MySQL schema drift 修复回归

- **WHEN** database compatibility tests or validation scripts run for this change
- **THEN** they SHALL verify an existing MySQL `banners` table missing `brand_id` can be detected and safely remediated or blocked before production API traffic
- **AND** repeated execution SHALL remain idempotent
- **AND** default SQLite pytest SHALL remain runnable without a local MySQL service.

#### Scenario: 展示读取一致性回归

- **WHEN** tests or smoke verification read saved online brand-detail Banner data
- **THEN** admin list/detail and miniapp carousel query paths SHALL observe the same saved configuration
- **AND** homepage carousel and brand-list carousel queries SHALL remain separated by `position`.
