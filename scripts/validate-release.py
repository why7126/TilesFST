#!/usr/bin/env python3
"""Validate product release metadata and public announcement safety."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
import environment_tiered_evidence
RELEASES_DIR = ROOT / "releases"
PRODUCT_VERSION_FILE = ROOT / "src" / "shared" / "product-version.ts"
MINIAPP_PRODUCT_VERSION_FILES = (
    ROOT / "src" / "miniapp" / "utils" / "product-version.ts",
    ROOT / "src" / "miniapp" / "utils" / "product-version.js",
)
MINTLIFY_DIR = ROOT / "mintlify"
DEPLOYMENT_TARGETS = {"development", "production"}
RELEASE_STATUS_CLASSIFICATIONS = {
    "decision_missing",
    "prepare_evidence_missing",
    "publish_evidence_missing",
    "production_only_pending",
    "input_drift",
    "environment_unavailable",
    "scope_incomplete",
    "public_safety",
    "schema_invalid",
}

REQUIRED_GATES = (
    "openspec_archive",
    "tests",
    "orval",
    "docker_compose",
    "database_migration",
    "env_example",
    "product_version",
    "mintlify_preview",
)

IMAGE_GATES = (
    "image_prepare",
    "image_build",
)

IMPACT_KEYS = (
    "web_admin",
    "owner_web",
    "miniapp",
    "backend",
    "database",
    "object_storage",
    "docker",
)

SENSITIVE_PATTERNS = (
    re.compile(r"\bAPP_SECRET_KEY\s*=", re.I),
    re.compile(r"\bDATABASE_URL\s*=", re.I),
    re.compile(r"mysql(\+\w+)?://", re.I),
    re.compile(r"\bMINIO_(?:ACCESS|SECRET)_KEY\s*=", re.I),
    re.compile(r"\bAuthorization\s*:", re.I),
    re.compile(r"\bBearer\s+[A-Za-z0-9._-]+", re.I),
    re.compile(r"\bCookie\s*:", re.I),
    re.compile(r"\bpassword\s*=", re.I),
)
HEX_SHA256_PATTERN = re.compile(r"\b[a-f0-9]{64}\b", re.I)

NO_IMPACT_VALUES = {"", "none", "na", "n/a", "not_applicable", "not applicable", "无", "不涉及"}
MYSQL_EVIDENCE_PATTERNS = (
    re.compile(r"\bmysql\b", re.I),
    re.compile(r"schema\.mysql\.sql", re.I),
)
MYSQL_CHECK_PATTERNS = (
    re.compile(r"check-mysql-schema-drift\.py", re.I),
    re.compile(r"schema\s*drift", re.I),
    re.compile(r"information_schema", re.I),
    re.compile(r"mysql\s+smoke", re.I),
    re.compile(r"目标\s*mysql", re.I),
    re.compile(r"生产\s*mysql", re.I),
)
DATABASE_ROLLBACK_PATTERNS = (
    re.compile(r"rollback", re.I),
    re.compile(r"backup", re.I),
    re.compile(r"回滚"),
    re.compile(r"备份"),
)
DATABASE_GATE_EFFECTIVE_AT = "2026-07-21 00:00:00"
IMAGE_GATE_EFFECTIVE_AT = "2026-07-29 15:51:41"
USAGE_DOCS_GATE_EFFECTIVE_AT = "2026-08-01 10:35:08"
MINTLIFY_SITE_GATE_EFFECTIVE_AT = "2026-08-03 18:45:00"
RELEASE_TARGET_GATE_EFFECTIVE_AT = "2026-08-30 09:55:00"


def load_image_validator() -> Any:
    script = SCRIPTS_DIR / "validate-image-build.py"
    spec = importlib.util.spec_from_file_location("validate_image_build_script", script)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot load image validator: {script}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_usage_docs_validator() -> Any:
    script = SCRIPTS_DIR / "validate-usage-docs.py"
    spec = importlib.util.spec_from_file_location("validate_usage_docs_script", script)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot load usage docs validator: {script}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_upgrade_validator() -> Any:
    script = SCRIPTS_DIR / "validate-release-upgrade.py"
    spec = importlib.util.spec_from_file_location("validate_release_upgrade_script", script)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot load upgrade validator: {script}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"missing file: {path}") from None
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON {path}: {exc}") from None
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def extract_product_version(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"PRODUCT_VERSION\s*=\s*['\"]([^'\"]+)['\"]", text)
    if not match:
        raise ValueError(f"PRODUCT_VERSION not found in {path}")
    return match.group(1)


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def product_version_file_candidates(product_version_file: Path) -> tuple[Path, ...]:
    resolved = product_version_file.resolve()
    candidates = [resolved]
    if resolved == PRODUCT_VERSION_FILE.resolve():
        candidates.extend(path.resolve() for path in MINIAPP_PRODUCT_VERSION_FILES if path.exists())
    return tuple(candidates)


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def gate_is_passing(name: str, gate: Any, errors: list[str]) -> None:
    if not isinstance(gate, dict):
        errors.append(f"gate {name} must be an object")
        return
    status = str(gate.get("status", "")).lower()
    if status == "pass":
        require(bool(gate.get("evidence")), f"gate {name} status pass requires evidence", errors)
        return
    if status == "na":
        require(bool(gate.get("rationale")), f"gate {name} status na requires rationale", errors)
        return
    errors.append(f"gate {name} must be pass or na, got {status or '<missing>'}")


def impact_value_requires_gate(value: Any) -> bool:
    return str(value or "").strip().lower() not in NO_IMPACT_VALUES


def release_target_environment(data: dict[str, Any], override: str | None = None) -> str:
    if override:
        return override
    target = data.get("release_target")
    if isinstance(target, dict):
        value = str(target.get("environment") or "").strip().lower()
        if value in DEPLOYMENT_TARGETS:
            return value
    return "production"


def validate_release_target(data: dict[str, Any], errors: list[str]) -> None:
    target = data.get("release_target")
    if target is None:
        if str(data.get("release_time", "")) >= RELEASE_TARGET_GATE_EFFECTIVE_AT:
            errors.append("release_target is required for releases after dev/prod target governance")
        return
    if not isinstance(target, dict):
        errors.append("release_target must be an object")
        return
    environment = str(target.get("environment") or "").strip().lower()
    scope = str(target.get("deployment_scope") or "").strip().lower()
    require(environment in DEPLOYMENT_TARGETS, "release_target.environment must be development or production", errors)
    require(scope in DEPLOYMENT_TARGETS, "release_target.deployment_scope must be development or production", errors)
    require(bool(target.get("rationale")), "release_target.rationale is required", errors)


def evidence_gate_is_satisfied(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    status = str(value.get("status") or "").strip().lower()
    if status == "pass":
        return bool(value.get("evidence"))
    if status == "na":
        return bool(value.get("rationale"))
    return False


def validate_production_publish_gates(data: dict[str, Any], errors: list[str], *, stage: str, target_override: str | None = None) -> None:
    if stage != "publish" or release_target_environment(data, target_override) != "production":
        return
    if str(data.get("release_time", "")) < RELEASE_TARGET_GATE_EFFECTIVE_AT and data.get("release_target") is None:
        return
    production = data.get("production_deployment")
    if not isinstance(production, dict):
        errors.append("production release publish requires production_deployment evidence object")
        return
    for key in (
        "env_image_tag",
        "backup_confirmation",
        "public_api_consistency",
        "media_no_fallback",
        "runtime_smoke",
        "rollback_readiness",
    ):
        if key not in production:
            errors.append(f"production_deployment.{key} is required for production publish")
        elif not evidence_gate_is_satisfied(production[key]):
            errors.append(f"production_deployment.{key} must be pass with evidence or na with rationale")


def release_requires_image(data: dict[str, Any]) -> bool:
    explicit = data.get("image_required")
    if isinstance(explicit, bool):
        return explicit
    impact = data.get("impact_scope")
    if not isinstance(impact, dict):
        return False
    return any(impact_value_requires_gate(impact.get(key)) for key in ("backend", "database", "docker", "object_storage"))


def validate_database_impact_gate(data: dict[str, Any], errors: list[str]) -> None:
    impact = data.get("impact_scope")
    gates = data.get("gates")
    if not isinstance(impact, dict) or not isinstance(gates, dict):
        return
    if str(data.get("release_time", "")) < DATABASE_GATE_EFFECTIVE_AT:
        return
    if not impact_value_requires_gate(impact.get("database")):
        return

    gate = gates.get("database_migration")
    if not isinstance(gate, dict):
        return
    status = str(gate.get("status", "")).lower()
    if status != "pass":
        errors.append("database impact requires gate database_migration status pass")
        return

    evidence = str(gate.get("evidence", ""))
    require(
        any(pattern.search(evidence) for pattern in MYSQL_EVIDENCE_PATTERNS),
        "database impact requires database_migration evidence to mention MySQL or schema.mysql.sql",
        errors,
    )
    require(
        any(pattern.search(evidence) for pattern in MYSQL_CHECK_PATTERNS),
        "database impact requires MySQL schema drift or target MySQL smoke evidence",
        errors,
    )
    require(
        any(pattern.search(evidence) for pattern in DATABASE_ROLLBACK_PATTERNS),
        "database impact requires database rollback or backup evidence",
        errors,
    )


def expected_upgrade_sources(version: str) -> list[str]:
    upgrade_validator = load_upgrade_validator()
    sources = ["fresh"]
    try:
        previous = upgrade_validator.previous_version(version, ROOT)
    except Exception:
        previous = None
    if previous:
        sources.append(previous)
    return sources


def validate_upgrade_plan_gates(release_dir: Path, data: dict[str, Any], errors: list[str], *, stage: str, target_override: str | None = None) -> None:
    if stage != "publish":
        return
    if str(data.get("release_time", "")) < RELEASE_TARGET_GATE_EFFECTIVE_AT and data.get("release_target") is None:
        return
    version = str(data.get("version") or "")
    target = release_target_environment(data, target_override)
    upgrade_validator = load_upgrade_validator()
    for source in expected_upgrade_sources(version):
        target_plan_name = upgrade_validator.safe_plan_name(source, version, target)
        legacy_plan_name = upgrade_validator.safe_plan_name(source, version)
        target_plan_path = release_dir / "upgrade-plans" / target_plan_name
        legacy_plan_path = release_dir / "upgrade-plans" / legacy_plan_name
        plan_path = target_plan_path if target_plan_path.exists() else legacy_plan_path
        if not plan_path.exists():
            errors.append(f"release publish requires {target} upgrade plan: {target_plan_path}")
            continue
        try:
            plan = load_json(plan_path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        plan_target = str(plan.get("deployment_target") or "production").strip().lower()
        if plan_target != target:
            errors.append(f"upgrade plan {plan_path} deployment_target {plan_target} does not match release target {target}")
        errors.extend(f"{plan_path}: {error}" for error in upgrade_validator.validate_plan_data(plan))


def scan_public_safety(release_dir: Path, release_data: dict[str, Any], errors: list[str]) -> None:
    announcement_name = release_data.get("announcement", "announcement.mdx")
    announcement_path = release_dir / str(announcement_name)
    if not announcement_path.exists():
        errors.append(f"announcement file missing: {announcement_path}")
        return
    combined = json.dumps(release_data, ensure_ascii=False) + "\n" + announcement_path.read_text(encoding="utf-8")
    for pattern in SENSITIVE_PATTERNS:
        if pattern.search(combined):
            errors.append(f"public announcement or metadata contains sensitive pattern: {pattern.pattern}")


def validate_publish_announcement_stability(release_dir: Path, release_data: dict[str, Any], errors: list[str], *, stage: str) -> None:
    if stage != "publish":
        return
    announcement_name = release_data.get("announcement", "announcement.mdx")
    announcement_path = release_dir / str(announcement_name)
    if not announcement_path.exists():
        return
    text = announcement_path.read_text(encoding="utf-8")
    if HEX_SHA256_PATTERN.search(text):
        errors.append(
            "announcement.mdx must not embed final sha256 values at publish stage; "
            "reference image-manifest.json and the tarball .sha256 sidecar instead"
        )


def validate_mintlify_site_gate(release_dir: Path, data: dict[str, Any], errors: list[str], *, stage: str) -> None:
    if str(data.get("release_time", "")) < MINTLIFY_SITE_GATE_EFFECTIVE_AT:
        return
    usage_docs = data.get("usage_docs")
    if not isinstance(usage_docs, dict):
        return
    status = str(usage_docs.get("status", "")).lower()
    if status == "generated":
        mint_config = MINTLIFY_DIR / "docs.json"
        require(mint_config.exists(), f"Mintlify site config missing: {mint_config}", errors)
        manifest_path = release_dir / str(usage_docs.get("manifest") or "usage-docs/manifest.json")
        if manifest_path.exists():
            try:
                manifest = load_json(manifest_path)
            except ValueError as exc:
                errors.append(str(exc))
                return
            projection = manifest.get("site_projection")
            if not isinstance(projection, dict) or projection.get("status") != "synced":
                errors.append("usage_docs.status generated requires manifest.site_projection.status synced")
        gate = data.get("gates", {}).get("mintlify_preview") if isinstance(data.get("gates"), dict) else None
        if isinstance(gate, dict) and str(gate.get("status", "")).lower() == "pass":
            evidence = str(gate.get("evidence", ""))
            if "mintlify" not in evidence.lower() and "validate-usage-docs.py" not in evidence:
                errors.append("gate mintlify_preview evidence must mention Mintlify site validation or validate-usage-docs.py")
    if stage == "publish" and impact_value_requires_gate(data.get("impact_scope", {}).get("docker") if isinstance(data.get("impact_scope"), dict) else None):
        gate = data.get("gates", {}).get("docker_compose") if isinstance(data.get("gates"), dict) else None
        if isinstance(gate, dict) and str(gate.get("status", "")).lower() == "pass":
            evidence = str(gate.get("evidence", ""))
            if "docs-site" in evidence and "docker compose" not in evidence.lower():
                errors.append("docs-site release scope requires Docker Compose validation evidence")


def validate_image_gates(release_dir: Path, data: dict[str, Any], errors: list[str], *, stage: str) -> None:
    if str(data.get("release_time", "")) < IMAGE_GATE_EFFECTIVE_AT and "image_required" not in data:
        return
    image_required = release_requires_image(data)
    if "image_required" not in data:
        errors.append("image_required is required for image-governed releases")
        return
    if not image_required:
        require(bool(data.get("image_required_rationale")), "image_required false requires image_required_rationale", errors)
        return

    gates = data.get("gates")
    if not isinstance(gates, dict):
        return
    for name in IMAGE_GATES:
        require(name in gates, f"gate {name} is required when image_required is true", errors)
        if name in gates:
            gate_is_passing(name, gates[name], errors)

    plan_path = release_dir / str(data.get("image_plan", "image-build-plan.json"))
    manifest_path = release_dir / str(data.get("image_manifest", "image-manifest.json"))
    require(plan_path.exists(), f"image_required true requires image build plan: {plan_path}", errors)
    if stage == "publish":
        require(manifest_path.exists(), f"image_required true requires image manifest: {manifest_path}", errors)

    if plan_path.exists():
        image_validator = load_image_validator()
        errors.extend(image_validator.validate_plan(str(data.get("version")), release_dir, require_unblocked=False))
    if manifest_path.exists():
        image_validator = load_image_validator()
        errors.extend(image_validator.validate_manifest(str(data.get("version")), release_dir))


def validate_usage_docs_gates(release_dir: Path, data: dict[str, Any], errors: list[str]) -> None:
    if str(data.get("release_time", "")) < USAGE_DOCS_GATE_EFFECTIVE_AT and "usage_docs" not in data:
        return
    usage_docs = data.get("usage_docs")
    gates = data.get("gates")
    if not isinstance(usage_docs, dict):
        errors.append("usage_docs is required for usage-docs governed releases")
        return
    if not isinstance(gates, dict) or "usage_docs_preview" not in gates:
        errors.append("gate usage_docs_preview is required")
        return
    validator = load_usage_docs_validator()
    errors.extend(validator.validate_release_usage_docs(release_dir / "release.json"))


def validate_release(
    release_dir: Path,
    product_version_file: Path = PRODUCT_VERSION_FILE,
    *,
    stage: str = "prepare",
    target_override: str | None = None,
) -> list[str]:
    errors: list[str] = []
    if stage not in {"prepare", "publish"}:
        return [f"stage must be prepare or publish, got {stage}"]
    data = load_json(release_dir / "release.json")

    version = str(data.get("version", ""))
    require(bool(re.fullmatch(r"v\d+\.\d+\.\d+(?:[-.][A-Za-z0-9.]+)?", version)), "version must be SemVer-like, e.g. v0.1.0", errors)
    require(bool(re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", str(data.get("release_time", "")))), "release_time must be YYYY-MM-DD HH:mm:ss", errors)
    require(bool(data.get("owner")), "owner is required", errors)
    require(data.get("formal_scope_only") is True, "formal_scope_only must be true", errors)
    validate_release_target(data, errors)

    sprints = data.get("sprints")
    require(isinstance(sprints, list) and bool(sprints), "sprints must be a non-empty list", errors)
    for key in ("requirements", "bugs", "changes", "known_issues", "upgrade_steps"):
        require(isinstance(data.get(key), list), f"{key} must be a list", errors)
    require(isinstance(data.get("rollback"), dict), "rollback must be an object", errors)

    impact = data.get("impact_scope")
    require(isinstance(impact, dict), "impact_scope must be an object", errors)
    if isinstance(impact, dict):
        for key in IMPACT_KEYS:
            require(key in impact, f"impact_scope.{key} is required", errors)

    gates = data.get("gates")
    require(isinstance(gates, dict), "gates must be an object", errors)
    if isinstance(gates, dict):
        for name in REQUIRED_GATES:
            require(name in gates, f"gate {name} is required", errors)
            if name in gates:
                gate_is_passing(name, gates[name], errors)
    validate_image_gates(release_dir, data, errors, stage=stage)
    validate_usage_docs_gates(release_dir, data, errors)
    validate_mintlify_site_gate(release_dir, data, errors, stage=stage)
    validate_database_impact_gate(data, errors)
    validate_upgrade_plan_gates(release_dir, data, errors, stage=stage, target_override=target_override)
    validate_production_publish_gates(data, errors, stage=stage, target_override=target_override)
    target = release_target_environment(data, target_override)
    environment_report = environment_tiered_evidence.validate_release(ROOT, release_dir, target=target)
    errors.extend(
        f"environment tiered evidence: {blocker.file}:{blocker.line}: {blocker.message}"
        for blocker in environment_report.blockers
    )

    for candidate in product_version_file_candidates(product_version_file):
        product_version = extract_product_version(candidate)
        if version != product_version:
            errors.append(
                f"product version mismatch blocks {stage}: {display_path(candidate)} has {product_version}, "
                f"expected {version}; update PRODUCT_VERSION and rerun /image-prepare {version} && /image-build {version}"
            )

    mint_config = MINTLIFY_DIR / "docs.json" if MINTLIFY_DIR.exists() else release_dir.parent / "mint.json"
    require(mint_config.exists(), f"Mintlify config missing: {mint_config}", errors)
    scan_public_safety(release_dir, data, errors)
    validate_publish_announcement_stability(release_dir, data, errors, stage=stage)
    return errors


def classify_release_error(error: str) -> str:
    lowered = error.lower()
    if "environment tiered evidence" in lowered and "production_only_pending" in lowered:
        if "生产发布目标" in error or "production target" in lowered:
            return "publish_evidence_missing"
        return "production_only_pending"
    if "environment tiered evidence" in lowered and ("devtools" in lowered or "development" in lowered or "开发环境" in error):
        return "environment_unavailable"
    if "pending_confirmation" in lowered or "decision" in lowered:
        return "decision_missing"
    if "product version mismatch" in lowered or "product_version" in lowered or "product version" in lowered:
        return "prepare_evidence_missing"
    if "input hash drift" in lowered or "stable input drift" in lowered or "source_plan sha256" in lowered:
        return "input_drift"
    if "sensitive pattern" in lowered or "public announcement" in lowered:
        return "public_safety"
    if "openspec" in lowered or "archive" in lowered or "formal_scope" in lowered:
        return "scope_incomplete"
    if "missing" in lowered or "required" in lowered or "requires" in lowered or "must" in lowered:
        return "publish_evidence_missing"
    return "schema_invalid"


def release_status_item(
    *,
    classification: str,
    phase: str,
    blocks_target: str,
    message: str,
    owner: str = "ai",
    current_evidence: str = "",
    safe_remediation: str = "",
    rerun_check: str = "",
) -> dict[str, str]:
    if classification not in RELEASE_STATUS_CLASSIFICATIONS:
        classification = "schema_invalid"
    return {
        "classification": classification,
        "phase": phase,
        "blocks_target": blocks_target,
        "message": message,
        "owner": owner,
        "current_evidence": current_evidence,
        "safe_remediation": safe_remediation,
        "rerun_check": rerun_check,
    }


def expected_upgrade_plan_paths(release_dir: Path, version: str, target: str) -> list[dict[str, str]]:
    upgrade_validator = load_upgrade_validator()
    paths: list[dict[str, str]] = []
    for source in expected_upgrade_sources(version):
        plan_name = upgrade_validator.safe_plan_name(source, version, target)
        paths.append(
            {
                "from_version": source,
                "path": str(release_dir / "upgrade-plans" / plan_name),
                "command": f"/upgrade-plan --from {source} --to {version} --target {target}",
            }
        )
    return paths


def production_only_followups(data: dict[str, Any], target: str) -> list[dict[str, str]]:
    if target != "development":
        return []
    target_data = data.get("release_target") if isinstance(data.get("release_target"), dict) else {}
    if target_data.get("production_release_required") is False:
        return []
    production = data.get("production_deployment")
    keys = (
        "env_image_tag",
        "backup_confirmation",
        "public_api_consistency",
        "media_no_fallback",
        "runtime_smoke",
        "rollback_readiness",
    )
    missing = [key for key in keys if not isinstance(production, dict) or not evidence_gate_is_satisfied(production.get(key))]
    if not missing:
        return []
    return [
        release_status_item(
            classification="production_only_pending",
            phase="production_publish",
            blocks_target="production",
            message=f"生产发布证据待补齐：{', '.join(missing)}",
            owner="operator",
            current_evidence="development release does not require production-only evidence",
            safe_remediation=f"准备生产发布时补齐 production_deployment，并生成 {release_target_environment(data)} 之外的 production upgrade plans",
            rerun_check="python scripts/validate-release.py --release-dir <release-dir> --stage publish --target production",
        )
    ]


def release_status(release_dir: Path, product_version_file: Path = PRODUCT_VERSION_FILE, *, target_override: str | None = None) -> dict[str, Any]:
    try:
        data = load_json(release_dir / "release.json")
    except ValueError as exc:
        return {
            "release_dir": str(release_dir),
            "version": release_dir.name,
            "target": target_override or "unknown",
            "phase": "missing_release",
            "publish_ready": False,
            "next_command": "暂无可推进下一步",
            "blocking_decisions": [],
            "blocking_evidence": [
                release_status_item(
                    classification="schema_invalid",
                    phase="propose",
                    blocks_target=target_override or "unknown",
                    message=str(exc),
                    safe_remediation=f"/release-propose {release_dir.name}",
                    rerun_check=f"python scripts/validate-release.py --release-dir {release_dir}",
                )
            ],
            "production_followups": [],
            "default_upgrade_paths": [],
        }

    version = str(data.get("version") or release_dir.name)
    target = release_target_environment(data, target_override)
    prepare_errors = validate_release(release_dir, product_version_file, stage="prepare", target_override=target_override)
    publish_errors = validate_release(release_dir, product_version_file, stage="publish", target_override=target_override)
    blocking_decisions: list[dict[str, str]] = []
    blocking_evidence: list[dict[str, str]] = []

    usage_docs = data.get("usage_docs")
    if isinstance(usage_docs, dict) and str(usage_docs.get("status") or "").lower() == "pending_confirmation":
        blocking_decisions.append(
            release_status_item(
                classification="decision_missing",
                phase="prepare",
                blocks_target=target,
                message="usage docs 是否生成仍待确认",
                owner="operator",
                current_evidence="release.json usage_docs.status=pending_confirmation",
                safe_remediation=(
                    f"生成：/usage-docs-generate {version}；"
                    f"跳过：python scripts/generate-usage-docs.py {version} --skip --confirmed-by operator --rationale '<reason>'"
                ),
                rerun_check=f"python scripts/validate-release.py --release-dir releases/{version} --stage prepare",
            )
        )

    for error in prepare_errors:
        if "usage_docs" in error and blocking_decisions:
            continue
        blocking_evidence.append(
            release_status_item(
                classification=classify_release_error(error),
                phase="prepare",
                blocks_target=target,
                message=error,
                current_evidence=f"python scripts/validate-release.py --release-dir releases/{version} --stage prepare",
                safe_remediation="按错误指向的 gate 补齐证据或修复 release.json",
                rerun_check=f"python scripts/validate-release.py --release-dir releases/{version} --stage prepare",
            )
        )

    default_paths = expected_upgrade_plan_paths(release_dir, version, target)
    upgrade_missing = [item for item in default_paths if not Path(item["path"]).exists()]
    for item in upgrade_missing:
        blocking_evidence.append(
            release_status_item(
                classification="publish_evidence_missing",
                phase="upgrade",
                blocks_target=target,
                message=f"缺少默认升级计划：{Path(item['path']).name}",
                current_evidence=f"expected target upgrade plan for {item['from_version']} -> {version}",
                safe_remediation=item["command"],
                rerun_check=f"python scripts/validate-release-upgrade.py validate-plan --plan {item['path']}",
            )
        )

    if not prepare_errors:
        for error in publish_errors:
            if any(Path(item["path"]).name in error for item in upgrade_missing):
                continue
            blocking_evidence.append(
                release_status_item(
                    classification=classify_release_error(error),
                    phase="publish",
                    blocks_target=target,
                    message=error,
                    current_evidence=f"python scripts/validate-release.py --release-dir releases/{version} --stage publish",
                    safe_remediation="按错误指向的 publish gate 补齐证据",
                    rerun_check=f"python scripts/validate-release.py --release-dir releases/{version} --stage publish",
                )
            )

    image_required = release_requires_image(data)
    publish_ready = not blocking_decisions and not blocking_evidence and not publish_errors
    if blocking_decisions:
        phase = "decision_blocked"
        next_command = "暂无可推进下一步"
    elif prepare_errors:
        phase = "prepare_blocked"
        next_command = "暂无可推进下一步"
    elif image_required and not (release_dir / str(data.get("image_manifest", "image-manifest.json"))).exists():
        phase = "image_pending"
        next_command = f"/image-build {version}"
    elif upgrade_missing:
        phase = "upgrade_pending"
        next_command = upgrade_missing[0]["command"]
    elif publish_errors:
        phase = "publish_blocked"
        next_command = "暂无可推进下一步"
    elif isinstance(data.get("publish_confirmation"), dict):
        phase = "published"
        next_command = "暂无可推进下一步"
    else:
        phase = "publish_ready"
        next_command = f"/release-publish {version} --target {target}"

    return {
        "release_dir": str(release_dir),
        "version": version,
        "target": target,
        "phase": phase,
        "publish_ready": publish_ready,
        "next_command": next_command,
        "blocking_decisions": blocking_decisions,
        "blocking_evidence": blocking_evidence,
        "production_followups": production_only_followups(data, target),
        "default_upgrade_paths": default_paths,
    }


def print_release_status(status: dict[str, Any], *, json_output: bool = False) -> None:
    if json_output:
        print(json.dumps(status, ensure_ascii=False, indent=2))
        return
    print("## Release Status")
    print()
    print(f"Version: {status['version']}")
    print(f"Target: {status['target']}")
    print(f"Phase: {status['phase']}")
    print(f"Publish ready: {'yes' if status['publish_ready'] else 'no'}")
    print(f"Next command: {status['next_command']}")
    print(f"Blocking decisions: {len(status['blocking_decisions'])}")
    print(f"Blocking evidence: {len(status['blocking_evidence'])}")
    print(f"Production follow-ups: {len(status['production_followups'])}")
    if status["blocking_decisions"]:
        print()
        print("Decision blockers:")
        for item in status["blocking_decisions"]:
            print(f"- [{item['classification']}] {item['message']} -> {item['safe_remediation']}")
    if status["blocking_evidence"]:
        print()
        print("Evidence blockers:")
        for item in status["blocking_evidence"]:
            print(f"- [{item['classification']}] {item['message']} -> {item['safe_remediation']}")
    if status["production_followups"]:
        print()
        print("Production-only follow-ups:")
        for item in status["production_followups"]:
            print(f"- [{item['classification']}] {item['message']}")
    if status["default_upgrade_paths"]:
        print()
        print("Default upgrade paths:")
        for item in status["default_upgrade_paths"]:
            marker = "exists" if Path(item["path"]).exists() else "missing"
            print(f"- {item['from_version']} -> {status['version']} ({marker}): {item['command']}")


def release_dirs_from_args(path: str | None) -> list[Path]:
    if path:
        return [Path(path).resolve()]
    if not RELEASES_DIR.exists():
        return []
    return sorted(p for p in RELEASES_DIR.iterdir() if p.is_dir() and re.fullmatch(r"v\d+\.\d+\.\d+(?:[-.][A-Za-z0-9.]+)?", p.name))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate product release metadata and announcement source.")
    parser.add_argument("--release-dir", help="Release directory such as releases/v0.1.0")
    parser.add_argument("--product-version-file", default=str(PRODUCT_VERSION_FILE))
    parser.add_argument(
        "--stage",
        choices=("prepare", "publish"),
        default="prepare",
        help="Validation stage. prepare requires a valid image plan; publish also requires a manifest.",
    )
    parser.add_argument("--target", choices=sorted(DEPLOYMENT_TARGETS), help="Override release_target.environment for validation")
    parser.add_argument("--status", action="store_true", help="Print a read-only release status decision panel")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON for --status")
    args = parser.parse_args()

    release_dirs = release_dirs_from_args(args.release_dir)
    if not release_dirs:
        print("No versioned release directories found; templates only.")
        return 0

    all_errors: list[str] = []
    product_version_file = Path(args.product_version_file).resolve()
    if args.status:
        for release_dir in release_dirs:
            print_release_status(
                release_status(release_dir, product_version_file, target_override=args.target),
                json_output=args.json,
            )
        return 0

    for release_dir in release_dirs:
        errors = validate_release(release_dir, product_version_file, stage=args.stage, target_override=args.target)
        if errors:
            all_errors.append(f"{release_dir}:")
            all_errors.extend(f"  - {error}" for error in errors)

    if all_errors:
        print("Release validation failed:")
        for error in all_errors:
            print(error)
        return 1

    print(f"Release validation passed for {len(release_dirs)} release(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
