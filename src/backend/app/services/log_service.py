"""Product usage logging service."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from app.core.exceptions import AuthInvalidRequestError
from app.repositories.log_repository import LogRecord, LogRepository
from app.repositories.task_trace_repository import TaskTraceRepository
from app.repositories.user_repository import UserRecord
from app.schemas.logs import (
    LogDetailData,
    LogDetailSection,
    LogListData,
    LogListItem,
    LogMetricsData,
    LogObservabilityData,
    LogObservabilityQueryParams,
    LogQueryParams,
    ObservabilityDistributionItem,
    ObservabilityEndpointItem,
    ObservabilitySlowRequestItem,
    ObservabilitySpanItem,
    ObservabilitySummaryData,
    ObservabilityTaskItem,
    ObservabilityTraceResultsData,
    RequestSnapshotActorData,
    RequestSnapshotData,
    RequestSnapshotInputData,
    RequestSnapshotRequestData,
    RequestSnapshotResourceData,
    RequestSnapshotResponseData,
    RequestSnapshotTimingData,
    TaskTraceData,
    TaskTraceSpanData,
    UsageEventCreate,
    UsageEventData,
)
from app.services.task_trace_service import TaskTraceService

SENSITIVE_KEYS = {
    "authorization",
    "cookie",
    "password",
    "token",
    "access_token",
    "refresh_token",
    "secret",
    "secret_key",
    "access_key",
    "dsn",
    "database_url",
    "env",
    ".env",
    "minio_access_key",
    "minio_secret_key",
    "accesskey",
    "secretkey",
    "raw_object_key",
    "object_key",
    "internal_path",
    "customer_data",
    "real_customer_data",
    "raw_response",
    "raw_payload",
}

EVENT_DEFINITIONS: dict[str, dict[str, Any]] = {
    "page_view": {
        "category": "navigation",
        "required": {"page_path", "module"},
        "forbidden": {"token", "password"},
    },
    "search_submit": {
        "category": "discovery",
        "required": {"module", "keyword"},
        "forbidden": {"token", "password"},
    },
    "filter_change": {
        "category": "discovery",
        "required": {"module", "filter_name", "filter_value"},
        "forbidden": {"token", "password"},
    },
    "detail_view": {
        "category": "inspection",
        "required": {"module", "entity_type", "entity_id"},
        "forbidden": {"token", "password"},
    },
    "copy_request_id": {
        "category": "utility",
        "required": {"module", "entity_type", "entity_id", "request_id"},
        "forbidden": {"token", "password", "authorization", "cookie"},
    },
    "entity_create": {
        "category": "mutation",
        "required": {"entity_type", "entity_id"},
        "forbidden": {"raw_payload", "password"},
    },
    "entity_update": {
        "category": "mutation",
        "required": {"entity_type", "entity_id", "changed_fields"},
        "forbidden": {"before_value", "password"},
    },
    "entity_delete": {
        "category": "mutation",
        "required": {"entity_type", "entity_id"},
        "forbidden": {"raw_payload", "token"},
    },
    "status_change": {
        "category": "mutation",
        "required": {"entity_type", "entity_id", "from_status", "to_status"},
        "forbidden": {"raw_payload", "token"},
    },
    "media_upload": {
        "category": "media",
        "required": {"media_type", "business_type", "file_size", "result"},
        "forbidden": {"raw_filename", "token"},
    },
    "login_success": {
        "category": "auth",
        "required": {"user_id", "role"},
        "forbidden": {"password", "token"},
    },
    "login_failed": {
        "category": "auth",
        "required": {"username_masked", "reason"},
        "forbidden": {"password", "token"},
    },
    "api_error": {
        "category": "reliability",
        "required": {"request_id", "path", "status_code", "error_code"},
        "forbidden": {"authorization", "cookie"},
    },
    "product_detail_view": {
        "category": "miniapp_engagement",
        "required": {"product_id", "page_path", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_filename"},
    },
    "home_share": {
        "category": "miniapp_engagement",
        "required": {"page_path", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_filename"},
    },
    "product_share": {
        "category": "miniapp_engagement",
        "required": {"product_id", "page_path", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_filename"},
    },
    "home_contact_click": {
        "category": "miniapp_engagement",
        "required": {"page_path", "contact_type", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_filename", "phone"},
    },
    "product_contact_click": {
        "category": "miniapp_engagement",
        "required": {"product_id", "page_path", "contact_type", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_filename", "phone"},
    },
    "miniapp_home_search_click": {
        "category": "miniapp_home_style",
        "required": {"page_path", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_filename", "phone"},
    },
    "miniapp_home_quick_entry_click": {
        "category": "miniapp_home_style",
        "required": {"page_path", "entry_key", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_filename", "phone"},
    },
    "miniapp_home_new_product_click": {
        "category": "miniapp_home_style",
        "required": {"product_id", "page_path", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_filename", "phone"},
    },
    "miniapp_home_hot_product_click": {
        "category": "miniapp_home_style",
        "required": {"product_id", "page_path", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_filename", "phone"},
    },
    "miniapp_home_waterfall_product_click": {
        "category": "miniapp_home_style",
        "required": {"product_id", "page_path", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_filename", "phone"},
    },
    "miniapp_home_favorite_visual_click": {
        "category": "miniapp_home_style",
        "required": {"product_id", "page_path", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_filename", "phone"},
    },
    "miniapp_certificate_tab_click": {
        "category": "miniapp_home_style",
        "required": {"page_path", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_filename", "phone"},
    },
    "certificate_list_page_view": {
        "category": "miniapp_certificate_list",
        "required": {"page_path", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "certificate_list_load": {
        "category": "miniapp_certificate_list",
        "required": {"page_path", "page", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "certificate_list_refresh": {
        "category": "miniapp_certificate_list",
        "required": {"page_path", "page", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "certificate_list_load_more": {
        "category": "miniapp_certificate_list",
        "required": {"page_path", "page", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "certificate_list_retry": {
        "category": "miniapp_certificate_list",
        "required": {"page_path", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "certificate_click": {
        "category": "miniapp_certificate_list",
        "required": {"page_path", "certificateId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "certificate_preview_click": {
        "category": "miniapp_certificate_list",
        "required": {"page_path", "certificateId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "certificate_load_failed": {
        "category": "miniapp_certificate_list",
        "required": {"page_path", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "certificate_detail_view": {
        "category": "miniapp_certificate_detail",
        "required": {"page_path", "certificateId", "client_type"},
        "forbidden": {
            "authorization",
            "cookie",
            "raw_payload",
            "raw_object_key",
            "object_key",
            "internal_remark",
            "phone",
        },
    },
    "certificate_detail_media_switch": {
        "category": "miniapp_certificate_detail",
        "required": {"page_path", "certificateId", "client_type"},
        "forbidden": {
            "authorization",
            "cookie",
            "raw_payload",
            "raw_object_key",
            "object_key",
            "internal_remark",
            "phone",
        },
    },
    "certificate_detail_image_preview": {
        "category": "miniapp_certificate_detail",
        "required": {"page_path", "certificateId", "client_type"},
        "forbidden": {
            "authorization",
            "cookie",
            "raw_payload",
            "raw_object_key",
            "object_key",
            "internal_remark",
            "phone",
        },
    },
    "certificate_detail_file_open": {
        "category": "miniapp_certificate_detail",
        "required": {"page_path", "certificateId", "client_type"},
        "forbidden": {
            "authorization",
            "cookie",
            "raw_payload",
            "raw_object_key",
            "object_key",
            "internal_remark",
            "phone",
        },
    },
    "certificate_detail_brand_click": {
        "category": "miniapp_certificate_detail",
        "required": {"page_path", "certificateId", "brandId", "client_type"},
        "forbidden": {
            "authorization",
            "cookie",
            "raw_payload",
            "raw_object_key",
            "object_key",
            "internal_remark",
            "phone",
        },
    },
    "certificate_detail_share_click": {
        "category": "miniapp_certificate_detail",
        "required": {"page_path", "certificateId", "client_type"},
        "forbidden": {
            "authorization",
            "cookie",
            "raw_payload",
            "raw_object_key",
            "object_key",
            "internal_remark",
            "phone",
        },
    },
    "certificate_detail_load_failed": {
        "category": "miniapp_certificate_detail",
        "required": {"page_path", "client_type"},
        "forbidden": {
            "authorization",
            "cookie",
            "raw_payload",
            "raw_object_key",
            "object_key",
            "raw_response",
            "internal_remark",
            "phone",
        },
    },
    "miniapp_home_waterfall_load": {
        "category": "miniapp_home_style",
        "required": {"page_path", "page", "page_size", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_filename", "phone"},
    },
    "miniapp_home_waterfall_load_failed": {
        "category": "miniapp_home_style",
        "required": {"page_path", "page", "reason", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_filename", "phone"},
    },
    "miniapp_home_waterfall_end_reached": {
        "category": "miniapp_home_style",
        "required": {"page_path", "page", "total", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_filename", "phone"},
    },
    "sku_detail_view": {
        "category": "miniapp_sku_detail",
        "required": {"sku_id", "page_path", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "sku_media_swipe": {
        "category": "miniapp_sku_detail",
        "required": {"sku_id", "page_path", "client_type", "media_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "sku_image_preview": {
        "category": "miniapp_sku_detail",
        "required": {"sku_id", "page_path", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "sku_video_play": {
        "category": "miniapp_sku_detail",
        "required": {"sku_id", "page_path", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "sku_video_fullscreen_click": {
        "category": "miniapp_sku_detail",
        "required": {"sku_id", "page_path", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "sku_video_fullscreen_enter": {
        "category": "miniapp_sku_detail",
        "required": {"sku_id", "page_path", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "sku_video_fullscreen_exit": {
        "category": "miniapp_sku_detail",
        "required": {"sku_id", "page_path", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "sku_video_fullscreen_failed": {
        "category": "miniapp_sku_detail",
        "required": {"sku_id", "page_path", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "sku_video_action_menu_open": {
        "category": "miniapp_sku_detail",
        "required": {"sku_id", "page_path", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "sku_video_action_cancel": {
        "category": "miniapp_sku_detail",
        "required": {"sku_id", "page_path", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "sku_video_action_share": {
        "category": "miniapp_sku_detail",
        "required": {"sku_id", "page_path", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "sku_video_action_save": {
        "category": "miniapp_sku_detail",
        "required": {"sku_id", "page_path", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "sku_video_save_success": {
        "category": "miniapp_sku_detail",
        "required": {"sku_id", "page_path", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "sku_video_save_failed": {
        "category": "miniapp_sku_detail",
        "required": {"sku_id", "page_path", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "sku_favorite": {
        "category": "miniapp_sku_detail",
        "required": {"sku_id", "page_path", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "sku_unfavorite": {
        "category": "miniapp_sku_detail",
        "required": {"sku_id", "page_path", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "sku_share_click": {
        "category": "miniapp_sku_detail",
        "required": {"sku_id", "page_path", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "sku_brand_click": {
        "category": "miniapp_sku_detail",
        "required": {"sku_id", "brand_id", "page_path", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "sku_recommend_click": {
        "category": "miniapp_sku_detail",
        "required": {"sku_id", "target_sku_id", "recommend_type", "page_path", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "sku_load_error": {
        "category": "miniapp_sku_detail",
        "required": {"sku_id", "page_path", "client_type", "error_code", "stage"},
        "forbidden": {
            "authorization",
            "cookie",
            "raw_payload",
            "raw_object_key",
            "object_key",
            "raw_response",
            "internal_path",
            "phone",
        },
    },
    "category_page_view": {
        "category": "miniapp_category_list",
        "required": {"page_path", "client_type", "has_cache"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "primary_category_click": {
        "category": "miniapp_category_list",
        "required": {"category_id", "category_index", "page_path", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "primary_category_product_list_click": {
        "category": "miniapp_category_list",
        "required": {
            "category_id",
            "category_name",
            "category_level",
            "sourcePage",
            "category_index",
            "page_path",
            "client_type",
        },
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "secondary_category_click": {
        "category": "miniapp_category_list",
        "required": {"category_id", "parent_category_id", "category_index", "page_path", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "category_load_failed": {
        "category": "miniapp_category_list",
        "required": {"page_path", "client_type", "error_code", "has_cache"},
        "forbidden": {
            "authorization",
            "cookie",
            "raw_payload",
            "raw_object_key",
            "object_key",
            "raw_response",
            "internal_path",
            "phone",
        },
    },
    "product_list_page_view": {
        "category": "miniapp_product_list",
        "required": {"page_path", "sourcePage", "sort", "pageSize", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "internal_remark", "phone"},
    },
    "product_list_item_exposure": {
        "category": "miniapp_product_list",
        "required": {"skuId", "sourcePage", "positionIndex", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "internal_remark", "phone"},
    },
    "product_list_item_click": {
        "category": "miniapp_product_list",
        "required": {"skuId", "sourcePage", "positionIndex", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "internal_remark", "phone"},
    },
    "product_list_filter_open": {
        "category": "miniapp_product_list",
        "required": {"sourcePage", "filterSnapshot", "sort", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "internal_remark", "phone"},
    },
    "product_list_filter_apply": {
        "category": "miniapp_product_list",
        "required": {"sourcePage", "filterSnapshot", "sort", "resultCount", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "internal_remark", "phone"},
    },
    "product_list_sort_change": {
        "category": "miniapp_product_list",
        "required": {"sourcePage", "filterSnapshot", "sort", "resultCount", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "internal_remark", "phone"},
    },
    "product_list_refresh": {
        "category": "miniapp_product_list",
        "required": {"sourcePage", "page", "pageSize", "resultCount", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "internal_remark", "phone"},
    },
    "product_list_load_more": {
        "category": "miniapp_product_list",
        "required": {"sourcePage", "page", "pageSize", "resultCount", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "internal_remark", "phone"},
    },
    "product_list_load_failed": {
        "category": "miniapp_product_list",
        "required": {"sourcePage", "page", "pageSize", "errorCode", "requestId", "client_type"},
        "forbidden": {
            "authorization",
            "cookie",
            "raw_payload",
            "raw_object_key",
            "object_key",
            "raw_response",
            "internal_path",
            "internal_remark",
            "phone",
        },
    },
    "product_list_share_click": {
        "category": "miniapp_product_list",
        "required": {"sourcePage", "share_channel", "share_path", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "internal_remark", "phone"},
    },
    "brand_list_page_view": {
        "category": "miniapp_brand_list",
        "required": {"page_path", "sourcePage", "resultCount", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "internal_remark", "phone"},
    },
    "brand_list_carousel_click": {
        "category": "miniapp_brand_list",
        "required": {"page_path", "jumpType", "positionIndex", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "internal_remark", "phone"},
    },
    "brand_list_card_click": {
        "category": "miniapp_brand_list",
        "required": {"page_path", "brandId", "positionIndex", "sourcePage", "sourceEntry", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "internal_remark", "phone"},
    },
    "brand_detail_share_click": {
        "category": "miniapp_brand_detail",
        "required": {"page_path", "brandId", "share_channel", "share_path", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "internal_remark", "phone"},
    },
    "search_page_view": {
        "category": "miniapp_search",
        "required": {"page_path", "client_type", "sourcePage", "requestId"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "search_input": {
        "category": "miniapp_search",
        "required": {"keyword", "normalizedKeyword", "scope", "sourcePage", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "search_suggestion_exposure": {
        "category": "miniapp_search",
        "required": {"keyword", "normalizedKeyword", "scope", "resultCount", "sourcePage", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "search_suggestion_click": {
        "category": "miniapp_search",
        "required": {"keyword", "normalizedKeyword", "scope", "entityType", "sourcePage", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "search_result_exposure": {
        "category": "miniapp_search",
        "required": {"keyword", "normalizedKeyword", "scope", "entityType", "resultCount", "sourcePage", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "search_result_click": {
        "category": "miniapp_search",
        "required": {"keyword", "normalizedKeyword", "scope", "entityType", "sourcePage", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "search_filter_apply": {
        "category": "miniapp_search",
        "required": {"keyword", "normalizedKeyword", "scope", "filterSnapshot", "resultCount", "sourcePage", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "search_no_result": {
        "category": "miniapp_search",
        "required": {"keyword", "normalizedKeyword", "scope", "resultCount", "sourcePage", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "search_history_click": {
        "category": "miniapp_search",
        "required": {"keyword", "normalizedKeyword", "scope", "sourcePage", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "search_history_delete": {
        "category": "miniapp_search",
        "required": {"keyword", "normalizedKeyword", "scope", "sourcePage", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "search_history_clear": {
        "category": "miniapp_search",
        "required": {"scope", "sourcePage", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "favorite_list_page_view": {
        "category": "miniapp_favorite_list",
        "required": {"page_path", "terminal", "sourcePage", "hasLogin", "resultCount", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "favorite_list_load_failed": {
        "category": "miniapp_favorite_list",
        "required": {"page_path", "terminal", "errorCode", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "raw_response", "phone"},
    },
    "favorite_list_empty_action_click": {
        "category": "miniapp_favorite_list",
        "required": {"page_path", "terminal", "target", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "favorite_list_item_click": {
        "category": "miniapp_favorite_list",
        "required": {
            "page_path",
            "terminal",
            "objectType",
            "objectId",
            "index",
            "sourcePage",
            "hasLogin",
            "resultCount",
            "requestId",
            "client_type",
        },
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "favorite_list_remove": {
        "category": "miniapp_favorite_list",
        "required": {
            "page_path",
            "terminal",
            "objectType",
            "objectId",
            "sourcePage",
            "hasLogin",
            "resultCount",
            "requestId",
            "client_type",
        },
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "phone"},
    },
    "brand_detail_view": {
        "category": "miniapp_brand_detail",
        "required": {"page_path", "sourcePage", "sourceModule", "brandId", "tab", "page", "pageSize", "resultCount", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "internal_remark", "phone"},
    },
    "brand_detail_load_failed": {
        "category": "miniapp_brand_detail",
        "required": {"page_path", "sourcePage", "sourceModule", "brandId", "tab", "page", "pageSize", "resultCount", "requestId", "client_type"},
        "forbidden": {
            "authorization",
            "cookie",
            "raw_payload",
            "raw_object_key",
            "object_key",
            "raw_response",
            "internal_remark",
            "phone",
        },
    },
    "brand_detail_tab_click": {
        "category": "miniapp_brand_detail",
        "required": {"page_path", "sourcePage", "sourceModule", "brandId", "tab", "page", "pageSize", "resultCount", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "internal_remark", "phone"},
    },
    "brand_products_load": {
        "category": "miniapp_brand_detail",
        "required": {"page_path", "sourcePage", "sourceModule", "brandId", "tab", "page", "pageSize", "resultCount", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "internal_remark", "phone"},
    },
    "brand_products_load_more": {
        "category": "miniapp_brand_detail",
        "required": {"page_path", "sourcePage", "sourceModule", "brandId", "tab", "page", "pageSize", "resultCount", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "internal_remark", "phone"},
    },
    "brand_products_load_failed": {
        "category": "miniapp_brand_detail",
        "required": {"page_path", "sourcePage", "sourceModule", "brandId", "tab", "page", "pageSize", "resultCount", "requestId", "client_type"},
        "forbidden": {
            "authorization",
            "cookie",
            "raw_payload",
            "raw_object_key",
            "object_key",
            "raw_response",
            "internal_remark",
            "phone",
        },
    },
    "brand_certificates_load": {
        "category": "miniapp_brand_detail",
        "required": {"page_path", "sourcePage", "sourceModule", "brandId", "tab", "page", "pageSize", "resultCount", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "internal_remark", "phone"},
    },
    "brand_certificates_load_failed": {
        "category": "miniapp_brand_detail",
        "required": {"page_path", "sourcePage", "sourceModule", "brandId", "tab", "page", "pageSize", "resultCount", "requestId", "client_type"},
        "forbidden": {
            "authorization",
            "cookie",
            "raw_payload",
            "raw_object_key",
            "object_key",
            "raw_response",
            "internal_remark",
            "phone",
        },
    },
    "brand_certificate_click": {
        "category": "miniapp_brand_detail",
        "required": {"page_path", "sourcePage", "sourceModule", "brandId", "tab", "certificateId", "index", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "internal_remark", "phone"},
    },
    "product_card_exposure": {
        "category": "miniapp_product_card",
        "required": {"page_path", "sourcePage", "sourceModule", "listContext", "index", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "internal_remark", "phone"},
    },
    "product_card_click": {
        "category": "miniapp_product_card",
        "required": {"page_path", "sourcePage", "sourceModule", "listContext", "index", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "internal_remark", "phone"},
    },
    "product_card_unavailable_click": {
        "category": "miniapp_product_card",
        "required": {"page_path", "sourcePage", "sourceModule", "listContext", "index", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "internal_remark", "phone"},
    },
    "product_card_image_failed": {
        "category": "miniapp_product_card",
        "required": {"page_path", "sourcePage", "sourceModule", "listContext", "index", "requestId", "client_type"},
        "forbidden": {
            "authorization",
            "cookie",
            "raw_payload",
            "raw_object_key",
            "object_key",
            "raw_response",
            "internal_remark",
            "phone",
        },
    },
    "brand_card_click": {
        "category": "miniapp_brand_card",
        "required": {"page_path", "sourcePage", "sourceModule", "listContext", "index", "requestId", "client_type"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "internal_remark", "phone"},
    },
    "brand_card_unavailable_click": {
        "category": "miniapp_brand_card",
        "required": {"page_path", "sourcePage", "sourceModule", "listContext", "index", "requestId", "client_type", "unavailableReason"},
        "forbidden": {"authorization", "cookie", "raw_payload", "raw_object_key", "object_key", "internal_remark", "phone"},
    },
    "brand_card_image_failed": {
        "category": "miniapp_brand_card",
        "required": {"page_path", "sourcePage", "sourceModule", "listContext", "index", "requestId", "client_type"},
        "forbidden": {
            "authorization",
            "cookie",
            "raw_payload",
            "raw_object_key",
            "object_key",
            "raw_response",
            "internal_remark",
            "phone",
        },
    },
}


@dataclass
class RequestLogContext:
    request_id: str
    actor_user_id: str | None
    actor_role: str | None
    client_type: str
    client_request_id: str | None
    method: str
    path: str
    status_code: int
    duration_ms: int
    ip_address: str | None
    user_agent: str | None
    error_code: str | None = None
    metadata: dict[str, Any] | None = None
    task_trace_id: str | None = None
    task_type: str | None = None
    actor_username: str | None = None


class LogService:
    def __init__(self, repo: LogRepository) -> None:
        self._repo = repo

    def record_request(self, context: RequestLogContext) -> None:
        result = "failed" if context.status_code >= 400 else "success"
        summary = f"{context.method} {context.path} · {context.status_code}"
        self._repo.insert_request_log(
            request_id=context.request_id,
            actor_user_id=context.actor_user_id,
            actor_role=context.actor_role,
            client_type=context.client_type,
            client_request_id=context.client_request_id,
            method=context.method,
            path=context.path,
            status_code=context.status_code,
            duration_ms=context.duration_ms,
            ip_address_masked=mask_ip(context.ip_address),
            user_agent_summary=truncate_text(context.user_agent, 180),
            summary=summary,
            error_code=context.error_code,
            result=result,
            task_trace_id=context.task_trace_id,
            task_type=context.task_type,
            metadata=safe_json_dumps(context.metadata or {}),
        )

    def create_usage_event(
        self,
        payload: UsageEventCreate,
        *,
        request_id: str | None,
        current_user: UserRecord | None,
        ip_address: str | None,
        user_agent: str | None,
        client_request_id: str | None = None,
    ) -> UsageEventData:
        definition = EVENT_DEFINITIONS.get(payload.event_name)
        if definition is None:
            raise AuthInvalidRequestError("未知埋点事件")

        properties = dict(payload.properties)
        required = set(definition["required"])
        missing = sorted(required.difference(properties.keys()))
        if missing:
            raise AuthInvalidRequestError(f"埋点事件缺少必填属性：{', '.join(missing)}")

        forbidden = set(definition["forbidden"]).union(SENSITIVE_KEYS)
        forbidden_present = sorted(key for key in properties if key.lower() in forbidden)
        if forbidden_present:
            raise AuthInvalidRequestError(f"埋点事件包含禁止属性：{', '.join(forbidden_present)}")

        sanitized = sanitize_metadata(properties)
        effective_client_request_id = truncate_text(payload.client_request_id or client_request_id, 128)
        if effective_client_request_id:
            sanitized["client_request_id"] = effective_client_request_id
        actor_user_id = current_user.id if current_user else None
        actor_role = current_user.role if current_user else "anonymous"
        client_type = payload.client_type or "web_admin"
        summary = payload.summary or build_event_summary(payload.event_name, sanitized)
        event_id = self._repo.insert_usage_event(
            request_id=request_id or payload.request_id,
            actor_user_id=actor_user_id,
            actor_role=actor_role,
            client_type=client_type,
            event_name=payload.event_name,
            event_category=str(definition["category"]),
            page_path=payload.page_path or str(sanitized.get("page_path") or ""),
            session_id=truncate_text(payload.session_id, 128),
            ip_address_masked=mask_ip(ip_address),
            user_agent_summary=truncate_text(user_agent, 180),
            summary=truncate_text(summary, 220) or payload.event_name,
            duration_ms=payload.duration_ms,
            result=str(sanitized.get("result") or "success"),
            task_trace_id=TaskTraceService.validate_task_trace_id(payload.task_trace_id),
            task_type=truncate_text(payload.task_type, 64),
            metadata=safe_json_dumps(sanitized),
        )
        return UsageEventData(id=event_id, accepted=True)

    def list_logs(self, params: LogQueryParams) -> LogListData:
        result = self._repo.list_logs(
            page=params.page,
            page_size=params.page_size,
            log_type=params.log_type,
            keyword=params.keyword,
            actor_user_id=params.actor_user_id,
            client_type=params.client_type,
            status_code=params.status_code,
            result=params.result,
            resource_id=params.resource_id,
            path_or_request_id=params.path_or_request_id,
            task_trace_id=params.task_trace_id,
            start_time=params.start_time,
            end_time=params.end_time,
        )
        metrics = self._repo.get_metrics(today_start=today_start_utc())
        return LogListData(
            items=[to_list_item(record) for record in result.items],
            total=result.total,
            page=params.page,
            page_size=params.page_size,
            summary=LogMetricsData(
                today_logs=metrics.today_logs,
                api_errors=metrics.api_errors,
                slow_requests=metrics.slow_requests,
                sensitive_ops=metrics.sensitive_ops,
            ),
        )

    def get_observability(self, params: LogObservabilityQueryParams) -> LogObservabilityData:
        slow_request_threshold_ms = 1000
        slow_task_threshold_ms = 1000
        data = self._repo.get_observability(
            filters=params.model_dump(),
            slow_request_threshold_ms=slow_request_threshold_ms,
            slow_task_threshold_ms=slow_task_threshold_ms,
            top_limit=8,
        )
        rankings = data["rankings"]
        return LogObservabilityData(
            summary=ObservabilitySummaryData(**data["summary"]),
            distributions={
                key: [ObservabilityDistributionItem(**item) for item in value]
                for key, value in data["distributions"].items()
            },
            endpoint_errors=[ObservabilityEndpointItem(**item) for item in data["endpoint_errors"]],
            rankings={
                "slow_requests": [ObservabilitySlowRequestItem(**item) for item in rankings["slow_requests"]],
                "slow_tasks": [ObservabilityTaskItem(**item) for item in rankings["slow_tasks"]],
                "slowest_spans": [ObservabilitySpanItem(**item) for item in rankings["slowest_spans"]],
            },
            trace_results=ObservabilityTraceResultsData(**data["trace_results"]),
            thresholds={
                "slow_request_ms": slow_request_threshold_ms,
                "slow_task_ms": slow_task_threshold_ms,
            },
        )

    def get_log_detail(self, log_id: str) -> LogDetailData:
        from app.core.exceptions import AppError
        from app.core.error_codes import LOG_NOT_FOUND

        record = self._repo.get_log(log_id)
        if record is None:
            raise AppError(status_code=404, code=LOG_NOT_FOUND, message="日志不存在")
        metadata = parse_metadata(record.metadata)
        request_snapshot = build_request_snapshot(record, metadata)
        task_traces = self._build_related_task_traces(record.task_trace_id, record.request_id)
        task_trace = task_traces[0] if task_traces else None
        return LogDetailData(
            log=to_list_item(record),
            basic=LogDetailSection(
                title="基础信息",
                fields={
                    "日志 ID": record.id,
                    "日志类型": record.log_type,
                    "状态 / 结果": format_result(record),
                    "request_id": record.request_id or "-",
                    "client_request_id": record.client_request_id or metadata.get("client_request_id", "-") or "-",
                    "task_trace_id": record.task_trace_id or "-",
                    "发生时间": record.created_at,
                },
            ),
            request=LogDetailSection(
                title="请求信息",
                fields={
                    "Method": record.method or "-",
                    "Path": record.path or "-",
                    "Status Code": record.status_code if record.status_code is not None else "-",
                    "Duration": f"{record.duration_ms} ms" if record.duration_ms is not None else "-",
                    "Error Code": record.error_code or "-",
                },
            ),
            actor=LogDetailSection(
                title="操作者与客户端",
                fields={
                    "操作者": record.actor_username or record.actor_role or "anonymous",
                    "User ID": record.actor_user_id or "-",
                    "客户端": record.client_type or "-",
                    "Client Request ID": record.client_request_id or metadata.get("client_request_id", "-") or "-",
                    "IP": record.ip_address_masked or "-",
                    "User Agent": record.user_agent_summary or "-",
                },
            ),
            context=LogDetailSection(
                title="操作上下文",
                fields={
                    "业务动作": record.event_name or record.method or "-",
                    "操作摘要": record.summary,
                    "结果": record.result,
                    "路径 / 资源": record.path or "-",
                    "Task Trace": record.task_trace_id or "-",
                },
            ),
            event=LogDetailSection(
                title="埋点属性",
                fields={
                    "event_name": record.event_name or "-",
                    "module": metadata.get("module", "-"),
                    "entity_type": metadata.get("entity_type", "-"),
                    "entity_id": metadata.get("entity_id", "-"),
                    "changed_fields": metadata.get("changed_fields", "-"),
                },
            ),
            task_trace=task_trace,
            related_task_traces=task_traces,
            request_snapshot=request_snapshot,
            metadata_json=safe_json_dumps(metadata, pretty=True),
        )

    def _build_task_trace(self, task_trace_id: str | None) -> TaskTraceData | None:
        timeline = TaskTraceService(TaskTraceRepository(self._repo._db)).get_timeline(task_trace_id)
        if timeline is None or timeline.trace is None:
            return None
        slowest_span_name = timeline.trace.slowest_span_name
        return TaskTraceData(
            task_trace_id=timeline.trace.task_trace_id,
            task_type=timeline.trace.task_type,
            status=timeline.trace.status,
            parent_request_id=timeline.trace.parent_request_id,
            duration_ms=timeline.trace.duration_ms,
            resource_type=timeline.trace.resource_type,
            resource_id=timeline.trace.resource_id,
            slowest_span_name=slowest_span_name,
            error_code=timeline.trace.error_code,
            summary=timeline.trace.summary,
            spans=[
                TaskTraceSpanData(
                    span_name=span.span_name,
                    status=span.status,
                    started_at=span.started_at,
                    ended_at=span.ended_at,
                    duration_ms=span.duration_ms,
                    request_id=span.request_id,
                    error_code=span.error_code,
                    summary=span.summary,
                    is_slowest=span.span_name == slowest_span_name,
                )
                for span in timeline.spans
            ],
        )

    def _build_related_task_traces(self, task_trace_id: str | None, request_id: str | None) -> list[TaskTraceData]:
        trace_service = TaskTraceService(TaskTraceRepository(self._repo._db))
        timelines = []
        primary = trace_service.get_timeline(task_trace_id)
        if primary is not None and primary.trace is not None:
            timelines.append(primary)
        for timeline in trace_service.list_timelines_by_parent_request_id(request_id):
            if timeline.trace is None:
                continue
            if any(item.trace and item.trace.task_trace_id == timeline.trace.task_trace_id for item in timelines):
                continue
            timelines.append(timeline)
        traces: list[TaskTraceData] = []
        for timeline in timelines:
            if timeline.trace is None:
                continue
            slowest_span_name = timeline.trace.slowest_span_name
            traces.append(
                TaskTraceData(
                    task_trace_id=timeline.trace.task_trace_id,
                    task_type=timeline.trace.task_type,
                    status=timeline.trace.status,
                    parent_request_id=timeline.trace.parent_request_id,
                    duration_ms=timeline.trace.duration_ms,
                    resource_type=timeline.trace.resource_type,
                    resource_id=timeline.trace.resource_id,
                    slowest_span_name=slowest_span_name,
                    error_code=timeline.trace.error_code,
                    summary=timeline.trace.summary,
                    spans=[
                        TaskTraceSpanData(
                            span_name=span.span_name,
                            status=span.status,
                            started_at=span.started_at,
                            ended_at=span.ended_at,
                            duration_ms=span.duration_ms,
                            request_id=span.request_id,
                            error_code=span.error_code,
                            summary=span.summary,
                            is_slowest=span.span_name == slowest_span_name,
                        )
                        for span in timeline.spans
                    ],
                )
            )
        return traces


def to_list_item(record: LogRecord) -> LogListItem:
    return LogListItem(
        id=record.id,
        log_type=record.log_type,
        created_at=record.created_at,
        summary=record.summary,
        actor_name=record.actor_name,
        actor_username=record.actor_username,
        actor_role=record.actor_role,
        client_type=record.client_type or "backend",
        result=format_result(record),
        status_code=record.status_code,
        duration_ms=record.duration_ms,
        request_id=record.request_id,
        client_request_id=record.client_request_id,
        task_trace_id=record.task_trace_id,
        task_type=record.task_type,
        task_status=record.task_status,
        task_duration_ms=record.task_duration_ms,
        task_slowest_span_name=record.task_slowest_span_name,
        event_name=record.event_name,
        method=record.method,
        path=record.path,
    )


def format_result(record: LogRecord) -> str:
    if record.status_code is not None:
        return f"{record.status_code} 错误" if record.status_code >= 400 else "成功"
    return "成功" if record.result == "success" else "失败"


def build_event_summary(event_name: str, properties: dict[str, Any]) -> str:
    module = properties.get("module")
    if event_name == "search_submit" and properties.get("keyword"):
        return f"{module or 'search'} · search_submit · {properties['keyword']}"
    if event_name == "filter_change" and properties.get("filter_name"):
        return f"{module or 'filter'} · filter_change · {properties['filter_name']}"
    if event_name == "detail_view" and properties.get("entity_id"):
        return f"{module or 'detail'} · detail_view · {properties['entity_id']}"
    if event_name == "copy_request_id" and properties.get("request_id"):
        return f"{module or 'log'} · copy_request_id · {properties['request_id']}"
    entity = properties.get("entity_type") or properties.get("business_type")
    if module and entity:
        return f"{module} · {event_name} · {entity}"
    if module:
        return f"{module} · {event_name}"
    return event_name


def sanitize_metadata(value: dict[str, Any]) -> dict[str, Any]:
    sanitized: dict[str, Any] = {}
    for key, item in value.items():
        normalized = str(key).lower()
        if normalized in SENSITIVE_KEYS:
            sanitized[key] = "******"
            continue
        if isinstance(item, dict):
            sanitized[key] = sanitize_metadata(item)
        elif isinstance(item, list):
            sanitized[key] = [sanitize_metadata(x) if isinstance(x, dict) else x for x in item[:20]]
        elif isinstance(item, str):
            sanitized[key] = truncate_text(item, 300)
        else:
            sanitized[key] = item
    return sanitized


def safe_json_dumps(value: dict[str, Any], *, pretty: bool = False) -> str:
    text = json.dumps(
        value,
        ensure_ascii=False,
        indent=2 if pretty else None,
        sort_keys=pretty,
        default=str,
    )
    return truncate_text(text, 4000) or "{}"


def parse_metadata(value: str | None) -> dict[str, Any]:
    if not value:
        return {}
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return {"metadata_parse_error": "metadata JSON 解析失败", "raw_summary": truncate_text(value, 500)}
    return parsed if isinstance(parsed, dict) else {"value": parsed}


def build_request_snapshot(record: LogRecord, metadata: dict[str, Any]) -> RequestSnapshotData | None:
    parse_error = metadata.get("metadata_parse_error")
    snapshot = metadata.get("request_snapshot")
    if isinstance(snapshot, dict):
        return RequestSnapshotData(
            request=RequestSnapshotRequestData(**_dict_value(snapshot.get("request"))),
            input=RequestSnapshotInputData(**_dict_value(snapshot.get("input"))),
            resource=RequestSnapshotResourceData(**_dict_value(snapshot.get("resource"))),
            response=RequestSnapshotResponseData(**_dict_value(snapshot.get("response"))),
            actor=RequestSnapshotActorData(**_dict_value(snapshot.get("actor"))),
            timing=RequestSnapshotTimingData(**_dict_value(snapshot.get("timing"))),
            raw_json=safe_json_dumps(snapshot, pretty=True),
            parse_error=str(parse_error) if parse_error else None,
        )
    if record.log_type != "request" and not parse_error:
        return None
    fallback = {
        "request": {
            "method": record.method,
            "path": record.path,
            "route_template": "unknown",
            "route_match_status": "unknown",
            "request_id": record.request_id,
            "client_request_id": record.client_request_id,
        },
        "input": {
            "query": {},
            "body_schema_summary": {},
            "redaction_summary": {"policy": "unavailable", "stored_raw_body": False},
        },
        "resource": {"resource_type": None, "resource_id": None, "id_source": "unavailable"},
        "response": {
            "status_code": record.status_code,
            "error_code": record.error_code,
            "duration_ms": record.duration_ms,
            "result": record.result,
            "error_summary": record.error_code,
        },
        "actor": {
            "actor_user_id": record.actor_user_id,
            "actor_username": record.actor_username,
            "actor_role": record.actor_role,
            "client_type": record.client_type,
            "ip_summary": record.ip_address_masked,
            "user_agent_summary": record.user_agent_summary,
        },
        "timing": {"environment": None, "started_at": None, "finished_at": record.created_at},
    }
    return RequestSnapshotData(
        request=RequestSnapshotRequestData(**fallback["request"]),
        input=RequestSnapshotInputData(**fallback["input"]),
        resource=RequestSnapshotResourceData(**fallback["resource"]),
        response=RequestSnapshotResponseData(**fallback["response"]),
        actor=RequestSnapshotActorData(**fallback["actor"]),
        timing=RequestSnapshotTimingData(**fallback["timing"]),
        raw_json=safe_json_dumps(fallback, pretty=True),
        parse_error=str(parse_error) if parse_error else "request_snapshot_missing",
    )


def _dict_value(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def mask_ip(value: str | None) -> str | None:
    if not value:
        return None
    if "." in value:
        parts = value.split(".")
        if len(parts) == 4:
            return ".".join(parts[:2] + ["*", "*"])
    if ":" in value:
        return value[:8] + "::****"
    return "******"


def truncate_text(value: str | None, limit: int) -> str | None:
    if value is None:
        return None
    text_value = str(value)
    if len(text_value) <= limit:
        return text_value
    return text_value[: limit - 3] + "..."


def today_start_utc() -> str:
    now = datetime.now(UTC)
    return now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
