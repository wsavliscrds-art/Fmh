import json
import os
_root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data=open(os.path.join(_root,'data','daily.json')).read()
html = r'''<title>Painel Mini FMH</title>
<style>
:root{
  color-scheme: light;
  --plane:#f9f9f7; --surface:#fcfcfb; --surface-2:#ffffff;
  --ink:#0b0b0b; --ink-2:#52514e; --muted:#898781;
  --grid:#e1e0d9; --axis:#c3c2b7; --border:rgba(11,11,11,0.10);
  --s1:#2a78d6; --s2:#eb6834; --s3:#1baf7a; --s4:#eda100; --s5:#e87ba4;
  --s6:#008300; --s7:#4a3aa7; --s8:#e34948;
  --good:#006300; --bad:#d03b3b; --accent:#2a78d6;
}
@media (prefers-color-scheme: dark){
  :root:where(:not([data-theme="light"])){
    color-scheme: dark;
    --plane:#0d0d0d; --surface:#1a1a19; --surface-2:#212120;
    --ink:#ffffff; --ink-2:#c3c2b7; --muted:#898781;
    --grid:#2c2c2a; --axis:#383835; --border:rgba(255,255,255,0.10);
    --s1:#3987e5; --s2:#d95926; --s3:#199e70; --s4:#c98500; --s5:#d55181;
    --s6:#008300; --s7:#9085e9; --s8:#e66767;
    --good:#0ca30c; --bad:#e66767; --accent:#3987e5;
  }
}
:root[data-theme="dark"]{
  color-scheme: dark;
  --plane:#0d0d0d; --surface:#1a1a19; --surface-2:#212120;
  --ink:#ffffff; --ink-2:#c3c2b7; --muted:#898781;
  --grid:#2c2c2a; --axis:#383835; --border:rgba(255,255,255,0.10);
  --s1:#3987e5; --s2:#d95926; --s3:#199e70; --s4:#c98500; --s5:#d55181;
  --s6:#008300; --s7:#9085e9; --s8:#e66767;
  --good:#0ca30c; --bad:#e66767; --accent:#3987e5;
}
*{box-sizing:border-box}
body{margin:0;background:var(--plane);color:var(--ink);
  font-family:system-ui,-apple-system,"Segoe UI",sans-serif;font-size:14px;line-height:1.45;-webkit-font-smoothing:antialiased}
.wrap{max-width:none;width:100%;margin:0;padding:22px clamp(16px,3vw,40px) 60px}
header.top{display:flex;flex-wrap:wrap;align-items:baseline;gap:8px 14px}
h1{font-size:21px;margin:0;font-weight:680;letter-spacing:-0.01em}
.sub{color:var(--ink-2);font-size:13px}
.src{color:var(--muted);font-size:12px;margin:2px 0 16px}
.controls{display:flex;flex-wrap:wrap;gap:12px;align-items:flex-end;margin-bottom:8px}
.field{display:flex;flex-direction:column;gap:5px;position:relative}
.field label{font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);font-weight:600}
.ms{font:inherit;color:var(--ink);background:var(--surface-2);border:1px solid var(--border);border-radius:8px;
  padding:8px 30px 8px 10px;min-width:230px;text-align:left;cursor:pointer;position:relative;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:320px}
.ms::after{content:"▾";position:absolute;right:10px;color:var(--muted)}
.ms:focus{outline:2px solid var(--accent);outline-offset:1px}
select,button.tog{font:inherit;color:var(--ink);background:var(--surface-2);border:1px solid var(--border);border-radius:8px;padding:8px 10px;cursor:pointer}
.seg{display:inline-flex;border:1px solid var(--border);border-radius:8px;overflow:hidden;background:var(--surface-2)}
.seg button{font:inherit;font-size:13px;background:none;border:none;color:var(--ink-2);padding:8px 13px;cursor:pointer;border-right:1px solid var(--border)}
.seg button:last-child{border-right:none}
.seg button[aria-pressed=true]{background:var(--accent);color:#fff;font-weight:600}
.pop{position:absolute;top:100%;left:0;margin-top:4px;z-index:40;background:var(--surface-2);border:1px solid var(--border);
  border-radius:10px;box-shadow:0 10px 34px rgba(0,0,0,.22);width:340px;max-width:88vw;padding:8px;display:none}
.pop.open{display:block}
.pop .sr{width:100%;padding:7px 9px;border:1px solid var(--border);border-radius:7px;background:var(--surface);color:var(--ink);font:inherit;margin-bottom:6px}
.pop .acts{display:flex;gap:8px;justify-content:space-between;margin-bottom:6px}
.pop .acts button{font:inherit;font-size:12px;background:none;border:none;color:var(--accent);cursor:pointer;padding:2px 4px}
.opts{max-height:280px;overflow:auto}
.opt{display:flex;align-items:center;gap:8px;padding:6px 7px;border-radius:6px;cursor:pointer;font-size:13px}
.opt:hover{background:color-mix(in srgb,var(--accent) 10%,transparent)}
.opt input{accent-color:var(--accent);width:15px;height:15px;flex:none}
.opt .rg{margin-left:auto;font-size:11px;color:var(--muted)}
.opt.nodata{opacity:.5}
.kpis{display:flex;flex-wrap:wrap;gap:12px;margin:16px 0 20px}
.kpi{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:12px 14px;min-width:140px;flex:1}
.kpi .k{font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);font-weight:600}
.kpi .v{font-size:23px;font-weight:700;letter-spacing:-0.02em;margin-top:3px}
.kpi .m{font-size:12px;color:var(--ink-2);margin-top:2px}
.card{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:16px 18px;margin-bottom:18px}
.card h2{font-size:14px;margin:0 0 2px;font-weight:650}
.card .cap{font-size:12px;color:var(--muted);margin-bottom:10px}
.chart{width:100%;overflow-x:auto}
svg{display:block;max-width:100%}
.legend{display:flex;flex-wrap:wrap;gap:10px 14px;margin-top:10px}
.legend span{display:inline-flex;align-items:center;gap:6px;font-size:12px;color:var(--ink-2)}
.legend i{width:12px;height:12px;border-radius:3px;display:inline-block;flex:none}
.warn{font-size:12px;color:var(--bad);margin-top:8px}
.tt{position:fixed;pointer-events:none;z-index:60;background:var(--surface-2);border:1px solid var(--border);border-radius:8px;
  padding:8px 10px;font-size:12px;color:var(--ink);box-shadow:0 6px 22px rgba(0,0,0,.18);opacity:0;transition:opacity .08s;max-width:280px}
.tt b{font-weight:650}.tt .row{display:flex;justify-content:space-between;gap:14px;white-space:nowrap}
.tt .sw{display:inline-block;width:9px;height:9px;border-radius:2px;margin-right:6px}
table{border-collapse:collapse;width:100%;font-size:12px;font-variant-numeric:tabular-nums}
th,td{padding:6px 9px;text-align:right;border-bottom:1px solid var(--grid);white-space:nowrap}
th:first-child,td:first-child{text-align:left}
thead th{color:var(--muted);font-weight:600}
.cmp td:first-child{display:flex;align-items:center;gap:7px}
.cmp .sw{width:11px;height:11px;border-radius:3px;flex:none}
.tblwrap{max-height:440px;overflow:auto;border:1px solid var(--border);border-radius:10px}
.foot{color:var(--muted);font-size:12px;margin-top:26px;border-top:1px solid var(--border);padding-top:12px}
.nodata{padding:30px;text-align:center;color:var(--muted)}
.chhead{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap;margin-bottom:8px}
.viewseg{flex-wrap:wrap}
.viewhint{font-size:12px;color:var(--muted);margin-bottom:8px}
.splitctrl{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:8px}
.splitctrl select{font:inherit;color:var(--ink);background:var(--surface-2);border:1px solid var(--border);border-radius:8px;padding:8px 10px;min-width:220px;font-weight:600}
.splitgrid{display:grid;grid-template-columns:150px 1fr 1fr;gap:2px 10px;align-items:center}
.splitgrid .hd{font-size:12px;font-weight:650;color:var(--ink);padding:6px 0;position:sticky;top:0;background:var(--surface);border-bottom:1px solid var(--border)}
.splitgrid .hd i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:6px}
.splitgrid .oplbl{font-size:12px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.splitgrid .oplbl small{display:block;color:var(--muted);font-weight:400;font-size:10.5px}
.splitcell{border:1px solid var(--border);border-radius:9px;padding:6px 8px;background:var(--surface-2)}
.splitcell .st{font-size:10.5px;color:var(--ink-2);margin-bottom:3px}
.splitcell .st b{color:var(--ink);font-size:12.5px}
.splitcell.empty{opacity:.45;font-size:11px;color:var(--muted);text-align:center;padding:14px 0}
.smgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px}
.smcard{border:1px solid var(--border);border-radius:10px;padding:10px 12px;background:var(--surface-2)}
.smcard .nm{font-size:12px;font-weight:600;display:flex;align-items:center;gap:6px;margin-bottom:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.smcard .nm i{width:9px;height:9px;border-radius:2px;flex:none}
.smcard .st{font-size:11px;color:var(--ink-2);margin-bottom:6px}
.smcard .st b{color:var(--ink);font-size:14px}
.rankrow .tag{font-size:10px;font-weight:700;padding:1px 6px;border-radius:99px;margin-left:6px}
.tag.best{background:color-mix(in srgb,var(--good) 20%,transparent);color:var(--good)}
.tag.worst{background:color-mix(in srgb,var(--bad) 20%,transparent);color:var(--bad)}
.heatcell{stroke:var(--surface);stroke-width:1}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:2px 0 4px}
.chip{font-size:11px;background:color-mix(in srgb,var(--accent) 13%,transparent);color:var(--accent);border-radius:99px;padding:2px 9px;font-weight:600}
button.tog{padding:8px 12px}
@media(max-width:560px){.ms{min-width:150px}}
</style>

<div class="wrap">
  <header class="top">
    <h1>Painel Mini FMH — Comparativo</h1>
    <span class="sub">Escolha indicadores e operações · <span id="period"></span></span>
  </header>
  <div class="src">Fonte: aba <b>daily</b> (Mini FMH). <b>Indicadores</b> = Metric · <b>Operações</b> = Hub name · datas diárias.</div>

  <div class="controls">
    <div class="field">
      <label>Indicadores (coluna A)</label>
      <button class="ms" id="indBtn" aria-haspopup="true" aria-expanded="false">—</button>
      <div class="pop" id="indPop"></div>
    </div>
    <div class="field">
      <label>Operações (coluna D)</label>
      <button class="ms" id="opBtn" aria-haspopup="true" aria-expanded="false">—</button>
      <div class="pop" id="opPop"></div>
    </div>
    <div class="field">
      <label>Tipo (coluna E)</label>
      <div class="seg" id="tipoSeg"></div>
    </div>
    <div class="field">
      <label>Mês</label>
      <div class="seg" id="monthSeg"></div>
    </div>
    <div class="field">
      <label>&nbsp;</label>
      <button class="tog" id="tblbtn" aria-expanded="false">▤ Tabela diária</button>
    </div>
  </div>
  <div class="chips" id="chips"></div>

  <div class="kpis" id="kpis"></div>

  <div class="card">
    <div class="chhead">
      <div><h2 id="chTitle">Comparativo diário</h2><div class="cap" id="chCap"></div></div>
      <div class="seg viewseg" id="viewSeg"></div>
    </div>
    <div class="splitctrl" id="splitCtrl" hidden>
      <div class="field"><label>Indicador A · esquerda</label><select id="indA"></select></div>
      <div class="field"><label>Indicador B · direita</label><select id="indB"></select></div>
    </div>
    <div class="viewhint" id="viewHint"></div>
    <div class="chart" id="lineWrap"></div>
    <div class="legend" id="legend"></div>
    <div class="warn" id="warn"></div>
  </div>

  <div class="card">
    <h2>Resumo por série</h2>
    <div class="cap">Cada série = combinação Indicador × Operação selecionada.</div>
    <div class="tblwrap" style="max-height:none"><table class="cmp" id="cmpTbl"></table></div>
  </div>

  <div class="card" id="tblCard" hidden>
    <h2>Tabela diária</h2>
    <div class="cap">Valores por dia de cada série selecionada. Role para o lado para ver todas as datas.</div>
    <div class="tblwrap" id="tblWrap"></div>
  </div>

  <div class="foot">
    Dados reais da Página10 (01/jun–31/jul 2025). Operação “Overall” é a linha agregada da aba. Séries sem preenchimento na
    planilha aparecem vazias. Unidades diferentes (contagem vs %) compartilham o mesmo eixo — compare com atenção à escala.
  </div>
</div>
<div class="tt" id="tt"></div>

<script>
const DATA = __DATA__;
const SERIES=['--s1','--s2','--s3','--s4','--s5','--s6','--s7','--s8'];
const cssv=n=>getComputedStyle(document.body).getPropertyValue(n).trim();
const fmt=(v,u)=>v==null?'—':(u==='pct'?(Math.round(v*10)/10).toLocaleString('pt-BR',{maximumFractionDigits:1})+'%':Math.round(v).toLocaleString('pt-BR'));
const fmtK=v=>{if(v==null)return '—';const a=Math.abs(v);if(a>=1e6)return (v/1e6).toLocaleString('pt-BR',{maximumFractionDigits:1})+'M';if(a>=1e3)return (v/1e3).toLocaleString('pt-BR',{maximumFractionDigits:1})+'k';return Math.round(v).toLocaleString('pt-BR');};
const sum=a=>{let s=0,any=false;for(const v of a){if(v!=null){s+=v;any=true;}}return any?s:null;};
document.getElementById('period').textContent=DATA.period;

// state
let selInd=[], selOp=['__all'];
const indActive=DATA.indicators.map((it,i)=>i).filter(i=>DATA.indicators[i].active>0);
selInd=[indActive[0]];

// tipo (coluna E)
const MINI=new Set(DATA.miniHubs||[]);
let selTipo='all'; // 'all' | 'mini' | 'other'
function tipoOK(hub){ if(selTipo==='all')return true; const m=MINI.has(hub); return selTipo==='mini'?m:!m; }
function buildTipoSeg(){
  const el=document.getElementById('tipoSeg');
  const opts=[['all','Todos'],['mini','Mini FMH'],['other','Demais']];
  el.innerHTML=opts.map(o=>`<button data-t="${o[0]}">${o[1]}</button>`).join('');
  el.querySelectorAll('button').forEach(b=>b.onclick=()=>{ selTipo=b.dataset.t;
    // drop selected ops that no longer match tipo (keep Overall)
    selOp=selOp.filter(k=>k==='__all'||tipoOK(k));
    syncTipoSeg(); syncAll(); });
  syncTipoSeg();
}
function syncTipoSeg(){ document.querySelectorAll('#tipoSeg button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.t===selTipo))); }

// months
const MNAME={'01':'Janeiro','02':'Fevereiro','03':'Março','04':'Abril','05':'Maio','06':'Junho','07':'Julho','08':'Agosto','09':'Setembro','10':'Outubro','11':'Novembro','12':'Dezembro'};
const MONTHS=[...new Set(DATA.iso.map(d=>d.slice(0,7)))];
let selMonths=new Set(MONTHS);
let VIEW={idx:DATA.iso.map((_,i)=>i),labels:DATA.labels.slice()};
function computeView(){ if(!selMonths.size)selMonths=new Set(MONTHS);
  const idx=[]; DATA.iso.forEach((d,i)=>{ if(selMonths.has(d.slice(0,7)))idx.push(i); });
  VIEW={idx, labels: idx.map(i=>DATA.labels[i])}; }
function buildMonthSeg(){
  const el=document.getElementById('monthSeg');
  let btns=[`<button data-m="__all">Tudo</button>`].concat(MONTHS.map(m=>`<button data-m="${m}">${MNAME[m.slice(5,7)]}</button>`));
  el.innerHTML=btns.join('');
  el.querySelectorAll('button').forEach(b=>b.onclick=()=>{
    const m=b.dataset.m;
    if(m==='__all'){ selMonths=new Set(MONTHS); }
    else{ // single-select behaviour: clicking a month isolates it; clicking again keeps it
      selMonths=new Set([m]); }
    syncMonthSeg(); syncAll();
  });
  syncMonthSeg();
}
function syncMonthSeg(){
  const all=selMonths.size===MONTHS.length;
  document.querySelectorAll('#monthSeg button').forEach(b=>{
    const m=b.dataset.m;
    b.setAttribute('aria-pressed', String(m==='__all'?all:(!all&&selMonths.has(m))));
  });
}

// operation has data for indicator?
function opSeries(indIdx, opKey){
  const it=DATA.indicators[indIdx];
  if(opKey==='__all') return {s:it.overall, has:it.overall.some(v=>v!=null)};
  const h=it.hubs.find(x=>x.hub===opKey);
  return {s:h?h.s:new Array(DATA.iso.length).fill(null), has:!!h};
}
// which ops have data across all indicators (for greying)
function opHasAny(opKey){
  if(opKey==='__all')return true;
  return DATA.indicators.some(it=>it.hubs.some(h=>h.hub===opKey));
}

// ---- multiselect popovers ----
function buildIndPop(){
  const pop=document.getElementById('indPop');
  let h='<input class="sr" placeholder="Buscar indicador…" id="indSr"><div class="acts"><button data-a="none">Limpar</button></div><div class="opts" id="indOpts"></div>';
  pop.innerHTML=h;
  renderIndOpts('');
  document.getElementById('indSr').addEventListener('input',e=>renderIndOpts(e.target.value));
  pop.querySelector('[data-a=none]').onclick=()=>{selInd=[];syncAll();};
}
function renderIndOpts(q){
  q=q.toLowerCase();
  const el=document.getElementById('indOpts');
  el.innerHTML=DATA.indicators.map((it,i)=>{
    if(q&&!it.m.toLowerCase().includes(q))return '';
    const dis=it.active===0;
    return `<label class="opt ${dis?'nodata':''}"><input type="checkbox" data-i="${i}" ${selInd.includes(i)?'checked':''}>${it.m}${dis?' · sem dados':''}</label>`;
  }).join('');
  el.querySelectorAll('input').forEach(inp=>inp.onchange=()=>{
    const i=+inp.dataset.i;
    if(inp.checked){if(!selInd.includes(i))selInd.push(i);} else selInd=selInd.filter(x=>x!==i);
    syncAll();
  });
}
function buildOpPop(){
  const pop=document.getElementById('opPop');
  pop.innerHTML='<input class="sr" placeholder="Buscar operação…" id="opSr"><div class="acts"><button data-a="all">Todas c/ dados</button><button data-a="none">Limpar</button></div><div class="opts" id="opOpts"></div>';
  renderOpOpts('');
  document.getElementById('opSr').addEventListener('input',e=>renderOpOpts(e.target.value));
  pop.querySelector('[data-a=none]').onclick=()=>{selOp=[];syncAll();};
  pop.querySelector('[data-a=all]').onclick=()=>{selOp=['__all'].concat(currentOpsWithData().slice(0,7));syncAll();};
}
// ops that have data in at least one selected indicator, ranked by total
function currentOpsWithData(){
  const idx=selInd.length?selInd:indActive;
  const tot={};
  idx.forEach(ii=>DATA.indicators[ii].hubs.forEach(h=>{ if(!tipoOK(h.hub))return; tot[h.hub]=(tot[h.hub]||0)+(sum(h.s)||0);}));
  return Object.keys(tot).sort((a,b)=>tot[b]-tot[a]);
}
function opLabel(k){ if(k==='__all')return 'Overall (agregado)'; const o=DATA.ops.find(x=>x.hub===k); return o?o.op:k; }
function renderOpOpts(q){
  q=q.toLowerCase();
  const el=document.getElementById('opOpts');
  let rows=[`<label class="opt"><input type="checkbox" data-k="__all" ${selOp.includes('__all')?'checked':''}><b>Overall (agregado)</b></label>`];
  DATA.ops.forEach(o=>{
    if(!tipoOK(o.hub))return;
    if(q&&!(o.op.toLowerCase().includes(q)||o.hub.toLowerCase().includes(q)))return;
    const dis=!opHasAny(o.hub);
    const badge=o.mini?'<span class="rg" style="color:var(--accent);font-weight:600">Mini FMH</span>':`<span class="rg">${o.reg||''}</span>`;
    rows.push(`<label class="opt ${dis?'nodata':''}"><input type="checkbox" data-k="${o.hub}" ${selOp.includes(o.hub)?'checked':''}>${o.op}${badge}</label>`);
  });
  el.innerHTML=rows.join('');
  el.querySelectorAll('input').forEach(inp=>inp.onchange=()=>{
    const k=inp.dataset.k;
    if(inp.checked){if(!selOp.includes(k))selOp.push(k);} else selOp=selOp.filter(x=>x!==k);
    syncAll();
  });
}
function toggle(btn,pop){ const open=pop.classList.contains('open');
  document.querySelectorAll('.pop').forEach(p=>p.classList.remove('open'));
  document.querySelectorAll('.ms').forEach(b=>b.setAttribute('aria-expanded','false'));
  if(!open){pop.classList.add('open');btn.setAttribute('aria-expanded','true');}
}
document.getElementById('indBtn').onclick=e=>{e.stopPropagation();toggle(e.target,document.getElementById('indPop'));};
document.getElementById('opBtn').onclick=e=>{e.stopPropagation();toggle(e.target,document.getElementById('opPop'));};
document.querySelectorAll('.pop').forEach(p=>p.onclick=e=>e.stopPropagation());
document.addEventListener('click',()=>document.querySelectorAll('.pop').forEach(p=>p.classList.remove('open')));

// ---- build series list from selection ----
function buildSeries(){
  const inds=selInd.length?selInd:[indActive[0]];
  const ops=selOp.length?selOp:['__all'];
  let list=[];
  inds.forEach(ii=>{ ops.forEach(ok=>{
    const it=DATA.indicators[ii]; const os=opSeries(ii,ok);
    const nm=(inds.length>1&&ops.length>1)?`${it.m} · ${opLabel(ok)}`:(inds.length>1?it.m:opLabel(ok));
    list.push({ind:ii,op:ok,unit:it.unit,s:os.s,name:nm,indName:it.m,opName:opLabel(ok)});
  });});
  return list;
}
let capped=0;
function activeSeries(){ computeView();
  let l=buildSeries().filter(se=>se.s.some(v=>v!=null));
  capped=Math.max(0,l.length-8);
  return l.slice(0,8).map((se,i)=>({...se,s:VIEW.idx.map(j=>se.s[j]),color:cssv(SERIES[i%8])})); }

function niceMax(m){if(m<=0)return 1;const p=Math.pow(10,Math.floor(Math.log10(m)));const n=m/p;const s=n<=1?1:n<=2?2:n<=2.5?2.5:n<=5?5:10;return s*p;}
function movavg(arr,w){ const h=Math.floor(w/2); return arr.map((v,i)=>{ if(v==null)return null; let s=0,c=0;
  for(let j=Math.max(0,i-h);j<=Math.min(arr.length-1,i+h);j++){ if(arr[j]!=null){s+=arr[j];c++;} } return c?s/c:null; }); }
function seAvg(s){ const nz=s.filter(v=>v!=null&&v!==0); return nz.length?nz.reduce((a,b)=>a+b,0)/nz.length:0; }
function lowerBetter(name){ return /Backlog|Turnover|Absente|Deviation|Deviaç|Desvio/i.test(name); }
const BLUE=['#cde2fb','#9ec5f4','#6da7ec','#3987e5','#256abf','#184f95','#0d366b'];
function blueAt(t){ t=Math.max(0,Math.min(1,t)); return BLUE[Math.round(t*(BLUE.length-1))]; }

const VIEWS=[['rank','Ranking'],['split','Lado a lado'],['smooth','Linha suavizada'],['multi','Pequenos múltiplos'],['heat','Mapa de calor'],['line','Linha diária']];
let chartMode='rank';
let indA=indActive[0], indB=(indActive[1]!==undefined?indActive[1]:indActive[0]);
const HINTS={
  rank:'Barras ordenadas: a operação no topo tem o maior valor no período. Quando todas as séries são do mesmo indicador, marco a melhor e a pior.',
  split:'Lado a lado: cada linha é uma operação; à esquerda o Indicador A, à direita o Indicador B. As operações vêm da seleção “Operações” acima. Cada lado tem sua própria escala.',
  smooth:'Média móvel de 7 dias — remove o serrilhado de fim de semana e mostra a tendência de cada operação.',
  multi:'Um mini-gráfico por operação, todos na mesma escala. Ideal para bater o olho e comparar formatos sem sobreposição.',
  heat:'Mapa de calor: cada linha é uma operação, cada coluna um dia. Quanto mais escuro, maior o valor. Fácil ver quem é forte e onde há falhas.',
  line:'Linhas diárias sobrepostas (cru).'
};
function buildIndAB(){
  const mk=el=>{ el.innerHTML=DATA.indicators.map((it,i)=>it.active>0?`<option value="${i}">${it.m}</option>`:'').join(''); };
  const a=document.getElementById('indA'),b=document.getElementById('indB');
  mk(a);mk(b); a.value=indA; b.value=indB;
  a.onchange=()=>{indA=+a.value;drawLine();};
  b.onchange=()=>{indB=+b.value;drawLine();};
}
function splitOps(){ let ops=(selOp.length?selOp:['__all']).filter(k=>k==='__all'||tipoOK(k)); return ops.slice(0,12); }
function sparkSVG(s,color,top,H){ H=H||44; const N=s.length,pad=4,W=240;
  const x=i=>pad+i*((W-2*pad)/(N-1)), y=v=>H-pad-(v/(top||1))*(H-2*pad);
  let d='',st=false,pk=null; s.forEach((v,i)=>{ if(v==null){st=false;return;} d+=(st?'L':'M')+x(i).toFixed(1)+' '+y(v).toFixed(1)+' '; st=true; if(pk==null||v>pk[0])pk=[v,i]; });
  let g=`<svg viewBox="0 0 ${W} ${H}" width="100%" height="${H}" preserveAspectRatio="none"><path d="${d}" fill="none" stroke="${color}" stroke-width="1.8" stroke-linejoin="round"/>`;
  if(pk)g+=`<circle cx="${x(pk[1]).toFixed(1)}" cy="${y(pk[0]).toFixed(1)}" r="2.6" fill="${color}"/>`;
  return g+'</svg>';
}
function splitSeries(){ // for summary/table: both sides
  const ops=splitOps(); const cA=cssv('--s1'),cB=cssv('--s2'); let out=[];
  [[indA,cA,'A'],[indB,cB,'B']].forEach(([ii,col,tag])=>{ const it=DATA.indicators[ii];
    ops.forEach(ok=>{ const s=VIEW.idx.map(j=>opSeries(ii,ok).s[j]); if(!s.some(v=>v!=null))return;
      out.push({ind:ii,op:ok,unit:it.unit,s,name:`${tag}: ${opLabel(ok)}`,indName:it.m,opName:opLabel(ok),color:col}); }); });
  return out;
}
function renderSplit(wrap){
  const ops=splitOps(); const itA=DATA.indicators[indA], itB=DATA.indicators[indB];
  const cA=cssv('--s1'),cB=cssv('--s2');
  // column maxes
  let maxA=0,maxB=0;
  ops.forEach(ok=>{ VIEW.idx.forEach(j=>{ const va=opSeries(indA,ok).s[j], vb=opSeries(indB,ok).s[j];
    if(va!=null&&va>maxA)maxA=va; if(vb!=null&&vb>maxB)maxB=vb; }); });
  let h=`<div class="splitgrid"><div class="hd">Operação</div><div class="hd"><i style="background:${cA}"></i>${itA.m}</div><div class="hd"><i style="background:${cB}"></i>${itB.m}</div>`;
  ops.forEach(ok=>{
    const sA=VIEW.idx.map(j=>opSeries(indA,ok).s[j]), sB=VIEW.idx.map(j=>opSeries(indB,ok).s[j]);
    const tA=sum(sA), tB=sum(sB);
    h+=`<div class="oplbl">${opLabel(ok)}</div>`;
    h+= sA.some(v=>v!=null)?`<div class="splitcell"><div class="st"><b>${fmt(tA,itA.unit)}</b> · ${fmt(seAvg(sA),itA.unit)}/dia</div>${sparkSVG(sA,cA,maxA)}</div>`:`<div class="splitcell empty">sem dados</div>`;
    h+= sB.some(v=>v!=null)?`<div class="splitcell"><div class="st"><b>${fmt(tB,itB.unit)}</b> · ${fmt(seAvg(sB),itB.unit)}/dia</div>${sparkSVG(sB,cB,maxB)}</div>`:`<div class="splitcell empty">sem dados</div>`;
  });
  h+='</div>'; wrap.innerHTML=h;
}
function buildViewSeg(){ const el=document.getElementById('viewSeg');
  el.innerHTML=VIEWS.map(v=>`<button data-v="${v[0]}">${v[1]}</button>`).join('');
  el.querySelectorAll('button').forEach(b=>b.onclick=()=>{ chartMode=b.dataset.v; syncViewSeg(); drawLine(); });
  syncViewSeg();
}
function syncViewSeg(){ document.querySelectorAll('#viewSeg button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.v===chartMode))); }

let geom=null;
function drawLine(){
  geom=null;
  computeView();
  const wrap=document.getElementById('lineWrap');
  const mlab = selMonths.size===MONTHS.length?DATA.period:[...selMonths].sort().map(m=>MNAME[m.slice(5,7)]).join(' + ');
  document.getElementById('viewHint').textContent=HINTS[chartMode]||'';
  document.getElementById('splitCtrl').hidden = chartMode!=='split';

  if(chartMode==='split'){
    const series=splitSeries();
    document.getElementById('warn').textContent='';
    document.getElementById('legend').innerHTML='';
    const nops=splitOps().length;
    document.getElementById('chTitle').textContent='Lado a lado — 2 indicadores';
    document.getElementById('chCap').textContent=`${nops} operação(ões) · ${DATA.indicators[indA].m} vs ${DATA.indicators[indB].m} · ${mlab}`;
    if(!nops){ wrap.innerHTML='<div class="nodata">Selecione ao menos uma operação acima.</div>'; drawCmp([]); buildTable([]); return; }
    renderSplit(wrap); drawCmp(series); buildTable(series); return;
  }

  document.getElementById('chTitle').textContent='Comparativo diário';
  const series=activeSeries();
  document.getElementById('warn').textContent=capped>0?`Mostrando as 8 primeiras séries (${capped} a mais ocultas). Refine a seleção.`:'';
  const units=[...new Set(series.map(s=>s.unit))];
  document.getElementById('chCap').textContent=`${series.length} série(s) · ${mlab}`+(units.length>1?' · atenção: mistura contagem e %':'');
  if(!series.length){ wrap.innerHTML='<div class="nodata">Selecione ao menos um indicador e uma operação com dados.</div>'; document.getElementById('legend').innerHTML=''; drawCmp([]); buildTable([]); return; }
  document.getElementById('legend').innerHTML=(series.length>1 && chartMode!=='rank' && chartMode!=='heat')?series.map(se=>`<span><i style="background:${se.color}"></i>${se.name}</span>`).join(''):'';
  if(chartMode==='rank') renderRank(series,wrap);
  else if(chartMode==='multi') renderMulti(series,wrap);
  else if(chartMode==='heat') renderHeat(series,wrap);
  else renderLines(series,wrap,chartMode==='smooth');
  drawCmp(series); buildTable(series);
}

function cw(wrap){ return Math.max(320, Math.floor((wrap&&wrap.clientWidth)||900)); }
function renderLines(series,wrap,smooth){
  const N=VIEW.labels.length;
  const data=series.map(se=>({...se, plot: smooth?movavg(se.s,7):se.s}));
  const m={t:14,r:16,b:34,l:56};
  const W=Math.max(m.l+m.r+N*9, cw(wrap)), H=Math.max(260,Math.min(360,Math.round(cw(wrap)*0.34)));
  let mx=0,mn=0; data.forEach(se=>se.plot.forEach(v=>{if(v!=null){if(v>mx)mx=v;if(v<mn)mn=v;}}));
  const top=niceMax(mx),bot=mn<0?-niceMax(-mn):0;
  const x=i=>m.l+i*((W-m.l-m.r)/(N-1)); const y=v=>m.t+(top-v)/(top-bot||1)*(H-m.t-m.b);
  const grid=cssv('--grid'),axis=cssv('--axis'),muted=cssv('--muted');
  let g=`<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-label="Comparativo diário">`;
  for(let t=0;t<=5;t++){const val=bot+(top-bot)*t/5,yy=y(val);
    g+=`<line x1="${m.l}" y1="${yy}" x2="${W-m.r}" y2="${yy}" stroke="${grid}" stroke-width="1"/>`;
    g+=`<text x="${m.l-8}" y="${yy+4}" text-anchor="end" font-size="11" fill="${muted}">${fmtK(val)}</text>`;}
  VIEW.labels.forEach((lb,i)=>{if(i%7===0||i===N-1){g+=`<line x1="${x(i)}" y1="${m.t}" x2="${x(i)}" y2="${H-m.b}" stroke="${grid}" stroke-width="1" opacity=".5"/>`;
    g+=`<text x="${x(i)}" y="${H-m.b+16}" text-anchor="middle" font-size="10" fill="${muted}">${lb}</text>`;}});
  data.forEach(se=>{let d='',st=false;se.plot.forEach((v,i)=>{if(v==null){st=false;return;}d+=(st?'L':'M')+x(i).toFixed(1)+' '+y(v).toFixed(1)+' ';st=true;});
    g+=`<path d="${d}" fill="none" stroke="${se.color}" stroke-width="${smooth?2.4:2}" stroke-linejoin="round" stroke-linecap="round"/>`;});
  if(bot<0)g+=`<line x1="${m.l}" y1="${y(0)}" x2="${W-m.r}" y2="${y(0)}" stroke="${axis}" stroke-width="1.5"/>`;
  g+=`<line id="cross" x1="0" y1="${m.t}" x2="0" y2="${H-m.b}" stroke="${axis}" stroke-width="1" opacity="0"/><g id="dots"></g>`;
  g+=`<rect id="hit" x="${m.l}" y="${m.t}" width="${W-m.l-m.r}" height="${H-m.t-m.b}" fill="transparent"/></svg>`;
  wrap.innerHTML=g; geom={W,H,m,N,x,y,series:data.map(se=>({...se,s:se.plot}))};
  attachHover(wrap.querySelector('svg'));
}

function renderRank(series,wrap){
  const rows=series.map(se=>({se,tot:sum(se.s)||0,avg:seAvg(se.s)}));
  const sameInd=new Set(series.map(s=>s.indName)).size===1;
  const lb=sameInd&&lowerBetter(series[0].indName);
  rows.sort((a,b)=> lb? a.tot-b.tot : b.tot-a.tot);
  const max=Math.max(...rows.map(r=>r.tot),1);
  const W=cw(wrap), lblW=Math.min(300,Math.max(180,Math.round(W*0.28))), rowH=34, barMax=Math.max(80,W-lblW-110), H=rows.length*rowH+8;
  const ink2=cssv('--ink-2');
  let g=`<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" class="bars" role="img" aria-label="Ranking">`;
  rows.forEach((r,i)=>{ const yy=i*rowH+6, w=Math.max(2,r.tot/max*barMax);
    const isBest=sameInd&&i===0, isWorst=sameInd&&i===rows.length-1&&rows.length>1;
    g+=`<text x="0" y="${yy+13}" font-size="12" fill="${cssv('--ink')}" font-weight="600">${i+1}. ${r.se.name.length>32?r.se.name.slice(0,31)+'…':r.se.name}</text>`;
    if(isBest||isWorst){const col=isBest?cssv('--good'):cssv('--bad');g+=`<text x="0" y="${yy+27}" font-size="10.5" fill="${col}" font-weight="700">${isBest?(lb?'▼ menor (melhor)':'▲ maior'):(lb?'▲ maior (pior)':'▼ menor')}</text>`;}
    g+=`<rect x="${lblW}" y="${yy+2}" width="${w}" height="${rowH-12}" rx="4" fill="${r.se.color}"/>`;
    g+=`<text x="${lblW+w+8}" y="${yy+15}" font-size="12" fill="${ink2}">${fmt(r.tot,r.se.unit)} <tspan fill="${cssv('--muted')}">· ${fmt(r.avg,r.se.unit)}/dia</tspan></text>`;
  });
  g+='</svg>'; wrap.innerHTML=g;
}

function renderMulti(series,wrap){
  const N=VIEW.labels.length;
  let gmax=0; series.forEach(se=>se.s.forEach(v=>{if(v!=null&&v>gmax)gmax=v;}));
  const top=niceMax(gmax);
  const W=240,H=64,pad=4;
  const x=i=>pad+i*((W-2*pad)/(N-1)); const y=v=>H-pad-(v/(top||1))*(H-2*pad);
  let html='<div class="smgrid">';
  series.slice().sort((a,b)=>(sum(b.s)||0)-(sum(a.s)||0)).forEach(se=>{
    let d='',ar='',st=false; se.s.forEach((v,i)=>{ if(v==null){st=false;return;} const cx=x(i),cy=y(v);
      d+=(st?'L':'M')+cx.toFixed(1)+' '+cy.toFixed(1)+' '; ar+=(st?'L':'M')+cx.toFixed(1)+' '+cy.toFixed(1)+' '; st=true; });
    // area baseline close
    let pk=null; se.s.forEach((v,i)=>{if(v!=null&&(pk==null||v>pk[0]))pk=[v,i];});
    let sv=`<svg viewBox="0 0 ${W} ${H}" width="100%" height="${H}" preserveAspectRatio="none">`;
    sv+=`<path d="${d}" fill="none" stroke="${se.color}" stroke-width="1.8" stroke-linejoin="round"/>`;
    if(pk)sv+=`<circle cx="${x(pk[1]).toFixed(1)}" cy="${y(pk[0]).toFixed(1)}" r="2.6" fill="${se.color}"/>`;
    sv+='</svg>';
    html+=`<div class="smcard"><div class="nm"><i style="background:${se.color}"></i>${se.name}</div>`+
      `<div class="st"><b>${fmt(sum(se.s),se.unit)}</b> total · ${fmt(seAvg(se.s),se.unit)}/dia · pico ${pk?fmt(pk[0],se.unit):'—'}</div>${sv}</div>`;
  });
  html+='</div>'; wrap.innerHTML=html;
}

function renderHeat(series,wrap){
  const N=VIEW.labels.length;
  const rows=series.slice().sort((a,b)=>(sum(b.s)||0)-(sum(a.s)||0));
  let gmax=0; rows.forEach(se=>se.s.forEach(v=>{if(v!=null&&v>gmax)gmax=v;}));
  const CW=cw(wrap), lblW=Math.min(240,Math.max(150,Math.round(CW*0.2))), rowH=22, totW=52;
  const cell=Math.max(6,(CW-lblW-totW)/N), H=rows.length*rowH+34, W=Math.max(CW,lblW+N*cell+totW);
  const muted=cssv('--muted');
  let g=`<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-label="Mapa de calor">`;
  VIEW.labels.forEach((lb,i)=>{ if(i%7===0||i===N-1){ g+=`<text x="${lblW+i*cell+cell/2}" y="12" text-anchor="middle" font-size="10" fill="${muted}">${lb}</text>`; } });
  rows.forEach((se,r)=>{ const yy=18+r*rowH;
    g+=`<text x="0" y="${yy+rowH/2+3}" font-size="11" fill="${cssv('--ink')}">${se.name.length>30?se.name.slice(0,29)+'…':se.name}</text>`;
    se.s.forEach((v,i)=>{ const xx=lblW+i*cell; const fill=(v==null)?'transparent':(v===0?cssv('--surface-2'):blueAt(gmax?v/gmax:0));
      g+=`<rect class="heatcell" x="${xx.toFixed(1)}" y="${yy}" width="${cell.toFixed(2)}" height="${rowH-3}" fill="${fill}"><title>${se.name} · ${VIEW.labels[i]}: ${v==null?'—':fmt(v,se.unit)}</title></rect>`; });
    g+=`<text x="${(lblW+N*cell+6).toFixed(1)}" y="${yy+rowH/2+3}" font-size="11" fill="${cssv('--ink-2')}">${fmtK(sum(se.s))}</text>`;
  });
  g+='</svg>'; wrap.innerHTML=g;
}
const tt=document.getElementById('tt');
function attachHover(svg){ if(!geom)return; const {m,x,y,N,series,W}=geom;
  const cross=svg.querySelector('#cross'),dots=svg.querySelector('#dots'),hit=svg.querySelector('#hit');
  function idx(evt){const r=svg.getBoundingClientRect();const sx=(evt.clientX-r.left)*(W/r.width);let i=Math.round((sx-m.l)/((W-m.l-m.r)/(N-1)));return Math.max(0,Math.min(N-1,i));}
  function move(evt){const i=idx(evt),cx=x(i);cross.setAttribute('x1',cx);cross.setAttribute('x2',cx);cross.setAttribute('opacity','1');
    let dd='';series.forEach(se=>{const v=se.s[i];if(v==null)return;dd+=`<circle cx="${cx}" cy="${y(v)}" r="4" fill="${se.color}" stroke="var(--surface)" stroke-width="2"/>`;});dots.innerHTML=dd;
    let rows=series.map(se=>({c:se.color,n:se.name,v:se.s[i],u:se.unit})).filter(o=>o.v!=null).sort((a,b)=>b.v-a.v);
    tt.innerHTML=`<b>${VIEW.labels[i]}</b>`+(rows.length?rows.map(o=>`<div class="row"><span><span class="sw" style="background:${o.c}"></span>${o.n}</span><b>${fmt(o.v,o.u)}</b></div>`).join(''):'<div class="muted">sem valor</div>');
    tt.style.opacity='1';const pad=14;let lx=evt.clientX+pad,ly=evt.clientY+pad;const b=tt.getBoundingClientRect();
    if(lx+b.width>innerWidth)lx=evt.clientX-b.width-pad;if(ly+b.height>innerHeight)ly=evt.clientY-b.height-pad;tt.style.left=lx+'px';tt.style.top=ly+'px';}
  hit.addEventListener('mousemove',move);
  hit.addEventListener('mouseleave',()=>{tt.style.opacity='0';cross.setAttribute('opacity','0');dots.innerHTML='';});
  hit.addEventListener('touchmove',e=>{move(e.touches[0]);e.preventDefault();},{passive:false});
}
function drawCmp(series){
  const el=document.getElementById('cmpTbl');
  if(!series.length){el.innerHTML='<tbody><tr><td class="nodata">—</td></tr></tbody>';return;}
  let h='<thead><tr><th>Série</th><th>Indicador</th><th>Operação</th><th>Total</th><th>Média/dia</th><th>Pico</th><th>Dia do pico</th></tr></thead><tbody>';
  series.forEach(se=>{const vals=se.s.map((v,i)=>[v,i]).filter(a=>a[0]!=null);const nz=vals.filter(a=>a[0]!==0);
    const t=sum(se.s);const avg=nz.length?nz.reduce((s,a)=>s+a[0],0)/nz.length:null;let pk=null;vals.forEach(a=>{if(pk==null||a[0]>pk[0])pk=a;});
    h+=`<tr><td><span class="sw" style="background:${se.color}"></span>${se.name}</td><td>${se.indName}</td><td>${se.opName}</td><td><b>${fmt(t,se.unit)}</b></td><td>${fmt(avg,se.unit)}</td><td>${pk?fmt(pk[0],se.unit):'—'}</td><td>${pk?VIEW.labels[pk[1]]:'—'}</td></tr>`;});
  h+='</tbody>';el.innerHTML=h;
}
function buildTable(series){
  const wrap=document.getElementById('tblWrap');
  if(!series.length){wrap.innerHTML='<div class="nodata">—</div>';return;}
  let h='<table><thead><tr><th>Série</th><th>Total</th>'+VIEW.labels.map(l=>`<th>${l}</th>`).join('')+'</tr></thead><tbody>';
  series.forEach(se=>{h+=`<tr><td>${se.name}</td><td><b>${fmt(sum(se.s),se.unit)}</b></td>`+se.s.map(v=>`<td>${v==null?'':fmt(v,se.unit)}</td>`).join('')+'</tr>';});
  h+='</tbody></table>';wrap.innerHTML=h;
}
function drawKpis(){
  const series=activeSeries();const el=document.getElementById('kpis');
  const inds=[...new Set(series.map(s=>s.ind))],ops=[...new Set(series.map(s=>s.op))];
  const grand=series.reduce((s,se)=>{const t=sum(se.s);return t==null?s:s+t;},0);
  const cards=[
    ['Indicadores',String(selInd.length||1),'selecionados'],
    ['Operações',String(selOp.length||1),'selecionadas'],
    ['Séries no gráfico',String(series.length),capped>0?`(+${capped} ocultas)`:'combinações'],
    ['Soma geral',fmtK(grand),'todas as séries (contagem)'],
  ];
  el.innerHTML=cards.map(c=>`<div class="kpi"><div class="k">${c[0]}</div><div class="v">${c[1]}</div><div class="m">${c[2]}</div></div>`).join('');
}
function syncBtns(){
  document.getElementById('indBtn').textContent=selInd.length?(selInd.length===1?DATA.indicators[selInd[0]].m:selInd.length+' indicadores'):'Nenhum';
  document.getElementById('opBtn').textContent=selOp.length?(selOp.length===1?opLabel(selOp[0]):selOp.length+' operações'):'Nenhuma';
  const chips=[]; selInd.slice(0,4).forEach(i=>chips.push(`<span class="chip">${DATA.indicators[i].m}</span>`)); if(selInd.length>4)chips.push(`<span class="chip">+${selInd.length-4}</span>`);
  selOp.slice(0,4).forEach(k=>chips.push(`<span class="chip">${opLabel(k)}</span>`)); if(selOp.length>4)chips.push(`<span class="chip">+${selOp.length-4}</span>`);
  document.getElementById('chips').innerHTML=chips.join('');
}
function syncAll(){ syncBtns(); drawKpis(); drawLine();
  const io=document.getElementById('indOpts'); if(io)renderIndOpts(document.getElementById('indSr').value||'');
  const oo=document.getElementById('opOpts'); if(oo)renderOpOpts(document.getElementById('opSr').value||''); }
document.getElementById('tblbtn').onclick=e=>{const c=document.getElementById('tblCard');const open=c.hidden;c.hidden=!open;e.target.setAttribute('aria-expanded',String(open));e.target.textContent=open?'▤ Ocultar tabela':'▤ Tabela diária';};
window.addEventListener('resize',()=>{clearTimeout(window._rz);window._rz=setTimeout(drawLine,150);});
buildIndPop();buildOpPop();buildTipoSeg();buildMonthSeg();buildViewSeg();buildIndAB();syncAll();
</script>'''
html=html.replace('__DATA__',data)
skeleton=('<!doctype html>\n<html lang="pt-BR">\n<head>\n'
  '<meta charset="utf-8">\n'
  '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
  '<meta name="description" content="Painel comparativo Mini FMH — indicadores diários da Página10 (junho–julho 2025).">\n'
  '</head>\n<body>\n'+html+'\n</body>\n</html>\n')
out=os.path.join(_root,'index.html')
open(out,'w').write(skeleton)
print('written',out,len(skeleton),'bytes')
