const test = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '../../src/miniapp');
function harness(options = {}) {
  const events = [], requests = [], storage = { miniapp_search_recent_keywords_v1: ['local-only'] };
  const wx = new Proxy({
    getStorageSync: key => storage[key], setStorage: ({key,data}) => { storage[key] = data; },
    getImageInfo: options.image || (o => o.fail()),
  }, {get: (target, key) => target[key] || (() => {})});
  const api = { track: (name, props) => { if(options.trackThrows) throw Error('offline'); events.push({name,props}); if(options.trackRejects) return Promise.reject(Error('offline')); },
    request: url => { requests.push(url); return Promise.resolve(options.response || { items: [], page: 1, has_more: false }); }};
  function evaluate(file, extra={}) {
    const module = {exports:{}};
    let source = fs.readFileSync(path.join(root,file),'utf8');
    if (process.env.MINIAPP_TEST_TYPESCRIPT === '1') {
      const ts = require('../../src/web/node_modules/typescript');
      source = ts.transpileModule(fs.readFileSync(path.join(root,file.replace(/\.js$/, '.ts')),'utf8'), { compilerOptions: { target: ts.ScriptTarget.ES2020, module: ts.ModuleKind.CommonJS } }).outputText;
    }
    vm.runInNewContext(source, {
      module, exports:module.exports, console, wx, setTimeout, clearTimeout,
      require: name => name.includes('public-sharing') ? sharing : name.includes('services/api') ? api : name.includes('price') ? { displayPriceState: () => ({}) } : {},
      ...extra,
    },{filename:file}); return module.exports;
  }
  const sharing=evaluate('utils/public-sharing.js');
  function page(name) {
    let definition;
    evaluate(`pages/${name}/index.js`, {Page: d => { definition=d; }});
    const instance = {...definition,data:JSON.parse(JSON.stringify(definition.data || {})),setData(patch){ Object.assign(this.data,patch); }};
    return instance;
  }
  return {sharing,page,events,requests,storage,wx};
}
const names=['index','tile-detail','product-list','brand-detail','certificate-detail','brand-list','certificates','search','category','store-info','find'];
for (const name of names) test(`${name}: real callbacks return safe dual-channel routes`,()=>{
  const h=harness(), p=h.page(name); p.data.id=7; p.data.brandId=8;p.data.certificateId=9;
  const friend=p.onShareAppMessage(), timeline=p.onShareTimeline();
  assert.equal(friend.path.split('?')[0],`/pages/${name}/index`);
  assert.ok(friend.title);assert.ok(timeline.title);assert.equal(friend.imageUrl,h.sharing.LOGO);
  const q=new URLSearchParams(timeline.query);assert.equal(q.get('source'),'share');assert.equal(q.get('shareChannel'),'wechat_timeline');
  assert.equal(h.events.length,2);assert.ok(h.events.every(e=>!e.props.page_path.includes('?')));
});
test('parameter round trip, tampering, and no inherited context',()=>{
 const h=harness();const p=h.page('product-list');Object.assign(p.data,{categoryId:2,categoryLevel:'secondary',keyword:'石材 %26 & 空 格',brandId:4,spec:'800x800',priceRange:'10-80',sort:'price_desc',page:9,token:'secret'});
 const share=p.onShareAppMessage();const query=Object.fromEntries(share.path.split('?')[1].split('&').map(p=>p.split('=')));
 query.token='secret';query.requestId='sender'; const restored=h.sharing.receiveShare('product-list',query);
 assert.equal(restored.keyword,p.data.keyword);assert.equal(restored.priceRange,'10-80');assert.equal(restored.sort,'price_desc');assert.equal(restored.requestId,undefined);assert.equal(restored.token,undefined);
 assert.equal(new URLSearchParams(share.path.split('?')[1]).get('page'),null);
 const invalid=h.sharing.receiveShare('tile-detail',{source:'share',skuId:'NaN',id:'bad'}); assert.equal(invalid.skuId,'');assert.equal(invalid.id,undefined);
 assert.doesNotThrow(()=>h.sharing.receiveShare('search',{source:'share',keyword:'%E0%A4%A'}));
 assert.equal(h.sharing.sanitize('product-list',{priceRange:'80-10'}).priceRange,undefined);
 assert.equal(h.sharing.sanitize('product-list',{priceRange:'-80'}).priceRange,'-80');
 assert.equal(h.sharing.sanitize('search',{keyword:'中'.repeat(80)}).keyword.length,80);
 assert.equal(h.sharing.sanitize('search',{keyword:'中'.repeat(81)}).keyword,undefined);
 assert.ok(h.events.every(e=>!JSON.stringify(e).includes('石材')));
});
test('query overflow falls back as a whole, with matching title',()=>{
 const h=harness(),p=h.page('product-list');Object.assign(p.data,{keyword:'中'.repeat(80),spec:'中'.repeat(80),categoryName:'中'.repeat(80)});
 let card=p.onShareAppMessage();assert.ok(card.path.split('?')[1].length<=2048);assert.equal(new URLSearchParams(card.path.split('?')[1]).get('categoryName'),null);
 p.data.keyword='x'.repeat(81);card=p.onShareAppMessage();assert.equal(card.title,'全部商品');assert.equal(new URLSearchParams(card.path.split('?')[1]).get('spec'),null);
});
test('image validation never blocks first share and failure stays on logo',()=>{
 let pending;const h=harness({image:o=>{pending=o;}}),p=h.page('brand-detail');p.data.brandId=1;p.data.brand={brand_name:'品牌',brand_logo_thumbnail_url:'https://public.example/logo.thumb.jpg'};
 assert.equal(p.onShareAppMessage().imageUrl,h.sharing.LOGO);pending.success({path:'wxfile://tmp/brand.png'});assert.equal(p.onShareAppMessage().imageUrl,'wxfile://tmp/brand.png');
 p.data.brand.brand_logo_thumbnail_url='https://public.example/bad.thumb.jpg';assert.equal(p.onShareAppMessage().imageUrl,h.sharing.LOGO);pending.fail();assert.equal(p.onShareAppMessage().imageUrl,h.sharing.LOGO);
});
test('search receive executes query but preserves personal history and skips submit event',()=>{
 const h=harness(),p=h.page('search');p.loadResults=()=>{};p.onLoad({source:'share',keyword:encodeURIComponent('花纹'),scope:encodeURIComponent('客厅'),tab:'sku'});
 assert.deepEqual(h.storage.miniapp_search_recent_keywords_v1,['local-only']);assert.equal(p.data.normalizedKeyword,'花纹');assert.equal(p.data.filterSnapshot.category,'客厅');assert.equal(p.data.activeTab,'sku');assert.ok(!h.events.some(e=>e.name==='search_submit'));
 p.data.keyword='草稿';assert.equal(new URLSearchParams(p.onShareTimeline().query).get('keyword'),'花纹');
 p.submitSearch();assert.equal(h.storage.miniapp_search_recent_keywords_v1[0],'草稿');assert.ok(h.events.some(e=>e.name==='search_submit'));
 p.data.searchMode='home';const card=p.onShareAppMessage();assert.equal(new URLSearchParams(card.path.split('?')[1]).get('keyword'),null);assert.equal(card.imageUrl,h.sharing.LOGO);
});
test('product receive uses full existing API conditions and resets page',()=>{
 const h=harness(),p=h.page('product-list');p.loadProducts=()=>{};p.onLoad({source:'share',categoryId:'2',categoryLevel:'primary',keyword:'瓷砖',spec:'800',priceRange:'0-80',sort:'price_asc',page:'8'});
 const query=new URLSearchParams(p.buildQuery(1));assert.equal(query.get('sort'),'price_asc');assert.equal(query.get('spec'),'800');assert.equal(query.get('priceRange'),'0-80');assert.equal(p.data.page,1);
});
test('brand/certificate share uses successful query rather than input draft',async()=>{
 for(const name of ['brand-list','certificates']){
  const h=harness(),p=h.page(name);p.data.keyword='submitted';
  if(name==='brand-list')p.loadBrands(true);else p.loadCertificates({reset:true});
  await new Promise(resolve=>setImmediate(resolve));p.data.keyword='draft';
  assert.equal(new URLSearchParams(p.onShareTimeline().query).get('keyword'),'submitted');
 }
});
test('category share selection survives onShow and stale cache',async()=>{
 const tree={items:[{id:1,name:'one',children:[]},{id:2,name:'two',children:[]}]};const h=harness({response:tree}),p=h.page('category');
 p.readCache=()=>tree;p.readSavedState=()=>({currentPrimaryId:1});p.onLoad({source:'share',categoryId:'2'});p.onShow();assert.equal(p.data.currentPrimaryId,2);
 await new Promise(resolve=>setImmediate(resolve));assert.equal(p.data.currentPrimaryId,2);
 p.onLoad({source:'share',categoryId:'99'});await new Promise(resolve=>setImmediate(resolve));assert.equal(p.data.currentPrimaryId,1);
});
test('collection throw does not prevent share or receive parsing',()=>{
 const h=harness({trackThrows:true}),p=h.page('find');assert.doesNotThrow(()=>p.onShareAppMessage());assert.doesNotThrow(()=>h.sharing.receiveShare('find',{source:'share'}));let route;h.wx.navigateTo=o=>{route=o.url;};p.openSearch();assert.equal(route,'/pages/search/index');
});

test('optional unset IDs do not discard effective product filters',()=>{
 const h=harness(),p=h.page('product-list');Object.assign(p.data,{keyword:'瓷砖',spec:'800',priceRange:'0-80'});
 const q=new URLSearchParams(p.onShareTimeline().query);assert.equal(q.get('keyword'),'瓷砖');assert.equal(q.get('priceRange'),'0-80');assert.equal(q.get('categoryId'),null);
});
test('input suggestions share only the public search entry',()=>{
 const h=harness(),p=h.page('search');p.scheduleSearchInputTrack=()=>{};p.onInput({detail:{value:'draft'}});clearTimeout(p.suggestionTimer);
 assert.equal(new URLSearchParams(p.onShareTimeline().query).get('keyword'),null);
});
test('async collection rejection is isolated',async()=>{
 const h=harness({trackRejects:true});h.page('find').onShareAppMessage();h.sharing.receiveShare('find',{source:'share'});
 await new Promise(resolve=>setImmediate(resolve));assert.equal(h.events.length,2);
});
test('ordinary no-stack navigation falls back home and recovers switch failure',()=>{
 let component,route;vm.runInNewContext(fs.readFileSync(path.join(root,'components/custom-navigation/index.js'),'utf8'),{
 Component:c=>component=c,getCurrentPages:()=>[],wx:{switchTab:o=>{assert.equal(o.url,'/pages/index/index');o.fail();},reLaunch:o=>{route=o.url;}}
 });component.methods.handleBack();assert.equal(route,'/pages/index/index');
});
test('text and price length boundaries',()=>{
 const {sharing:s}=harness();for(const n of [79,80,81])for(const key of ['keyword','spec'])assert.equal(Boolean(s.sanitize('product-list',{[key]:'a'.repeat(n)})[key]),n<=80);
 for(const n of [39,40,41])assert.equal(Boolean(s.sanitize('product-list',{priceRange:'0.'+'0'.repeat(n-4)+'1-' }).priceRange),n<=40);
});
test('encoded query exact 2047/2048/2049 boundary preserves or drops only display name',()=>{
 for(const limit of [2047,2048,2049]){
  const h=harness(),p=h.page('product-list');Object.assign(p.data,{keyword:'中'.repeat(80),spec:'中'.repeat(80),categoryId:1,categoryLevel:'primary'});
  let found=false;
  for(let chinese=0;chinese<=80&&!found;chinese++)for(let ascii=0;ascii<=80-chinese;ascii++){
   p.data.categoryName='中'.repeat(chinese)+'a'.repeat(ascii);
   if(h.sharing.serialize(h.sharing.sanitize('product-list',p.data),'wechat_timeline').length===limit){found=true;break;}
  }
  assert.ok(found);const card=p.onShareTimeline(),q=new URLSearchParams(card.query);
  assert.ok(card.query.length<=2048);assert.equal(q.has('categoryName'),limit<=2048);assert.equal(q.get('spec'),p.data.spec);assert.equal(q.get('categoryId'),'1');
 }
});


test('native share logo uses a cached local file for both channels',()=>{
 const h=harness(),p=h.page('search');const copies=[];
 h.wx.env={USER_DATA_PATH:'wxfile://usr'};
 h.wx.getFileSystemManager=()=>({copyFileSync:(...args)=>copies.push(args),accessSync:()=>{}});
 assert.equal(p.onShareAppMessage().imageUrl,'wxfile://usr/public-share-logo-v1.png');
 assert.equal(p.onShareTimeline().imageUrl,'wxfile://usr/public-share-logo-v1.png');
 assert.deepEqual(copies,[[h.sharing.LOGO,'wxfile://usr/public-share-logo-v1.png']]);
});
test('restricted file APIs retain a valid synchronous package fallback',()=>{
 const h=harness(),p=h.page('search');h.wx.env={USER_DATA_PATH:'wxfile://usr'};
 h.wx.getFileSystemManager=()=>({copyFileSync:()=>{throw Error('restricted');}});
 assert.equal(p.onShareAppMessage().imageUrl,h.sharing.LOGO);
 assert.equal(p.onShareTimeline().imageUrl,h.sharing.LOGO);
});
test('page entry prepares the logo and shares reuse it when file APIs become unavailable',()=>{
 const h=harness(),p=h.page('search');let copies=0;
 h.wx.env={USER_DATA_PATH:'wxfile://usr'};
 h.wx.getFileSystemManager=()=>({copyFileSync:()=>{copies++;}});
 h.sharing.receiveShare('search',{});
 h.wx.getFileSystemManager=()=>{throw Error('offline bridge');};
 assert.equal(p.onShareAppMessage().imageUrl,'wxfile://usr/public-share-logo-v1.png');
 assert.equal(p.onShareTimeline().imageUrl,'wxfile://usr/public-share-logo-v1.png');assert.equal(copies,1);
});

test('validated remote image shares decoded local file instead of expiring URL',()=>{
 let pending;const h=harness({image:o=>{pending=o;}}),p=h.page('product-list');
 p.data.items=[{cover_image:'https://public.example/short-lived.thumb.png'}];
 assert.equal(p.onShareAppMessage().imageUrl,h.sharing.LOGO);
 pending.success({path:'wxfile://tmp/decoded-share.png'});
 assert.equal(p.onShareAppMessage().imageUrl,'wxfile://tmp/decoded-share.png');
 assert.equal(p.onShareTimeline().imageUrl,'wxfile://tmp/decoded-share.png');
});
test('image success without a decoded local file remains on the logo',()=>{
 let pending;const h=harness({image:o=>{pending=o;}}),p=h.page('product-list');
 p.data.items=[{cover_image:'https://public.example/invalid.thumb.png'}];
 p.onShareAppMessage();pending.success({path:'https://public.example/invalid.thumb.png'});
 assert.equal(p.onShareTimeline().imageUrl,h.sharing.LOGO);
});
