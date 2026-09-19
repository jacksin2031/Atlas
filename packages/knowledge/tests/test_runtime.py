from __future__ import annotations

import json

import pytest

from atlas_knowledge import KnowledgeNotFoundError, KnowledgeRuntime, KnowledgeStorageError, KnowledgeValidationError, ProjectScope


@pytest.fixture
def scope(tmp_path):
    return ProjectScope("project-a", str(tmp_path))


@pytest.fixture
def runtime():
    return KnowledgeRuntime()


def entry(content="The Atlas Knowledge Runtime acceptance code is KRT-1600.", **changes):
    return {"title": "Atlas acceptance fact", "content": content, "type": "fact", "tags": ["acceptance"], "metadata": {"verified": True}, "source": {"type": "user"}, **changes}


def test_crud_and_versioning(runtime, scope):
    created = runtime.create(scope, entry())
    assert runtime.get(scope, created.id) == created
    updated = runtime.update(scope, created.id, {"content": "Version 2", "title": "Updated"})
    assert updated.version == 2
    assert updated.content == "Version 2"
    assert runtime.delete(scope, created.id)["deleted"] is True
    with pytest.raises(KnowledgeNotFoundError):
        runtime.get(scope, created.id)


def test_lexical_search_is_deterministic_and_reports_trace(runtime, scope):
    created = runtime.create(scope, entry())
    first = runtime.search(scope, "Atlas Knowledge Runtime acceptance code", request_id="search-1")
    second = runtime.search(scope, "Atlas Knowledge Runtime acceptance code", request_id="search-2")
    assert first["method"] == "lexical"
    assert first["results"][0]["entry"]["id"] == second["results"][0]["entry"]["id"] == created.id
    assert "KRT-1600" in first["results"][0]["excerpt"]
    assert first["results"][0]["score"] > 0


def test_update_and_delete_do_not_leave_stale_search_results(runtime, scope):
    created = runtime.create(scope, entry(content="Version 1 stale marker"))
    runtime.update(scope, created.id, {"content": "Version 2 current marker"})
    assert runtime.search(scope, "stale marker")["result_count"] == 0
    assert runtime.search(scope, "current marker")["result_count"] == 1
    runtime.delete(scope, created.id)
    assert KnowledgeRuntime().search(scope, "current marker")["result_count"] == 0


def test_project_isolation(runtime, tmp_path):
    a_path, b_path = tmp_path / "a", tmp_path / "b"
    a_path.mkdir(); b_path.mkdir()
    a, b = ProjectScope("project-a", str(a_path)), ProjectScope("project-b", str(b_path))
    runtime.create(a, entry(content="PROJECT_A_SECRET_TEST"))
    runtime.create(b, entry(content="PROJECT_B_TEST"))
    assert runtime.search(b, "PROJECT_A_SECRET_TEST")["result_count"] == 0
    assert runtime.search(b, "PROJECT_B_TEST")["result_count"] == 1


def test_persistence_survives_runtime_restart(scope):
    first = KnowledgeRuntime()
    created = first.create(scope, entry())
    first.update(scope, created.id, {"content": "Version 2 KRT-1600"})
    second = KnowledgeRuntime()
    assert second.get(scope, created.id).content == "Version 2 KRT-1600"
    assert second.get(scope, created.id).version == 2
    assert second.search(scope, "KRT-1600")["result_count"] == 1


def test_primary_corruption_recovers_from_backup(runtime, scope):
    created = runtime.create(scope, entry(content="Version 1"))
    runtime.update(scope, created.id, {"content": "Version 2"})
    path = scope.project_path + "/.atlas/knowledge.v1.json"
    with open(path, "w", encoding="utf-8") as stream:
        stream.write("corrupt")
    recovered = KnowledgeRuntime().get(scope, created.id)
    assert recovered.content == "Version 1"


def test_both_corrupt_files_return_storage_error(runtime, scope):
    created = runtime.create(scope, entry(content="Version 1"))
    runtime.update(scope, created.id, {"content": "Version 2"})
    for suffix in ("", ".bak"):
        with open(scope.project_path + "/.atlas/knowledge.v1.json" + suffix, "w", encoding="utf-8") as stream:
            stream.write("corrupt")
    with pytest.raises(KnowledgeStorageError):
        runtime.get(scope, created.id)


def test_provenance_and_content_hash_are_persisted(runtime, scope):
    created = runtime.create(scope, entry(source={"type": "vision_ocr", "frame_reference": "frame-1"}, provenance={"observed": True}))
    assert created.source["type"] == "vision_ocr"
    assert created.provenance["observed"] is True
    assert len(created.provenance["content_hash"]) == 64


def test_credential_shaped_metadata_is_rejected(runtime, scope):
    with pytest.raises(KnowledgeValidationError):
        runtime.create(scope, entry(metadata={"api_key": "must-not-persist"}))


@pytest.mark.parametrize("payload", [
    {"title": "", "content": "x"},
    {"title": "x", "content": "y", "type": "semantic-magic"},
    {"title": "x", "content": "y", "metadata": {"value": object()}},
])
def test_malformed_entries_are_rejected(runtime, scope, payload):
    with pytest.raises(KnowledgeValidationError):
        runtime.create(scope, payload)


def test_import_txt_and_json_preserve_portable_source(runtime, scope):
    text = runtime.import_content(scope, filename=r"C:\private\fact.txt", content="Imported Atlas fact", format_name="txt")
    data = runtime.import_content(scope, filename="entries.json", content=json.dumps([entry(content="JSON Atlas fact")]), format_name="json")
    assert text["created"][0]["source"]["filename"] == "fact.txt"
    assert data["count"] == 1
    assert runtime.search(scope, "Imported Atlas")["result_count"] == 1


def test_import_csv_and_unsupported_binary(runtime, scope):
    result = runtime.import_content(scope, filename="facts.csv", content="title,content,tags\nOne,CSV fact,atlas", format_name="csv")
    assert result["count"] == 1
    with pytest.raises(KnowledgeValidationError):
        runtime.import_content(scope, filename="file.pdf", content="%PDF", format_name="pdf")


def test_export_json_and_markdown(runtime, scope):
    runtime.create(scope, entry())
    exported = runtime.export(scope, "json")
    assert json.loads(exported["content"])["projectId"] == scope.project_id
    assert "# Atlas acceptance fact" in runtime.export(scope, "md")["content"]


def test_list_is_bounded_and_filterable(runtime, scope):
    runtime.create(scope, entry(title="A", type="fact", tags=["one"]))
    runtime.create(scope, entry(title="B", type="note", tags=["two"]))
    assert runtime.list_entries(scope, entry_type="fact")["total"] == 1
    assert runtime.list_entries(scope, tags=["two"])["entries"][0]["title"] == "B"
    with pytest.raises(KnowledgeValidationError):
        runtime.list_entries(scope, limit=1000)


def test_events_record_mutations_import_and_search(runtime, scope):
    created = runtime.create(scope, entry())
    runtime.update(scope, created.id, {"title": "Changed"})
    runtime.search(scope, "KRT-1600", request_id="trace")
    runtime.delete(scope, created.id)
    types = [event["event_type"] for event in runtime.events(scope)]
    assert types == ["entry_created", "entry_updated", "search_completed", "entry_deleted"]


def test_ai_context_requires_same_project_and_existing_reference(runtime, tmp_path):
    path = tmp_path / "project"; path.mkdir()
    scope = ProjectScope("project-a", str(path))
    created = runtime.create(scope, entry())
    context = runtime.assemble_ai_context(scope, [created.reference.to_dict()])
    assert context[0]["content"].endswith("KRT-1600.")
    bad = created.reference.to_dict(); bad["project_id"] = "project-b"
    with pytest.raises(KnowledgeValidationError):
        runtime.assemble_ai_context(scope, [bad])


def test_status_reports_real_storage_and_lexical_index(runtime, scope):
    runtime.create(scope, entry())
    status = runtime.status(scope)
    assert status["status"] == "available"
    assert status["index"] == {"method": "lexical", "state": "ready", "document_count": 1}
    assert status["storage"]["location"].startswith("project://")

@pytest.mark.parametrize("version", [2, True, "1"])
def test_incompatible_primary_never_recovers_over_source(runtime, scope, version):
    from pathlib import Path
    from atlas_knowledge.storage import JsonProjectKnowledgeStorage
    created = runtime.create(scope, entry())
    runtime.update(scope, created.id, {"content": "second"})
    path = Path(scope.project_path) / ".atlas" / "knowledge.v1.json"
    value = json.loads(path.read_text())
    value["schemaVersion"] = version
    path.write_text(json.dumps(value))
    original = path.read_bytes()
    with pytest.raises(KnowledgeStorageError):
        JsonProjectKnowledgeStorage().load(scope)
    with pytest.raises(KnowledgeStorageError):
        JsonProjectKnowledgeStorage().save(scope, [])
    assert path.read_bytes() == original


def test_malformed_entry_is_not_silently_discarded(scope):
    from atlas_knowledge.storage import JsonProjectKnowledgeStorage
    storage = JsonProjectKnowledgeStorage()
    primary, _ = storage._paths(scope)
    primary.write_text(json.dumps({"schemaVersion": 1, "projectId": scope.project_id, "entries": [42]}))
    with pytest.raises(KnowledgeStorageError):
        storage.load(scope)


def test_failed_replace_preserves_original(runtime, scope, monkeypatch):
    from pathlib import Path
    import atlas_knowledge.storage as storage_module
    created = runtime.create(scope, entry())
    path = Path(scope.project_path) / ".atlas" / "knowledge.v1.json"
    original = path.read_bytes()
    def fail_replace(source, destination):
        raise OSError("simulated commit failure")
    monkeypatch.setattr(storage_module.os, "replace", fail_replace)
    with pytest.raises(KnowledgeStorageError):
        runtime.update(scope, created.id, {"content": "lost"})
    assert path.read_bytes() == original
    assert not list(path.parent.glob("*.tmp"))
