---
title: 小程序证书列表页验收 evidence
change_id: add-miniapp-certificate-list-page
requirement_id: REQ-0057-certificate-list-page
created_at: 2026-07-20 09:35:00
updated_at: 2026-07-20 09:35:00
---

# 小程序证书列表页验收 evidence

## 静态与接口校验

```yaml
target: add-miniapp-certificate-list-page
page_path: pages/certificates/index
entry: tabbar
source: static_test
status: passed
artifact_ref: tests/test_miniapp_static.py::test_miniapp_certificate_list_page_replaces_placeholder_with_public_list
conclusion:
  status_bar: not_applicable
  capsule_reserve: not_applicable
  back_fallback: not_applicable
  content_offset: pass
remaining_risk: DevTools/真机视口仍需人工截图复核。
```

```yaml
target: add-miniapp-certificate-list-page
api_path: GET /api/v1/miniapp/certificates
source: pytest
status: passed
artifact_ref: tests/test_miniapp_home.py::test_miniapp_certificate_list_filters_public_data_and_supports_facets
conclusion:
  public_filter: pass
  pagination: pass
  facets: pass
  internal_fields: pass
remaining_risk:
```

## 设备截图矩阵

```yaml
target: add-miniapp-certificate-list-page
page_path: pages/certificates/index
entry: tabbar
viewport: 320pt
source: devtools
status: follow_up
artifact_ref: manual-summary
conclusion:
  status_bar: follow_up
  capsule_reserve: follow_up
  back_fallback: not_applicable
  content_offset: follow_up
remaining_risk: 当前命令环境未连接微信开发者工具，需人工补 320pt 截图。
```

```yaml
target: add-miniapp-certificate-list-page
page_path: pages/certificates/index
entry: tabbar
viewport: 375pt
source: devtools
status: follow_up
artifact_ref: manual-summary
conclusion:
  status_bar: follow_up
  capsule_reserve: follow_up
  back_fallback: not_applicable
  content_offset: follow_up
remaining_risk: 当前命令环境未连接微信开发者工具，需人工补 375pt 截图。
```

```yaml
target: add-miniapp-certificate-list-page
page_path: pages/certificates/index
entry: tabbar
viewport: 430pt
source: devtools
status: follow_up
artifact_ref: manual-summary
conclusion:
  status_bar: follow_up
  capsule_reserve: follow_up
  back_fallback: not_applicable
  content_offset: follow_up
remaining_risk: 当前命令环境未连接微信开发者工具，需人工补 430pt 截图。
```

```yaml
target: add-miniapp-certificate-list-page
page_path: pages/certificates/index
entry: tabbar
viewport: device
source: real_device
status: blocked
artifact_ref: manual-summary
conclusion:
  status_bar: blocked
  capsule_reserve: blocked
  back_fallback: not_applicable
  content_offset: blocked
remaining_risk: 当前命令环境无真机连接，未写作真机通过。
```
