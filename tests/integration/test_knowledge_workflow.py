from __future__ import annotations

import time
from typing import Any

from atlas_workflow.host import DesktopWorkflowHost


def node(node_id: str, node_type: str, *, inputs=(), outputs=(), config=None) -> dict[str, Any]:
    return {"id":node_id,"type":node_type,"config":config or {},"inputs":list(inputs),"outputs":list(outputs),"ports_in":[f"{node_id}:in:{i}" for i,_ in enumerate(inputs)],"ports_out":[f"{node_id}:out:{i}" for i,_ in enumerate(outputs)],"metadata":{"input_ports":{f"{node_id}:in:{i}":name for i,name in enumerate(inputs)},"output_ports":{f"{node_id}:out:{i}":name for i,name in enumerate(outputs)},"input_port_types":{f"{node_id}:in:{i}":"any" for i,_ in enumerate(inputs)},"output_port_types":{f"{node_id}:out:{i}":"any" for i,_ in enumerate(outputs)}}}


def edge(source: str, target: str, source_index=0, target_index=0) -> dict[str, Any]:
    return {"source":source,"target":target,"source_port":f"{source}:out:{source_index}","target_port":f"{target}:in:{target_index}"}


def definition(nodes, edges, exits):
    return {"name":"knowledge-acceptance","version":"1.0.0","metadata":{"name":"knowledge-acceptance"},"nodes":nodes,"edges":edges,"variables":[],"entry_nodes":[item["id"] for item in nodes if item["type"]=="entry"],"exit_nodes":exits}


def wait_result(host: DesktopWorkflowHost, execution_id: str):
    deadline=time.monotonic()+5
    while time.monotonic()<deadline:
        result=host.result(execution_id)["result"]
        if result is not None:return result
        time.sleep(.01)
    raise AssertionError("workflow did not finish")


def test_workflow_write_search_validate_real_runtime(tmp_path):
    host=DesktopWorkflowHost()
    nodes=[
        node("entry","entry",outputs=("output",)),
        node("write","knowledge_write",inputs=("trigger",),outputs=("entry","reference","persistentId"),config={"title":"Acceptance","content":"The Atlas Knowledge Runtime acceptance code is KRT-1600.","metadata":{"acceptance":True}}),
        node("search","knowledge_search",inputs=("trigger","query"),outputs=("results","references","context","retrieval"),config={"query":"Atlas Knowledge Runtime acceptance code"}),
        node("validate","knowledge_validate",inputs=("results",),outputs=("valid","result"),config={"expected":"KRT-1600"}),
        node("exit","exit",inputs=("input",)),
    ]
    manifest=definition(nodes,[edge("entry","write"),edge("write","search"),edge("search","validate"),edge("validate","exit")],["exit"])
    started=host.start({"definition":manifest,"projectContext":{"projectId":"project-a","path":str(tmp_path)}})
    result=wait_result(host,started["executionId"])
    assert result["success"] is True
    assert result["output"]["value"] is True
    stored=host.knowledge_command("knowledge_search",{"projectId":"project-a","projectPath":str(tmp_path),"query":"KRT-1600"})
    assert stored["results"][0]["entry"]["content"].endswith("KRT-1600.")
    assert stored["results"][0]["reference"]["project_id"] == "project-a"


def test_workflow_knowledge_failure_propagates_without_killing_host(tmp_path):
    host=DesktopWorkflowHost()
    bad=definition([node("entry","entry",outputs=("output",)),node("search","knowledge_search",inputs=("query",),outputs=("results",),config={"query":""}),node("exit","exit",inputs=("input",))],[edge("entry","search"),edge("search","exit")],["exit"])
    failed=wait_result(host,host.start({"definition":bad,"projectContext":{"projectId":"project-a","path":str(tmp_path)}})["executionId"])
    assert failed["success"] is False
    scope={"projectId":"project-a","projectPath":str(tmp_path)}
    created=host.knowledge_command("knowledge_create",{**scope,"entry":{"title":"Recovered","content":"host remains alive"}})
    assert created["title"] == "Recovered"


def test_vision_ocr_write_search_validate_real_runtime(tmp_path):
    host=DesktopWorkflowHost()
    frame={"url":"memory://controlled-ocr-frame","frameId":"frame-1"}
    nodes=[
        node("entry","entry",outputs=("output",)),
        node("ocr","vision_ocr",inputs=("frame",),outputs=("region","bounds","point","text","matches","providerResult","frame"),config={"frame":frame,"results":[{"text":"ATLAS KNOWLEDGE VISION TEST","confidence":0.99,"bounds":{"x":1,"y":2,"width":3,"height":4}}]}),
        node("write","knowledge_write",inputs=("content","providerResult","frame"),outputs=("entry","reference","persistentId"),config={"title":"OCR observation"}),
        node("search","knowledge_search",inputs=("trigger",),outputs=("results","references","context","retrieval"),config={"query":"ATLAS KNOWLEDGE VISION TEST"}),
        node("validate","knowledge_validate",inputs=("results",),outputs=("valid","result"),config={"expected":"ATLAS KNOWLEDGE VISION TEST"}),
        node("exit","exit",inputs=("input",)),
    ]
    edges=[edge("entry","ocr"),edge("ocr","write",3,0),edge("ocr","write",5,1),edge("ocr","write",6,2),edge("write","search"),edge("search","validate"),edge("validate","exit")]
    manifest=definition(nodes,edges,["exit"])
    started=host.start({"definition":manifest,"projectContext":{"projectId":"project-a","path":str(tmp_path)}})
    result=wait_result(host,started["executionId"])
    assert result["success"] is True
    assert result["output"]["value"] is True
    found=host.knowledge_command("knowledge_search",{"projectId":"project-a","projectPath":str(tmp_path),"query":"ATLAS KNOWLEDGE VISION TEST"})
    entry=found["results"][0]["entry"]
    assert entry["source"]["type"] == "vision_ocr"
    assert entry["source"]["frame_reference"] == "frame-1"


def test_knowledge_reference_reaches_ai_runtime_request_boundary(tmp_path):
    host=DesktopWorkflowHost()
    class Context:
        instance_id="execution-ai"; workflow_id="knowledge-ai"
    host._sessions[Context.instance_id]={"projectContext":{"projectId":"project-a","path":str(tmp_path)}}
    scope={"projectId":"project-a","projectPath":str(tmp_path)}
    created=host.knowledge_command("knowledge_create",{**scope,"entry":{"title":"Animal","content":"The Atlas secret acceptance animal is ORANGE CAPYBARA."}})
    captured={}
    host.bridge.request=lambda bridge,command,payload,timeout=180: captured.update(payload) or {"content":"ok"}  # type: ignore[method-assign]
    host._ai_inference("ai",{"providerId":"provider","modelId":"model","prompt":"animal?"},{"context":[{"entry_id":created["id"],"project_id":"project-a","entry_type":"note","title":"Animal","source_type":"user"}]},{},Context())
    request=captured["request"]
    assert request["contextReferences"][0]["entry_id"] == created["id"]
    assert request["knowledgeContext"][0]["content"].endswith("ORANGE CAPYBARA.")
