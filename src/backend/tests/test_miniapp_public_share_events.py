"""Exercise actual miniapp share payloads against the usage-event API."""
from pathlib import Path
import json
import subprocess

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.db.session import get_session_factory
from tests.test_auth import client  # noqa: F401


@pytest.fixture(scope="module")
def share_events():
    root = Path(__file__).resolve().parents[3]
    script = r"""
const fs=require('fs'),vm=require('vm');const events=[],moduleMock={exports:{}};
vm.runInNewContext(fs.readFileSync('src/miniapp/utils/public-sharing.js','utf8'),{
module:moduleMock,wx:{getImageInfo:o=>o.fail()},require:()=>({track:(name,props)=>events.push({event_name:name,client_type:'wechat_miniapp',page_path:props.page_path,properties:{...props,client_type:'wechat_miniapp'}})})
});
const h=moduleMock.exports;
for(const page of ['index','tile-detail','product-list','brand-detail','certificate-detail','brand-list','certificates','search','category','store-info','find']){
 const data={id:7,brandId:8,certificateId:9,categoryId:2,currentPrimaryId:2,keyword:'private-query',shareKeyword:'private-query',normalizedKeyword:'private-query',searchMode:'result',scope:'all',activeTab:'sku',requestId:'local-receiver-1'};
 for(const channel of ['wechat_friend','wechat_timeline'])h.sharePage(page,{data},channel);
 h.receiveShare(page,{source:'share',shareChannel:'wechat_friend',skuId:'7',brandId:'8',certificateId:'9',categoryId:'2',keyword:'private-query'});
}
console.log(JSON.stringify(events));
"""
    result = subprocess.run(["node", "-e", script], cwd=root, text=True, capture_output=True, check=True)
    return json.loads(result.stdout)


@pytest.mark.parametrize("index", range(33))
def test_real_share_payload_accepted_and_stored_without_raw_query(client: TestClient, share_events, index):
    payload = share_events[index]
    response = client.post("/api/v1/usage-events", json=payload)
    assert response.status_code == 200, response.text
    event_id = response.json()["data"]["id"]
    with get_session_factory()() as session:
        metadata = session.execute(text("SELECT metadata FROM usage_events WHERE id=:id"), {"id": event_id}).scalar_one()
    assert "private-query" not in metadata
    assert "source=share" not in metadata
    assert "share_channel" in metadata


def test_public_share_event_rejects_raw_keyword(client: TestClient):
    response = client.post("/api/v1/usage-events", json={
        "event_name": "share_page_open", "client_type": "wechat_miniapp",
        "properties": {"page_path": "/pages/search/index", "client_type": "wechat_miniapp", "share_channel": "wechat_friend", "keyword": "private-query"},
    })
    assert response.status_code == 400
    assert response.json()["code"] == 40001
