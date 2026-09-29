"""固定Git来源、generation原子提交、生命周期恢复及版本快照。"""
from __future__ import annotations

import ast
import copy
import fcntl
import json
import os
import re
import subprocess
import tempfile
import time
from contextlib import contextmanager, nullcontext
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from .core import KnowledgeError, Model, VERSION, byte_hash, canonical, digest, identifier, path_in, safe_load


def now():
    return datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S")


def git(root, *args):
    p = subprocess.run(["git", "-C", str(root), *args], capture_output=True)
    if p.returncode:
        raise KnowledgeError("source_revision_pending")
    return p.stdout


def atomic(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".pending-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as out:
            out.write(data if isinstance(data, bytes) else canonical(data) + b"\n")
            out.flush()
            os.fsync(out.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def normalized_trace(raw):
    text = raw.decode("utf-8")
    text = re.sub(r"\n<!-- knowledge-model-sync:start -->.*?<!-- knowledge-model-sync:end -->\n", "", text, flags=re.S)
    text = re.sub(r"(?m)^updated_at:.*$", "updated_at: receipt-independent", text, count=1)
    return (text.rstrip() + "\n").encode()


class Store:
    def __init__(self, root: Path, *, load_model=True):
        self.root = root.resolve()
        self.model = Model(self.root) if load_model else None
        self.base = "knowledge-model/"
        self.runtime = "data/knowledge-model/"

    def path(self, rel):
        return path_in(self.root, rel)

    def read(self, rel):
        try:
            return safe_load(self.path(rel).read_bytes())
        except OSError as exc:
            raise KnowledgeError("missing_file", rel) from exc

    @contextmanager
    def lock(self, *, shared=False):
        lock = self.path(self.runtime + "writer.lock")
        lock.parent.mkdir(parents=True, exist_ok=True)
        with lock.open("a") as stream:
            fcntl.flock(stream, fcntl.LOCK_SH if shared else fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(stream, fcntl.LOCK_UN)

    def archived(self, change):
        identifier(change)
        root = self.path("openspec/archive")
        matches = sorted(root.glob("????-??-??-" + change)) if root.exists() else []
        if len(matches) != 1 or self.path("openspec/changes/" + change).exists():
            raise KnowledgeError("change_not_archived", change)
        return str(matches[0].relative_to(self.root))

    def source(self, rel, locator, commit):
        p = self.path(rel)
        raw = git(self.root, "show", commit + ":" + rel)
        # Symlinks in Git must not be interpreted as source files.
        if git(self.root, "ls-tree", commit, "--", rel).startswith(b"120000"):
            raise KnowledgeError("symlink_source", rel)
        try:
            if p.read_bytes() != raw:
                raise KnowledgeError("source_revision_pending", rel)
        except OSError as exc:
            raise KnowledgeError("source_revision_pending", rel) from exc
        if locator and locator not in raw.decode("utf-8"):
            raise KnowledgeError("missing_locator", rel)
        return raw, {"path": rel, "locator": locator or "file", "git_commit": commit, "sha256": byte_hash(raw)}

    def fixed_commit(self, revision):
        # No shell and no arbitrary git options; rev-parse resolves a commit only.
        if not re.fullmatch(r"[A-Za-z0-9_./~^+-]+", revision) or revision.startswith("-"):
            raise KnowledgeError("invalid_revision")
        return git(self.root, "rev-parse", "--verify", revision + "^{commit}").decode().strip()

    def current(self):
        pointer = self.path(self.base + "generated/current.yaml")
        if not pointer.exists():
            return {"parts": {}, "entities": [], "relations": []}, None
        key = self.read(self.base + "generated/current.yaml")["generation"]
        if not re.fullmatch(r"[a-f0-9]{64}", key):
            raise KnowledgeError("invalid_generation")
        rel = self.base + "generated/generations/" + key + "/"
        manifest = self.read(rel + "manifest.yaml")
        if manifest.get("generation") != key: raise KnowledgeError("generated_drift", "manifest")
        data = {}
        for name in ("entities", "relations", "parts"):
            raw = self.path(rel + name + ".yaml").read_bytes()
            if byte_hash(raw) != manifest["files"][name + ".yaml"]:
                raise KnowledgeError("generated_drift", name)
            data[name] = safe_load(raw)
        if digest(data) != key:
            raise KnowledgeError("generated_drift", "generation")
        return data, key

    def part(self, change, revision):
        archive = self.archived(change)
        commit = self.fixed_commit(revision)
        coverage = self.model.registry["coverage"][change]
        mapping = self.model.read(coverage["mapping"])
        sources = []
        raws = []
        for src in mapping["sources"]:
            raw, evidence = self.source(src["path"], src["locator"], commit)
            sources.append(evidence)
            raws.append(raw)
        # Metadata content is evidence, not copied. Trace is read before our receipt append.
        for name in ("proposal.md", "design.md", "tasks.md"):
            raw, evidence = self.source(archive + "/" + name, "", commit)
            if name == "tasks.md" and re.search(rb"^- \[ \]", raw, re.M):
                raise KnowledgeError("tasks_incomplete", change)
            sources.append(evidence)
        proposal_source = sources[-3]
        for document in self.model.files.values():
            for item in document.get("elements", []) + document.get("relation_types", []):
                if item.get("source"):
                    src = item["source"]
                    _, evidence = self.source(src["path"], src["locator"], commit)
                    if evidence not in sources: sources.append(evidence)
        trace_rel = archive + "/trace.md"
        trace_raw = git(self.root, "show", commit + ":" + trace_rel)
        if normalized_trace(trace_raw) != normalized_trace(self.path(trace_rel).read_bytes()):
            raise KnowledgeError("source_revision_pending", trace_rel)
        sources.append(dict(path=trace_rel, locator="file", git_commit=commit, sha256=byte_hash(normalized_trace(trace_raw)), normalization="knowledge-trace-v1"))
        trace = trace_raw.decode()
        issue_entities = {}
        issue_ids = sorted(set(re.findall(r"\b(?:REQ|BUG)-\d{4}(?:-[a-z0-9-]+)?", trace)))
        # Canonical Issue packages only, exact ID prefix; ambiguous matches fail closed.
        for issue in issue_ids:
            family = "requirements" if issue.startswith("REQ") else "bugs"
            matches = sorted(p for stage in ("review", "archive") for p in self.path("issues/" + family + "/" + stage).glob(issue + "*"))
            if len(matches) != 1:
                raise KnowledgeError("issue_archive_pending", issue)
            primary = matches[0] / ("requirement.md" if family == "requirements" else "bug.md")
            _, evidence = self.source(str(primary.relative_to(self.root)), "", commit)
            sources.append(evidence)
            issue_entities[matches[0].name] = dict(id="issue:" + matches[0].name, type="pd:Requirement" if family == "requirements" else "pd:Bug", layer="fact",
                                                 attributes={"name": matches[0].name}, source=evidence, review_status="confirmed", origin_change=change)
        # Rehearsal/acceptance is a committed input, distinct from actual release evidence.
        if self.path(archive + "/validation.md").exists():
            _, evidence = self.source(archive + "/validation.md", "", commit)
            sources.append(evidence)
        entities = []
        for entry in mapping["entities"]:
            selector = entry["selector"]
            raw = raws[entry["source_index"]]
            attrs = {"name": entry["id"]}
            if selector["kind"] == "openapi":
                document = json.loads(raw)
                operation = document.get("paths", {}).get(selector["path"], {}).get(selector["method"])
                if not operation or not operation.get("operationId"):
                    raise KnowledgeError("missing_api", entry["id"])
                attrs.update(operation_id=operation["operationId"], method=selector["method"], path=selector["path"])
            elif selector["kind"] == "python_symbol":
                symbols = [n.name for n in ast.walk(ast.parse(raw)) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
                if symbols.count(selector["name"]) > 1:
                    raise KnowledgeError("ambiguous_symbol", entry["id"])
                if selector["name"] not in symbols:
                    raise KnowledgeError("missing_symbol", entry["id"])
                attrs["symbol"] = selector["name"]
            elif selector["kind"] == "literal":
                # Literal labels are curated mapping data, never raw extracted paragraphs.
                attrs.update(entry.get("attributes", {}))
            else:
                raise KnowledgeError("unknown_selector", entry["id"])
            entities.append(dict(id=identifier(entry["id"]), type=entry["type"], layer="fact", attributes=attrs,
                                 source=sources[entry["source_index"]], review_status=entry.get("review_status", "candidate" if selector["kind"] == "literal" else "confirmed"), origin_change=change))
        change_entity = dict(id="change:" + change, type="pd:Change", layer="fact", attributes={"name": change}, source=proposal_source, review_status="confirmed", origin_change=change)
        entities.append(change_entity)
        relations = []
        for entry in mapping.get("relations", []):
            relations.append({**entry, "source": sources[entry.get("source_index", 0)], "origin_change": change})
        for entity in entities[:-1]:
            if entity["type"] == "pd:Artifact":
                relations.append(dict(id="edge:" + change + ":" + entity["id"], predicate="pd:evidencedBy", subject=change_entity["id"], object=entity["id"], source=entity["source"], origin_change=change))
        for issue_entity in issue_entities.values():
            entities.append(issue_entity)
            relations.append(dict(id="edge:" + change + ":" + issue_entity["id"], predicate="pd:tracks", subject=change_entity["id"], object=issue_entity["id"], source=issue_entity["source"], origin_change=change))
        # Confirmed domain rules are projected with explicit model provenance. No prose inference.
        for model_file, document in self.model.files.items():
            for item in document.get("elements", []):
                if not item.get("effect"):
                    continue
                raw, evidence = self.source("knowledge-model/" + model_file, item["id"], commit)
                sources.append(evidence)
                _, business_evidence = self.source(item["source"]["path"], item["source"]["locator"], commit)
                sources.append(business_evidence)
                rule = {k: copy.deepcopy(v) for k, v in item.items() if k not in {"refs", "source"}}
                rule.update(id="rule:" + change + ":" + item["id"], layer="fact", source=evidence, origin_change=change)
                entities.append(rule)
        overrides = self.model.read("overrides/reviewed.yaml")["overrides"]
        for override in overrides:
            if override["change"] != change:
                continue
            target = next((e for e in entities if e["id"] == override["target"]), None)
            if not target or override.get("reviewed_source_hash") != target["source"]["sha256"] or override.get("review_status") != "confirmed":
                raise KnowledgeError("override_stale", override["target"])
            target["attributes"].update(override["attributes"])
        deps = self.model.dependency_hashes()
        # Definitions and mappings must also belong to the recorded source commit.
        for rel in deps:
            self.source(rel, "", commit)
        for item in entities + relations:
            item["model_versions"] = self.model.registry["versions"]
            item["mapping_version"] = mapping["version"]
        # Cross-Change references are validated against the assembled candidate in sync.
        return dict(change=change, commit=commit, sources=sources, dependencies=deps,
                    extractor_version=VERSION, entities=entities, relations=relations)

    def verify_part(self, part):
        if part["dependencies"] != self.model.dependency_hashes():
            raise KnowledgeError("stale_model", part["change"])
        for src in part["sources"]:
            raw = self.path(src["path"]).read_bytes()
            if src.get("normalization") == "knowledge-trace-v1": raw = normalized_trace(raw)
            if byte_hash(raw) != src["sha256"]:
                raise KnowledgeError("stale_source", src["path"])
        if part["extractor_version"] != VERSION:
            raise KnowledgeError("stale_extractor")

    def receipt(self, change, value):
        identifier(change)
        # Values are constructed here; no exception text or source paragraphs persisted.
        atomic(self.path(self.runtime + "runs/" + change + ".json"), {**value, "recorded_at": now(), "phases": {"archive": "completed", "knowledge": value["status"], "trace": "recoverable"}})

    def record_trace(self, change, summary):
        archive = self.archived(change)
        trace = self.path(archive + "/trace.md")
        # A closed Sprint is immutable. Recovery remains in runtime receipts.
        frozen = self.path("iterations/archive")
        if frozen.exists() and any(change in p.read_text() for p in frozen.glob("sprint-*/sprint.yaml")):
            return
        text = trace.read_text()
        block = "\n<!-- knowledge-model-sync:start -->\n## 知识模型同步\n\n" + "\n".join(
            "- " + k + ": " + str(summary[k]) for k in ("status", "generation", "reason") if k in summary
        ) + "\n<!-- knowledge-model-sync:end -->\n"
        text = re.sub(r"\n<!-- knowledge-model-sync:start -->.*?<!-- knowledge-model-sync:end -->\n", "", text, flags=re.S)
        text = re.sub(r"(?m)^updated_at:.*$", "updated_at: " + now(), text, count=1)
        atomic(trace, (text.rstrip() + "\n" + block).encode())

    def record_unresolved(self, change, *, reason=None):
        path = self.path(self.base + "unresolved/sync-" + change + ".yaml")
        if reason:
            atomic(path, {"generator": "knowledge-sync", "items": [{"id": "sync:" + change, "change": change, "risk": "high", "status": "open", "reason": reason, "source": "knowledge-model/registry.yaml"}]})
        elif path.exists():
            value = safe_load(path.read_bytes())
            if value.get("generator") == "knowledge-sync":
                for item in value["items"]: item["status"] = "resolved"
                atomic(path, value)

    def sync(self, change, revision="HEAD", *, dry_run=False, fail_at=None):
        identifier(change)
        if change not in self.model.registry["coverage"]:
            return dict(status="out_of_scope", change=change, reason=self.model.registry["out_of_scope_reason"])
        # Tests inject failures through the Python API only, never the production CLI.
        try:
            with (nullcontext() if dry_run else self.lock()):
                self.model = Model(self.root)
                part = self.part(change, revision)
                state, previous = self.current()
                old_entities = {e["id"]: e for e in state["entities"]}
                state = copy.deepcopy(state)
                state["parts"][change] = part
                # Rebuild from per-Change ownership; shared conflicting IDs reject, never silently overwrite.
                state["entities"] = [e for key in sorted(state["parts"]) for e in state["parts"][key]["entities"]]
                state["relations"] = [e for key in sorted(state["parts"]) for e in state["parts"][key]["relations"]]
                self.model.validate_graph(state["entities"], state["relations"])
                for existing in state["parts"].values():
                    self.verify_part(existing)
                key = digest(state)
                summary = dict(status="synced", change=change, generation=key, idempotent=key == previous,
                               entities=len(part["entities"]), relations=len(part["relations"]), input_commit=part["commit"], run_id=change + ":" + key)
                new_entities = {e["id"]: e for e in state["entities"]}
                summary["diff"] = {"added": sorted(new_entities.keys() - old_entities.keys()), "removed": sorted(old_entities.keys() - new_entities.keys()),
                                   "changed": sorted(k for k in new_entities.keys() & old_entities.keys() if new_entities[k] != old_entities[k])}
                if dry_run:
                    return {**summary, "status": "dry_run"}
                if fail_at == "before_commit":
                    raise KnowledgeError("injected_before_commit")
                rel = self.base + "generated/generations/" + key + "/"
                target = self.path(rel)
                if not target.exists():
                    temp_parent = self.path(self.base + "generated/generations")
                    temp_parent.mkdir(parents=True, exist_ok=True)
                    with tempfile.TemporaryDirectory(prefix=".pending-", dir=temp_parent) as tmp:
                        files = {}
                        for name in ("entities", "relations", "parts"):
                            data = canonical(state[name]) + b"\n"
                            Path(tmp, name + ".yaml").write_bytes(data)
                            files[name + ".yaml"] = byte_hash(data)
                        Path(tmp, "manifest.yaml").write_bytes(canonical({"generation": key, "files": files}) + b"\n")
                        # Rename directory, then recreate temp so TemporaryDirectory cleanup is safe.
                        os.rename(tmp, target)
                        Path(tmp).mkdir()
                else:
                    expected_manifest = {"generation": key, "files": {name + ".yaml": byte_hash(canonical(state[name]) + b"\n") for name in ("entities", "relations", "parts")}}
                    if self.read(rel + "manifest.yaml") != expected_manifest: raise KnowledgeError("generated_drift", "manifest")
                    # Validate a pre-existing orphan generation before promoting it.
                    for name in ("entities", "relations", "parts"):
                        if self.path(rel + name + ".yaml").read_bytes() != canonical(state[name]) + b"\n":
                            raise KnowledgeError("generated_drift", name)
                self.verify_part(part)
                atomic(self.path(self.base + "generated/current.yaml"), {"generation": key})
                if fail_at == "after_commit":
                    raise KnowledgeError("injected_after_commit")
                self.record_unresolved(change)
                self.receipt(change, summary)
                self.record_trace(change, summary)
                return summary
        except (KnowledgeError, OSError, ValueError) as exc:
            code = exc.code if isinstance(exc, KnowledgeError) else "sync_io_or_parse_error"
            if not dry_run:
                failure = dict(status="failed", change=change, reason=code, recovery="retry-single-change")
                self.record_unresolved(change, reason=code)
                self.receipt(change, failure)
                try: self.record_trace(change, failure)
                except (KnowledgeError, OSError): pass
            if isinstance(exc, KnowledgeError):
                raise
            raise KnowledgeError(code) from exc

    def check(self, changes):
        state, generation = self.current()
        reports = []
        self.model.validate_graph(state["entities"], state["relations"])
        for change in changes:
            if change not in self.model.registry["coverage"]:
                reports.append(dict(change=change, status="out_of_scope", reason=self.model.registry["out_of_scope_reason"]))
                continue
            part = state["parts"].get(change)
            if not part:
                reports.append(dict(change=change, status="failed", reason="not_synced"))
                continue
            try:
                self.archived(change)
                self.verify_part(part)
                receipt_path = self.runtime + "runs/" + change + ".json"
                if self.path(receipt_path).exists() and self.read(receipt_path).get("status") == "failed":
                    raise KnowledgeError("receipt_pending", change)
                reports.append(dict(change=change, status="synced"))
            except (KnowledgeError, OSError) as exc:
                reports.append(dict(change=change, status="stale", reason=exc.code if isinstance(exc, KnowledgeError) else "missing_source"))
        unresolved = []
        for path in sorted(self.path(self.base + "unresolved").glob("*.yaml")):
            for item in safe_load(path.read_bytes()).get("items", []):
                if item.get("change") not in changes or item.get("status") in {"resolved", "dismissed"}: continue
                if item.get("risk") not in {"high", "low"} or not item.get("reason") or not item.get("source"):
                    raise KnowledgeError("invalid_unresolved")
                unresolved.append(item)
        failed = any(r["status"] not in {"synced", "out_of_scope"} for r in reports) or any(i["risk"] == "high" for i in unresolved)
        return dict(status="blocked" if failed else "pass", generation=generation, changes=reports,
                    unresolved=unresolved, warnings=[e["id"] for e in state["entities"] if e["review_status"] == "candidate"])

    def limits(self, files):
        limits = self.model.registry["limits"]
        if len(files) > limits["max_files"] or sum(len(x) for x in files.values()) > limits["max_bytes"] or any(len(x) > limits["max_file_bytes"] for x in files.values()):
            raise KnowledgeError("snapshot_limit")

    def release_data(self, release):
        identifier(release)
        if not re.fullmatch(r"v\d+\.\d+\.\d+(?:[-.][A-Za-z0-9.]+)?", release):
            raise KnowledgeError("invalid_release")
        data = self.read("releases/" + release + "/release.json")
        def ids(key):
            result = []
            for item in data.get(key, []):
                if isinstance(item, str): result.append(item)
                elif isinstance(item, dict):
                    value = item.get("id") or item.get("change_id") or item.get("sprint_id")
                    if not value: raise KnowledgeError("release_scope_invalid", key)
                    result.append(value)
                else: raise KnowledgeError("release_scope_invalid", key)
            return sorted(set(result))
        return data, {"product_version": release, "changes": ids("changes"), "sprints": ids("sprints")}

    def snapshot(self, release, *, prepare=False, locked=False):
        with (self.lock() if prepare and not locked else nullcontext()):
            data, scope = self.release_data(release)
            if data.get("knowledge_model") and data.get("publish_confirmation"):
                reference = data["knowledge_model"]
                if reference.get("manifest") != self.base + "snapshots/" + release + "/manifest.yaml": raise KnowledgeError("snapshot_reference_invalid")
                manifest = self.read(reference["manifest"])
                historical = {k: v for k, v in manifest.items() if k not in {"snapshot_id", "generated_at", "source_release"}}
                if digest(historical) != reference["snapshot_id"] or manifest.get("snapshot_id") != reference["snapshot_id"]:
                    raise KnowledgeError("snapshot_content_drift")
                if any(manifest.get(k) != v for k, v in scope.items()): raise KnowledgeError("snapshot_input_drift")
                for rel, raw in manifest["dependency_contents"].items():
                    if byte_hash(raw.encode()) != manifest["dependencies"][rel]: raise KnowledgeError("snapshot_dependency_drift")
                dest = self.base + "snapshots/" + release + "/"
                for name, expected in manifest["files"].items():
                    if name not in {"entities.yaml", "relations.yaml", "rules.yaml"} or byte_hash(self.path(dest + name).read_bytes()) != expected:
                        raise KnowledgeError("snapshot_content_drift")
                return {"status": "pass", "snapshot_id": reference["snapshot_id"], "manifest": reference["manifest"]}
            if self.model is None: self.model = Model(self.root)
            relevant = [c for c in scope["changes"] if c in self.model.registry["coverage"]]
            if not relevant and not data.get("knowledge_model"):
                return {"status": "out_of_scope"}
            report = self.check(relevant)
            if report["status"] != "pass":
                raise KnowledgeError("snapshot_sync_incomplete")
            state, generation = self.current()
            parts = {k: state["parts"][k] for k in relevant}
            entities = [e for k in sorted(parts) for e in parts[k]["entities"]]
            relations = [e for k in sorted(parts) for e in parts[k]["relations"]]
            self.model.validate_graph(entities, relations)
            rules = [e for e in entities if e.get("effect") and e["review_status"] == "confirmed"]
            files = {k + ".yaml": canonical(v) + b"\n" for k, v in {"entities": entities, "relations": relations, "rules": rules}.items()}
            stable = dict(**scope, knowledge_model_version=self.model.registry["knowledge_model_version"], versions=self.model.registry["versions"],
                          schema_version=self.model.registry["schema_version"], extractor_version=VERSION, included_changes=relevant, source_commits={k:p["commit"] for k,p in parts.items()},
                          dependencies=self.model.dependency_hashes(), files={k:byte_hash(v) for k,v in files.items()})
            stable["included_sprints"] = scope["sprints"]
            manifest_path = self.base + "snapshots/" + release + "/manifest.yaml"
            prior_commit = self.read(manifest_path).get("git_commit") if self.path(manifest_path).exists() else None
            stable["git_commit"] = self.fixed_commit(data.get("git_commit") or prior_commit or "HEAD")
            stable["dependency_contents"] = {rel: self.path(rel).read_text() for rel in stable["dependencies"]}
            snapshot_id = digest(stable)
            dest = self.base + "snapshots/" + release + "/"
            exists = self.path(dest + "manifest.yaml").exists()
            if exists:
                manifest = self.read(dest + "manifest.yaml")
                if manifest.get("snapshot_id") != snapshot_id or any(manifest.get(k) != v for k, v in stable.items()):
                    raise KnowledgeError("snapshot_input_drift")
                for name, raw in files.items():
                    if self.path(dest + name).read_bytes() != raw:
                        raise KnowledgeError("snapshot_content_drift")
                return {"status": "pass", "snapshot_id": snapshot_id, "manifest": dest + "manifest.yaml"}
            if not prepare:
                raise KnowledgeError("snapshot_missing")
            if data.get("publish_confirmation"):
                raise KnowledgeError("published_snapshot_missing")
            manifest = {**stable, "snapshot_id": snapshot_id, "generated_at": now(), "source_release": "releases/" + release + "/release.json"}
            files["manifest.yaml"] = canonical(manifest) + b"\n"
            self.limits(files)
            parent = self.path(self.base + "snapshots")
            parent.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryDirectory(prefix=".pending-", dir=parent) as tmp:
                for name, raw in files.items(): Path(tmp, name).write_bytes(raw)
                os.rename(tmp, self.path(dest)); Path(tmp).mkdir()
            return {"status": "prepared", "snapshot_id": snapshot_id, "manifest": dest + "manifest.yaml"}

    def bind(self, release):
        # Validation and binding share a lock; publish never generates snapshot content.
        with self.lock():
            result = self.snapshot(release, locked=True)
            if result["status"] == "out_of_scope": return result
            data, _ = self.release_data(release)
            reference = {"snapshot_id": result["snapshot_id"], "manifest": result["manifest"]}
            if data.get("publish_confirmation") and data.get("knowledge_model") != reference:
                raise KnowledgeError("published_binding_immutable")
            data["knowledge_model"] = reference
            atomic(self.path("releases/" + release + "/release.json"), data)
        return {**result, "status": "bound"}

    def cleanup(self):
        with self.lock():
            cutoff = time.time() - self.model.registry["limits"]["record_days"] * 86400
            removed = 0
            folder = self.path(self.runtime + "runs")
            if folder.exists():
                for p in folder.glob("*.json"):
                    path_in(self.root, str(p.relative_to(self.root)))
                    if p.stat().st_mtime < cutoff:
                        p.unlink(); removed += 1
            # Generations are conservatively retained: readers may outlive the lock.
            return {"status": "cleaned", "records_removed": removed, "generations": "retained-for-readers"}
