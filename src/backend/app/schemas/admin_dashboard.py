"""Schemas for admin dashboard summary."""

from __future__ import annotations

from pydantic import BaseModel


class AdminDashboardMetric(BaseModel):
    value: int
    description: str
    visible: bool = True


class AdminDashboardSummary(BaseModel):
    sku_total: AdminDashboardMetric
    brand_total: AdminDashboardMetric
    banner_total: AdminDashboardMetric
    user_total: AdminDashboardMetric
