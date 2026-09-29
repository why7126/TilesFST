import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import vm from 'node:vm';
import ts from 'typescript';
import { expect, it, vi } from 'vitest';
const root = resolve(process.cwd(), '../miniapp');

function harness(extension: string) {
  const page = {};
  let definition: any;
  const calls: any[] = [], events: any[] = [], downloads: any[] = [];
  const modules = new Map<string, any>();
  const api = { request: vi.fn((_url: string, options: any) => new Promise(resolve => {
    const abort = vi.fn(); options.onRequestTask({abort}); calls.push({options, resolve, abort});
  })), track: (...args: any[]) => events.push(args) };
  function load(file: string): any {
    if (modules.has(file)) return modules.get(file).exports;
    const module = {exports: {}}; modules.set(file, module);
    let source = readFileSync(`${file}.${extension}`, 'utf8');
    if (extension === 'ts') source = ts.transpileModule(source, {compilerOptions:{target:ts.ScriptTarget.ES2018,module:ts.ModuleKind.CommonJS}}).outputText;
    vm.runInNewContext(source,{module,exports:module.exports,Date,Promise,Map,Set,WeakMap,setTimeout,clearTimeout,
      wx:{getPerformance:()=>({now:()=>0}),downloadFile:(options:any)=>{const abort=vi.fn();downloads.push({options,abort});return {abort};}}, getCurrentPages:()=>[page], Component:(value:any)=>{definition=value;},
      require:(name:string)=>name.endsWith('services/api') ? api : load(resolve(dirname(file),name)),
    });
    return module.exports;
  }
  load(resolve(root,'components/authorized-image/index'));
  function image(id: string) {
    const instance:any={...definition.methods, properties:{resourceType:'sku_image',resourceId:id,mediaId:0,variant:'thumbnail',src:'/media/never-read-directly'},data:{...definition.data},setData(patch:any){Object.assign(this.data,patch);}};
    definition.lifetimes.attached.call(instance); return instance;
  }
  function answer(index: number, suffix = '') {
    const call = calls[index]; call.resolve({server_time:'2026-09-08T00:00:00Z',items:call.options.data.items.map((reference:any)=>({reference,status:'ready',descriptor:{media_ref:reference.resource_id,variant:reference.variant,read_mode:'direct',expires_at:'2026-09-08T00:05:00Z',url:`https://storage.example.test/${reference.resource_id}${suffix}`}}))});
  }
  return {image,answer,calls,events,definition,api,downloads,page,pool:load(resolve(root,'utils/page-media'))};
}
for (const extension of ['ts','js']) {
  it(`${extension}: page widgets batch distinct references and isolate a hidden subscriber`,async()=>{
    const h=harness(extension), a=h.image('1'), b=h.image('2');
    await vi.waitFor(()=>expect(h.calls).toHaveLength(1));
    expect(h.calls[0].options.data.items).toHaveLength(2);
    a.hideMedia(); h.answer(0);
    await vi.waitFor(()=>expect(b.data.signedUrl).toBe('https://storage.example.test/2'));
    expect(a.data.signedUrl).toBe(''); expect(h.calls[0].abort).not.toHaveBeenCalled();
    b.onImageLoad(); expect(h.events.some(event=>event[1].phase==='load' && event[1].result==='success')).toBe(true);
    b.hideMedia();
  });
  it(`${extension}: replacement rejects old completion and final hide aborts requests`,async()=>{
    const h=harness(extension), a=h.image('1');
    await vi.waitFor(()=>expect(h.calls).toHaveLength(1));
    a.properties.resourceId='2'; a.loadMedia('initial');
    await vi.waitFor(()=>expect(h.calls).toHaveLength(2));
    h.answer(1); await vi.waitFor(()=>expect(a.data.signedUrl).toBe('https://storage.example.test/2'));
    h.answer(0); await Promise.resolve(); expect(a.data.signedUrl).toBe('https://storage.example.test/2');
    a.properties.resourceId='3'; a.loadMedia('initial');
    await vi.waitFor(()=>expect(h.calls).toHaveLength(3));
    a.hideMedia(); expect(h.calls[2].abort).toHaveBeenCalledTimes(1);
    h.answer(2); await Promise.resolve(); expect(a.data.signedUrl).toBe('');
  });
}

for (const extension of ['ts','js']) {
  it(`${extension}: failed attachment download reauthorizes before preparing a native file`,async()=>{
    const h=harness(extension);h.pool.beginPageMedia(h.page);
    const reference={resource_type:'certificate',resource_id:'136',variant:'original'};
    const preview=h.pool.preparePageFiles(h.page,[reference]);
    try {
      await vi.waitFor(()=>expect(h.calls).toHaveLength(1));h.answer(0,'/expired');
      await vi.waitFor(()=>expect(h.downloads).toHaveLength(1));
      expect(h.downloads[0].options.url).toContain('/expired');
      h.downloads[0].options.success({statusCode:403});
      await vi.waitFor(()=>expect(h.calls).toHaveLength(2),{timeout:2500});
      expect(h.calls[1].options.data.items).toEqual([reference]);h.answer(1,'/renewed');
      await vi.waitFor(()=>expect(h.downloads).toHaveLength(2));
      expect(h.downloads[1].options.url).toContain('/renewed');
      h.downloads[1].options.success({statusCode:200,tempFilePath:'wxfile://tmp/current.pdf'});
      expect(await preview).toEqual(['wxfile://tmp/current.pdf']);
    } finally {h.pool.endPageMedia(h.page);}
  });
  it(`${extension}: denied attachment renewal stops without another storage download`,async()=>{
    const h=harness(extension);h.pool.beginPageMedia(h.page);
    const reference={resource_type:'certificate',resource_id:'136',variant:'original'};
    const preview=h.pool.preparePageFiles(h.page,[reference]);
    const rejection=expect(preview).rejects.toBeDefined();
    try {
      await vi.waitFor(()=>expect(h.calls).toHaveLength(1));h.answer(0);
      await vi.waitFor(()=>expect(h.downloads).toHaveLength(1));
      h.downloads[0].options.success({statusCode:403});
      await vi.waitFor(()=>expect(h.calls).toHaveLength(2),{timeout:2500});
      h.calls[1].resolve({server_time:'2026-09-08T00:00:00Z',items:[{reference,status:'unavailable'}]});
      await rejection;
      expect(h.downloads).toHaveLength(1);
      expect(h.calls).toHaveLength(2);
    } finally {h.pool.endPageMedia(h.page);}
  });
  it(`${extension}: native albums use local files, cap downloads, and cancel on hide`,async()=>{
    const h=harness(extension);h.pool.beginPageMedia(h.page);
    const refs=Array.from({length:5},(_,i)=>({resource_type:'sku_image',resource_id:String(i+1),variant:'original'}));
    const preview=h.pool.preparePageImages(h.page,refs);
    await vi.waitFor(()=>expect(h.calls).toHaveLength(1));h.answer(0);
    await vi.waitFor(()=>expect(h.downloads).toHaveLength(4));
    h.downloads[0].options.success({statusCode:200,tempFilePath:'wxfile://tmp/1'});
    await vi.waitFor(()=>expect(h.downloads).toHaveLength(5));
    for(let i=1;i<5;i++)h.downloads[i].options.success({statusCode:200,tempFilePath:`wxfile://tmp/${i+1}`});
    expect(await preview).toEqual(refs.map((_,i)=>`wxfile://tmp/${i+1}`));
    const late=h.pool.preparePageImages(h.page,[refs[0]]);
    const rejection=expect(late).rejects.toHaveProperty('name','AbortError');
    await vi.waitFor(()=>expect(h.calls).toHaveLength(2));h.answer(1);
    await vi.waitFor(()=>expect(h.downloads).toHaveLength(6));h.pool.endPageMedia(h.page);
    await rejection;expect(h.downloads[5].abort).toHaveBeenCalledTimes(1);
  });
}
