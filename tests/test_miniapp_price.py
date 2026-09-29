"""Executable price-state and page integration regression tests (synthetic data)."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_node(script):
    result = subprocess.run(["node", "-e", script], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def test_price_state_matrix_and_ts_js_parity():
    result = run_node(r"""
const fs = require('fs'), vm = require('vm');
const ts = require('./src/web/node_modules/typescript');
const js = require('./src/miniapp/utils/price');
const typed = {exports:{}};
vm.runInNewContext(ts.transpileModule(fs.readFileSync('src/miniapp/utils/price.ts','utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS}}).outputText, typed);
const cases = [['¥128.00',true,'valid','¥128.00'],['￥1,280.50',true,'valid','￥1,280.50'],['0.00',true,'empty','暂无'],['-2',true,'empty','暂无'],[null,true,'empty','暂无'],[undefined,true,'empty','暂无'],[0,true,'empty','暂无'],['暂无参考价',true,'empty','暂无'],['价格待维护',true,'empty','暂无'],['12,34',true,'empty','12,34'],['Infinity',true,'empty','Infinity'],['¥128.00',false,'unavailable','暂不可查看'],['0.01',true,'valid','0.01']];
for(const [v,a,state,text] of cases){
const got=js.pricePresentation(v,a), other=typed.exports.pricePresentation(v,a);
if(got.state!==state||got.text!==text||JSON.stringify(got)!==JSON.stringify(other))throw Error(JSON.stringify({v,got,other}));
}
console.log(JSON.stringify({cases:cases.length}));
""")
    assert result['cases'] == 13


def test_card_detail_favorites_recompute_price_states():
    result = run_node(r"""
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const helper=require('./src/miniapp/utils/price');
function load(path){const ctx={require:(id)=>id.includes('utils/price')?helper:{request:()=>{},track:()=>{}},Component:()=>{},Page:()=>{},wx:{setStorageSync:(key,items)=>{ctx.saved=items;}},console,setTimeout,clearTimeout};vm.createContext(ctx);vm.runInContext(fs.readFileSync(path,'utf8'),ctx);return ctx;}
const card=load('src/miniapp/components/product-card/index.js');
const states=['¥100.00','暂无','¥25.00'].map(price_display=>card.normalizeProduct({product_id:1,price_display}).priceState);
assert.deepStrictEqual(states,['valid','empty','valid']);
const offline=card.normalizeProduct({product_id:1,price_display:'¥100.00',status:'offline'});assert.equal(offline.priceState,'unavailable');assert.equal(offline.priceText,'暂不可查看');
const detail=load('src/miniapp/pages/tile-detail/index.js');
const view=detail.normalizeSkuDetail({price_display:'¥99.00',parameters:[],media:[],same_series_recommendations:[{price_display:'暂无'}],same_brand_recommendations:[{price_display:'¥20.00'}]});
assert.equal(view.priceView.state,'valid');assert.equal(view.same_series_recommendations[0].priceView.state,'empty');assert.equal(view.same_brand_recommendations[0].priceView.state,'valid');
const fav=load('src/miniapp/pages/favorites/index.js');
for(const status of ['available','unavailable']){const item=fav.normalizeFavoriteItem({objectType:'sku',objectId:1,price_display:'¥10.00',status});assert.equal(item.priceView.state,status==='available'?'valid':'unavailable');}
fav.writeFavorites([fav.normalizeFavoriteItem({objectType:'sku',objectId:1,price_display:'¥10.00',status:'available'})]);
assert.equal(fav.saved[0].price_display,'¥10.00');assert.equal('priceView' in fav.saved[0],false);
console.log(JSON.stringify({passed:true}));
""")
    assert result['passed']
