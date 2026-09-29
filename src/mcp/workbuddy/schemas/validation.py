"""Pydantic validation for the published MCP input contract."""

from typing import Any, Literal

from pydantic import ConfigDict, Field, create_model

from src.mcp.workbuddy.schemas.tools import tool_schemas


def _model(name: str, schema: dict):
    fields = {}
    required = schema.get("required", [])
    for key, spec in schema.get("properties", {}).items():
        kind = {"string": str, "integer": int, "boolean": bool, "object": dict}[spec["type"]]
        if "enum" in spec:
            kind = Literal[tuple(spec["enum"])]
        constraints = {target: spec[source] for source, target in (
            ("minimum", "ge"), ("maximum", "le"), ("minLength", "min_length"),
            ("maxLength", "max_length"),
        ) if source in spec}
        fields[key] = (kind, Field(... if key in required else spec.get("default", None), **constraints))
    return create_model(name, __config__=ConfigDict(extra="forbid", strict=True), **fields)


MODELS = {tool["name"]: _model(tool["name"], tool["inputSchema"]) for tool in tool_schemas(True)}


def validate_arguments(name: str, args: dict[str, Any]) -> dict[str, Any]:
    return MODELS[name].model_validate(args).model_dump(exclude_unset=True)
