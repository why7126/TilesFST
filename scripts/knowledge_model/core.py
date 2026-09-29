"""安全加载、格式校验与本体语义验证；不执行模型中的业务表达式。"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

VERSION = "0.1.0"


class KnowledgeError(ValueError):
    """只携带脱敏的错误码和仓库内定位。"""

    def __init__(self, code: str, location: str = "", details=None):
        self.code = code
        self.location = location
        self.details = details
        super().__init__(f"{code}: {location}" if location else code)


class UniqueLoader(yaml.SafeLoader):
    pass


def _mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, (str, int)) or key in result:
            raise KnowledgeError("duplicate_or_invalid_key")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def safe_load(raw: str | bytes) -> Any:
    try:
        if len(raw) > 2097152: raise KnowledgeError("yaml_size_limit")
        if any(isinstance(event, yaml.AliasEvent) for event in yaml.parse(raw)):
            raise KnowledgeError("yaml_alias_forbidden")
        value = yaml.load(raw, Loader=UniqueLoader)
        # Reject recursive aliases and non-JSON types (including implicit timestamps).
        json.dumps(value, allow_nan=False)
        return value
    except KnowledgeError:
        raise
    except (yaml.YAMLError, ValueError, TypeError, RecursionError) as exc:
        raise KnowledgeError("invalid_yaml") from exc


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def byte_hash(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def path_in(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or "\\" in relative:
        raise KnowledgeError("invalid_path")
    pure = PurePosixPath(relative)
    if pure.is_absolute() or any(p in {"..", ".git"} for p in pure.parts):
        raise KnowledgeError("unsafe_path")
    root = root.resolve()
    p = root.joinpath(*pure.parts)
    if not p.resolve().is_relative_to(root):
        raise KnowledgeError("path_escape")
    # Reject all symlink components; avoids later writes through alias paths.
    current = root
    for part in pure.parts:
        current /= part
        if current.is_symlink():
            raise KnowledgeError("symlink_path")
    return p


def identifier(value: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.:-]*", value):
        raise KnowledgeError("invalid_identifier")
    return value


def check_structure(value, schema: dict, location="document"):
    """项目格式契约的显式子集，未知关键字失败，不声称支持完整JSON Schema。"""
    allowed = {"type", "required", "properties", "items", "enum", "additionalProperties"}
    if set(schema) - allowed:
        raise KnowledgeError("unsupported_schema_keyword", location)
    types = {"object": dict, "array": list, "string": str, "boolean": bool, "integer": int, "number": (int, float)}
    kind = schema.get("type")
    if kind and (kind not in types or not isinstance(value, types[kind]) or (kind in {"integer", "number"} and isinstance(value, bool))):
        raise KnowledgeError("schema_type", location)
    if "enum" in schema and value not in schema["enum"]:
        raise KnowledgeError("schema_enum", location)
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                raise KnowledgeError("schema_required", f"{location}.{key}")
        props = schema.get("properties", {})
        for key, child in value.items():
            if key in props:
                check_structure(child, props[key], f"{location}.{key}")
            elif schema.get("additionalProperties") is False:
                raise KnowledgeError("schema_unknown_field", f"{location}.{key}")
    if isinstance(value, list) and "items" in schema:
        for i, child in enumerate(value):
            check_structure(child, schema["items"], f"{location}[{i}]")


def condition_valid(node):
    if not isinstance(node, dict) or node.get("op") not in {"eq", "in", "exists", "all"}:
        raise KnowledgeError("unsupported_condition")
    if node["op"] == "all":
        if set(node) != {"op", "conditions"} or not isinstance(node["conditions"], list) or not node["conditions"]:
            raise KnowledgeError("invalid_condition")
        for child in node["conditions"]:
            condition_valid(child)
    else:
        required = {"op", "field"} | ({"value"} if node["op"] in {"eq", "in"} else set())
        if set(node) != required or not isinstance(node["field"], str):
            raise KnowledgeError("invalid_condition")
        if node["op"] == "in" and not isinstance(node["value"], list):
            raise KnowledgeError("invalid_condition")


def matches(node, context):
    condition_valid(node)
    if node["op"] == "all":
        values = [matches(c, context) for c in node["conditions"]]
        return False if False in values else None if None in values else True
    if node["field"] not in context:
        return None
    value = context[node["field"]]
    if node["op"] == "exists":
        return value is not None
    return value == node["value"] if node["op"] == "eq" else value in node["value"]


class Model:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.base = "knowledge-model/"
        self.registry = self.read("registry.yaml")
        self.schema = self.read("schema/knowledge-model.schema.yaml")
        self.types = {}
        self.relations = {}
        self.elements = {}
        self.files = {}
        for rel in self.registry["model_files"]:
            doc = self.read(rel)
            check_structure(doc, self.schema["model"])
            if doc["schema_version"] != self.registry["schema_version"]:
                raise KnowledgeError("schema_version", rel)
            self.files[rel] = doc
            for item in doc.get("types", []):
                self._add(self.types, item, rel)
            for item in doc.get("relation_types", []):
                self._add(self.relations, item, rel)
            for item in doc.get("elements", []):
                structural = {**item, "type": item["type"][0]} if isinstance(item.get("type"), list) and item["type"] else item
                check_structure(structural, self.schema["element"], rel)
                self._add(self.elements, item, rel)
            if doc["coverage"] == "out_of_scope" and (not doc.get("reason") or doc.get("elements")):
                raise KnowledgeError("coverage_reason", rel)
            if doc["coverage"] == "covered" and not any(doc.get(k) for k in ("elements", "types", "relation_types")):
                raise KnowledgeError("empty_coverage", rel)
        versions = self.registry["versions"]
        if versions not in self.registry["compatible_versions"]:
            raise KnowledgeError("incompatible_versions")
        for rel, doc in self.files.items():
            key = "meta" if doc["model_type"] == "META" else "development" if doc["model_type"] == "DEVELOPMENT" else "domain"
            if doc["version"] != versions[key]:
                raise KnowledgeError("model_version", rel)
        for name, item in self.types.items():
            self.ancestors(name)  # Includes missing parents and cycles.
            for field, target in item.get("refs", {}).items():
                if not target or any(t not in self.types for t in target):
                    raise KnowledgeError("undefined_ref_type", f"{name}.{field}")
        for name, rel in self.relations.items():
            if any(t not in self.types for t in rel["subject_types"] + rel["object_types"]):
                raise KnowledgeError("undefined_relation_type", name)
        meta = self.read("ontology/meta-ontology.yaml")["model_types"]
        for rel, document in self.files.items():
            if document["model_type"] not in meta: raise KnowledgeError("undefined_model_type", rel)
            expected = meta[document["model_type"]]
            for item in document.get("elements", []):
                if expected and not self.is_type(item["type"], expected): raise KnowledgeError("model_element_type", rel)
        self.validate_elements(list(self.elements.values()), domain=True)

    def read(self, relative):
        p = path_in(self.root, self.base + relative)
        try:
            return safe_load(p.read_bytes())
        except OSError as exc:
            raise KnowledgeError("missing_model_file", relative) from exc

    def _add(self, collection, item, rel):
        name = identifier(item["id"])
        if name in collection:
            raise KnowledgeError("duplicate_id", name)
        collection[name] = item

    def ancestors(self, name, chain=()):
        if isinstance(name, list):
            if not name: raise KnowledgeError("empty_type")
            return set().union(*(self.ancestors(t, chain) for t in name))
        identifier(name)
        if name not in self.types:
            raise KnowledgeError("unknown_type", name)
        if name in chain:
            raise KnowledgeError("inheritance_cycle", name)
        result = {name}
        for parent in self.types[name].get("parents", []):
            result |= self.ancestors(parent, (*chain, name))
        return result

    def is_type(self, actual, expected):
        return bool(self.ancestors(actual).intersection(expected))

    def validate_elements(self, elements, *, domain=False):
        index = {} if domain else dict(self.elements)
        seen = set()
        for item in elements:
            structural = {**item, "type": item["type"][0]} if isinstance(item.get("type"), list) and item["type"] else item
            check_structure(structural, self.schema["element"])
            name = identifier(item["id"])
            if name in seen or (not domain and name in index):
                raise KnowledgeError("duplicate_id", name)
            seen.add(name)
            index[name] = item
        for item in elements:
            name, kind = item["id"], item["type"]
            if item["layer"] != ("domain" if domain else "fact"):
                raise KnowledgeError("layer_mismatch", name)
            ancestors = self.ancestors(kind)
            for type_id in ancestors:
                definition = self.types[type_id]
                for attr, typ in definition.get("attributes", {}).items():
                    if attr in item.get("attributes", {}):
                        check_structure(item["attributes"][attr], {"type": typ}, f"{name}.{attr}")
                if any(attr not in item.get("attributes", {}) for attr in definition.get("required", [])):
                    raise KnowledgeError("missing_attribute", name)
                if domain and any(not item.get("refs", {}).get(field) for field in definition.get("domain_required_refs", [])):
                    raise KnowledgeError("missing_required_reference", name)
                for field, targets in definition.get("refs", {}).items():
                    refs = item.get("refs", {}).get(field, [])
                    if not isinstance(refs, list): raise KnowledgeError("reference_shape", name + "." + field)
                    for ref in refs:
                        if ref not in index or not self.is_type(index[ref]["type"], targets):
                            raise KnowledgeError("reference_type", f"{name}.{field}: expected {targets}")
                        if index[ref]["layer"] != item["layer"] and not definition.get("allow_domain_refs", False):
                            raise KnowledgeError("reference_layer", f"{name}.{field}")
            allowed_attributes = {f for a in ancestors for f in self.types[a].get("attributes", {})}
            if set(item.get("attributes", {})) - allowed_attributes: raise KnowledgeError("undefined_attribute", name)
            allowed_refs = {f for a in ancestors for f in self.types[a].get("refs", {})}
            if set(item.get("refs", {})) - allowed_refs:
                raise KnowledgeError("undefined_ref_field", name)
            for ref in item.get("premise_refs", []):
                if ref not in index:
                    raise KnowledgeError("missing_premise", name)
                if item.get("review_status") == "confirmed" and index[ref].get("review_status") != "confirmed":
                    raise KnowledgeError("unconfirmed_premise", name)
            source = item.get("source", {})
            if not source.get("path") or not source.get("locator"):
                raise KnowledgeError("missing_source", name)
            path_in(self.root, source["path"])
            if domain:
                p = path_in(self.root, source["path"])
                if not p.is_file(): raise KnowledgeError("missing_source_file", name)
                if source["locator"] not in p.read_text(): raise KnowledgeError("missing_locator", name)
            if not domain and (not re.fullmatch(r"[0-9a-f]{40,64}", source.get("git_commit", "")) or not re.fullmatch(r"[0-9a-f]{64}", source.get("sha256", ""))):
                raise KnowledgeError("missing_revision", name)
            if "precondition" in item.get("attributes", {}): condition_valid(item["attributes"]["precondition"])
            if "condition" in item:
                condition_valid(item["condition"])
            if item.get("effect") not in {None, "allow", "deny"}:
                raise KnowledgeError("invalid_effect", name)
            if item.get("effect") and (not item.get("condition") or not item.get("scope")):
                raise KnowledgeError("missing_condition", name)
            # Typed bindings for templates, action input and event payload.
            for field, target_field in (("template", "parameters"), ("behavior", "parameters"), ("event", "payload")):
                for ref in item.get("refs", {}).get(field, []):
                    expected = index[ref].get("attributes", {}).get(target_field, {})
                    actual = item.get("attributes", {}).get("bindings", {})
                    if set(actual) != set(expected) or any(actual[k] != expected[k] for k in expected):
                        raise KnowledgeError("binding_contract", name)
        return index

    def validate_graph(self, entities, relations):
        index = self.validate_elements(entities)
        seen = set()
        for edge in relations:
            check_structure(edge, self.schema["relation"])
            if edge["id"] in seen:
                raise KnowledgeError("duplicate_relation", edge["id"])
            seen.add(edge["id"])
            kind = self.relations.get(edge["predicate"])
            if not kind:
                raise KnowledgeError("unknown_relation", edge["id"])
            for end, types in (("subject", "subject_types"), ("object", "object_types")):
                ref = edge[end]
                if ref not in index or not self.is_type(index[ref]["type"], kind[types]):
                    raise KnowledgeError("relation_type", edge["id"])
            if index[edge["subject"]]["layer"] != index[edge["object"]]["layer"] and not kind.get("cross_layer", False):
                raise KnowledgeError("relation_layer", edge["id"])
            source = edge["source"]
            path_in(self.root, source["path"])
            if not source.get("locator") or not re.fullmatch(r"[a-f0-9]{40,64}", source.get("git_commit", "")) or not re.fullmatch(r"[a-f0-9]{64}", source.get("sha256", "")):
                raise KnowledgeError("missing_revision", edge["id"])
        for pred, definition in self.relations.items():
            edges = [e for e in relations if e["predicate"] == pred]
            for ent in entities:
                if not self.is_type(ent["type"], definition["subject_types"]):
                    continue
                count = len({e["object"] for e in edges if e["subject"] == ent["id"]})
                minimum = definition.get("min", 0)
                if ent.get("attributes", {}).get("legacy") and definition.get("legacy_min") is not None:
                    minimum = definition["legacy_min"]
                if count < minimum or count > definition.get("max", 10**9):
                    raise KnowledgeError("cardinality", ent["id"] + "." + pred)
            if definition.get("acyclic"):
                adjacency = {}
                for edge in edges:
                    adjacency.setdefault(edge["subject"], []).append(edge["object"])
                def visit(node, chain):
                    if node in chain:
                        raise KnowledgeError("relation_cycle", pred)
                    for target in adjacency.get(node, []):
                        visit(target, chain | {node})
                for node in adjacency:
                    visit(node, set())
        strong = [e for e in entities if e.get("effect") and e["review_status"] == "confirmed"]
        for i, a in enumerate(strong):
            for b in strong[i+1:]:
                if a.get("scope") == b.get("scope") and a.get("condition") == b.get("condition") and a["effect"] != b["effect"]:
                    raise KnowledgeError("rule_conflict", a["id"] + "," + b["id"], details=[{"id": e["id"], "source": e["source"]} for e in (a, b)])
        return {"entities": len(entities), "relations": len(relations), "rules": len(strong)}

    def dependency_hashes(self):
        paths = ["registry.yaml", "schema/knowledge-model.schema.yaml", *self.registry["model_files"], *self.registry.get("mapping_files", []), *self.registry.get("override_files", [])]
        return {self.base + rel: byte_hash(path_in(self.root, self.base + rel).read_bytes()) for rel in sorted(set(paths))}
