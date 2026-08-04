"""Export swarm run traces as a self-contained HTML visualizer.

Usage:
    python3 -m swarm_brain.export_traces [output.html]

Runs three full-scenario traces — baseline, governed, and governed
with the DSL stubbed to a no-op (the G4 falsifiability condition) —
and writes a single double-clickable HTML file with the data embedded.
No server, no dependencies.
"""

import contextlib
import io
import json
import sys
from pathlib import Path

from phi_pi_e_interpreter import PhiPiEInterpreterFixed

from .baseline_swarm import BaselineSwarm
from .governed_swarm import GovernedSwarm
from .task_spec import make_scenario

MAX_ROUNDS = 60


def _trace_dict(trace, label, note):
    return {
        "label": label,
        "note": note,
        "rounds_used": trace.rounds_used,
        "terminated_early": trace.terminated_early,
        "completed": sorted(trace.completed),
        "refused": sorted(trace.refused),
        "total_flip_flops": trace.total_flip_flops,
        "total_voluntary_idles": trace.total_voluntary_idles,
        "total_dsl_calls": trace.total_dsl_calls,
        "attempts": dict(trace.attempts),
        "per_round": trace.per_round,
    }


def collect_traces():
    """Run the three demonstration traces on the full scenario."""
    baseline = BaselineSwarm(make_scenario(), MAX_ROUNDS).run()

    governed = GovernedSwarm(make_scenario(), MAX_ROUNDS).run()

    # G4 condition: stub the DSL, watch governance collapse
    original = PhiPiEInterpreterFixed.execute
    PhiPiEInterpreterFixed.execute = lambda self, code, context=None: None
    try:
        stubbed = GovernedSwarm(make_scenario(), MAX_ROUNDS).run()
    finally:
        PhiPiEInterpreterFixed.execute = original

    scenario = make_scenario()
    meta = {
        "num_agents": scenario.num_agents,
        "resources": scenario.resources,
        "tasks": {t.id: {"resources": t.resources, "duration": t.duration,
                         "deps": t.deps, "priority": t.priority}
                  for t in scenario.tasks.values()},
        "poison": sorted(scenario.poison_ids),
    }
    return meta, [
        _trace_dict(baseline, "Baseline (naive)",
                    "No Harmonia. Greedy claims, unbounded retry, "
                    "release-all backoff. Watch P retried forever and "
                    "C1/C2 flip-flop in perpetual livelock."),
        _trace_dict(governed, "Governed (Harmonia brain)",
                    "Every decision flows through interpreter.execute(): "
                    "ε-steps ARE progress, Λ observations drive refusal "
                    "and conflict resolution. P refused after 5 flat "
                    "observations; contention resolved by voluntary "
                    "yield; early termination."),
        _trace_dict(stubbed, "Governed, DSL stubbed (G4)",
                    "Same governed code with interpreter.execute() "
                    "no-op'd. Registers never move, so nothing counts "
                    "as progress: the swarm loses the ability to work. "
                    "The DSL is the brain, not a sticker."),
    ]


def build_html(meta, traces) -> str:
    data = json.dumps({"meta": meta, "traces": traces})
    return (_TEMPLATE
            .replace("__TITLE__", "HARMONIA Swarm Brain — Phase 1")
            .replace("__DATA__", data))


def build_terrarium_html(meta, traces) -> str:
    """The field view: agents as individuated creatures on the complex
    plane (their actual @self register positions), moving over the real
    Λ coupling field. Governed + stubbed traces only — the baseline has
    no registers and therefore no field to move on."""
    field_traces = [t for t in traces if t["label"].startswith("Governed")]
    data = json.dumps({"meta": meta, "traces": field_traces})
    return (_TERRARIUM
            .replace("__TITLE__", "HARMONIA Terrarium — the field the AI moves on")
            .replace("__DATA__", data))


def main(out_path: str = "harmonia_swarm_viz.html",
         terrarium_path: str = "harmonia_terrarium.html"):
    with contextlib.redirect_stdout(io.StringIO()):
        meta, traces = collect_traces()
    html = build_html(meta, traces)
    Path(out_path).write_text(html, encoding="utf-8")
    print(f"wrote {out_path} ({len(html)//1024} KB)")
    thtml = build_terrarium_html(meta, traces)
    Path(terrarium_path).write_text(thtml, encoding="utf-8")
    print(f"wrote {terrarium_path} ({len(thtml)//1024} KB)")


_TEMPLATE = r"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>__TITLE__</title>
<style>
 body{background:#101418;color:#dde3ea;font:14px/1.45 -apple-system,'Segoe UI',sans-serif;margin:0;padding:16px}
 h1{font-size:18px;margin:0 0 4px}
 .sub{color:#8b97a5;font-size:12px;margin-bottom:12px}
 .tabs{display:flex;gap:8px;margin-bottom:10px;flex-wrap:wrap}
 .tab{padding:6px 12px;border:1px solid #2c3540;border-radius:6px;cursor:pointer;background:#161c23}
 .tab.on{background:#24445c;border-color:#4a90c4}
 .note{background:#161c23;border:1px solid #2c3540;border-radius:6px;padding:8px 12px;font-size:12.5px;color:#aab6c3;margin-bottom:10px}
 .wrap{display:flex;gap:14px;flex-wrap:wrap}
 canvas{background:#0b0e12;border:1px solid #2c3540;border-radius:8px}
 .side{width:330px;min-width:280px;flex:1}
 .ctrl{display:flex;gap:8px;align-items:center;margin:10px 0}
 button{background:#24445c;color:#dde3ea;border:1px solid #4a90c4;border-radius:6px;padding:5px 12px;cursor:pointer;font-size:13px}
 input[type=range]{flex:1}
 .stats{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:10px}
 .stat{background:#161c23;border:1px solid #2c3540;border-radius:6px;padding:6px 10px}
 .stat b{display:block;font-size:16px}
 .stat span{color:#8b97a5;font-size:11px}
 .log{background:#0b0e12;border:1px solid #2c3540;border-radius:6px;padding:8px;height:220px;overflow-y:auto;font-size:12px}
 .log div{padding:2px 0;border-bottom:1px solid #161c23}
 .e-refuse{color:#ff7b72}.e-idle{color:#ffb454}.e-flip{color:#ff7b72}
 .e-complete{color:#7ee787}.e-eps{color:#79c0ff}.e-claim{color:#8b97a5}
 .e-watch{color:#d2a8ff}.e-retry_blocked{color:#c76060}
 .legend{font-size:11px;color:#8b97a5;margin-top:6px}
</style></head><body>
<h1>__TITLE__</h1>
<div class="sub">Constrained allocation, 12 agents / 4 resources, poison task P + contention pair C1/C2 &nbsp;·&nbsp; every trace is deterministic and reproduced by the repo's test suite</div>
<div class="tabs" id="tabs"></div>
<div class="note" id="note"></div>
<div class="wrap">
 <div>
  <canvas id="cv" width="640" height="460"></canvas>
  <div class="ctrl">
   <button id="play">▶ play</button><button id="stepb">step</button>
   <input type="range" id="slider" min="0" value="0">
   <span id="rlabel" style="min-width:90px"></span>
  </div>
  <div class="legend">circle = agent (green working · orange yielding · purple watching blocked task · grey idle) · square = resource · line = holding · P glows red until refused</div>
 </div>
 <div class="side">
  <div class="stats" id="stats"></div>
  <div class="log" id="log"></div>
 </div>
</div>
<script>
const DATA = __DATA__;
const meta = DATA.meta, traces = DATA.traces;
let ti = 0, ri = 0, playing = null;
const cv = document.getElementById('cv'), cx = cv.getContext('2d');

function tabs(){
  const el = document.getElementById('tabs'); el.innerHTML='';
  traces.forEach((t,i)=>{
    const d=document.createElement('div');
    d.className='tab'+(i===ti?' on':''); d.textContent=t.label;
    d.onclick=()=>{ti=i;ri=0;stop();tabs();render();};
    el.appendChild(d);
  });
  document.getElementById('note').textContent = traces[ti].note;
  const s=document.getElementById('slider');
  s.max = traces[ti].per_round.length-1; s.value=ri;
}
function agentPos(i,n){const a=-Math.PI/2+2*Math.PI*i/n;
  return [320+225*Math.cos(a), 235+185*Math.sin(a)];}
function resPos(i,n){return [320+(i-(n-1)/2)*90, 235];}

function render(){
  const tr = traces[ti], snap = tr.per_round[ri];
  document.getElementById('slider').value = ri;
  document.getElementById('rlabel').textContent =
    'round '+snap.r+' / '+tr.rounds_used;
  cx.clearRect(0,0,cv.width,cv.height);
  // resources
  meta.resources.forEach((r,i)=>{
    const [x,y]=resPos(i,meta.resources.length);
    cx.fillStyle='#2c3540'; cx.fillRect(x-22,y-16,44,32);
    cx.strokeStyle='#4a90c4'; cx.strokeRect(x-22,y-16,44,32);
    cx.fillStyle='#dde3ea'; cx.textAlign='center';
    cx.font='12px sans-serif'; cx.fillText(r,x,y+4);
  });
  // holding lines
  cx.lineWidth=1.6;
  Object.entries(snap.hold).forEach(([a,rs])=>{
    const [ax,ay]=agentPos(+a,meta.num_agents);
    rs.forEach(r=>{
      const i=meta.resources.indexOf(r), [rx,ry]=resPos(i,meta.resources.length);
      cx.strokeStyle='#4a90c4'; cx.beginPath();
      cx.moveTo(ax,ay); cx.lineTo(rx,ry); cx.stroke();
    });
  });
  // agents
  const evByAgent={};
  snap.ev.forEach(e=>{ if(e.a!==undefined) evByAgent[e.a]=e.t; });
  for(let i=0;i<meta.num_agents;i++){
    const [x,y]=agentPos(i,meta.num_agents);
    const task = snap.assign[String(i)];
    const watching = task && meta.tasks[task] &&
      meta.tasks[task].deps.some(d=>!(snap.done.includes(d)));
    let c='#3a4552';
    if(evByAgent[i]==='idle') c='#ffb454';
    else if(watching) c='#d2a8ff';
    else if(task) c='#7ee787';
    cx.fillStyle=c; cx.beginPath(); cx.arc(x,y,14,0,7); cx.fill();
    cx.fillStyle='#0b0e12'; cx.font='11px sans-serif';
    cx.fillText(i,x,y+4);
    if(task){ cx.fillStyle='#8b97a5'; cx.font='10px sans-serif';
      const dy = y<235?-22:30; cx.fillText(task,x,y+dy); }
  }
  // poison banner
  meta.poison.forEach(p=>{
    const refused = snap.ref.includes(p);
    cx.font='13px sans-serif'; cx.textAlign='left';
    cx.fillStyle = refused ? '#7ee787' : '#ff7b72';
    cx.fillText(refused ? ('☑ '+p+' REFUSED (bounded, permanent)')
                        : ('☠ '+p+' unsatisfiable — attempts ongoing'),
                12, 20);
  });
  cx.fillStyle='#8b97a5'; cx.font='12px sans-serif'; cx.textAlign='left';
  cx.fillText('done: '+snap.done.length+'/'+Object.keys(meta.tasks).length+
              '   DSL calls this round: '+snap.dsl, 12, cv.height-12);
  stats(); log();
}
function stats(){
  const tr=traces[ti], snap=tr.per_round[ri];
  let flips=0, idles=0, eps=0, dsl=0;
  for(let k=0;k<=ri;k++){ const s=tr.per_round[k];
    s.ev.forEach(e=>{ if(e.t==='flip')flips++; if(e.t==='idle')idles++;
                      if(e.t==='eps')eps++; });
    dsl+=s.dsl; }
  const el=document.getElementById('stats');
  el.innerHTML='';
  [['completed',snap.done.length],['refused',snap.ref.length],
   ['flip-flops',flips],['voluntary idles',idles],
   ['ε-steps',eps],['DSL calls',dsl]].forEach(([k,v])=>{
    const d=document.createElement('div'); d.className='stat';
    d.innerHTML='<b>'+v+'</b><span>'+k+'</span>'; el.appendChild(d);});
}
function log(){
  const tr=traces[ti], el=document.getElementById('log');
  el.innerHTML='';
  for(let k=Math.max(0,ri-7);k<=ri;k++){
    const s=tr.per_round[k];
    s.ev.forEach(e=>{
      const d=document.createElement('div');
      d.className='e-'+e.t;
      let msg='r'+s.r+' · '+e.t+(e.a!==undefined?' a'+e.a:'')+
              (e.task?' → '+e.task:'');
      if(e.why) msg+=' — '+e.why;
      d.textContent=msg; el.appendChild(d);
    });
  }
  el.scrollTop=el.scrollHeight;
}
function step(){ const n=traces[ti].per_round.length;
  if(ri<n-1){ri++;render();} else stop(); }
function stop(){ if(playing){clearInterval(playing);playing=null;
  document.getElementById('play').textContent='▶ play';} }
document.getElementById('play').onclick=()=>{
  if(playing){stop();return;}
  if(ri>=traces[ti].per_round.length-1) ri=0;
  playing=setInterval(step,600);
  document.getElementById('play').textContent='⏸ pause';};
document.getElementById('stepb').onclick=()=>{stop();step();};
document.getElementById('slider').oninput=e=>{stop();ri=+e.target.value;render();};
tabs(); render();
</script></body></html>
"""

_TERRARIUM = r"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>__TITLE__</title>
<style>
 body{background:#07090c;color:#dde3ea;font:14px/1.45 -apple-system,'Segoe UI',sans-serif;margin:0;padding:14px}
 h1{font-size:17px;margin:0 0 2px}
 .sub{color:#7d8a99;font-size:12px;margin-bottom:10px;max-width:900px}
 .tabs{display:flex;gap:8px;margin-bottom:8px}
 .tab{padding:5px 12px;border:1px solid #2c3540;border-radius:6px;cursor:pointer;background:#10151b;font-size:13px}
 .tab.on{background:#24445c;border-color:#4a90c4}
 .row{display:flex;gap:12px;flex-wrap:wrap}
 canvas{border:1px solid #232c36;border-radius:8px;background:#04060a}
 .ctrl{display:flex;gap:8px;align-items:center;margin:8px 0}
 button{background:#24445c;color:#dde3ea;border:1px solid #4a90c4;border-radius:6px;padding:5px 12px;cursor:pointer;font-size:13px}
 input[type=range]{flex:1}
 .panel{width:300px;min-width:260px}
 .box{background:#10151b;border:1px solid #232c36;border-radius:8px;padding:10px;margin-bottom:10px;font-size:12.5px}
 .box h3{margin:0 0 6px;font-size:13px;color:#8ec0e8}
 .mono{font-family:ui-monospace,monospace;font-size:11.5px;color:#9fb3c8}
 .legend{font-size:11px;color:#7d8a99;margin-top:4px;max-width:900px}
</style></head><body>
<h1>__TITLE__</h1>
<div class="sub">This plane is ℂ — the complex plane. Each creature's position IS its <b>@self</b> register; stars are <b>@goal</b> registers; the glowing landscape is the real Λ coupling field Λ(z,goals) computed live from the math core's formula (Λ=137/3). ε-steps move creatures by ≤0.001 — they physically cannot jump (that's the proven safety bound), so use the microscope. Φ-stabilization during conflict is the only large motion, and it is a proven contraction.</div>
<div class="tabs" id="tabs"></div>
<div class="row">
 <div>
  <canvas id="cv" width="920" height="420"></canvas>
  <div class="ctrl">
   <button id="play">▶ play</button><button id="stepb">step</button>
   <input type="range" id="slider" min="0" value="0">
   <span id="rlabel" style="min-width:90px"></span>
  </div>
  <div class="legend">click a creature to follow it (field re-centers on its goal; microscope engages) · click empty space to release · trails show the last 12 rounds of real register motion</div>
 </div>
 <div class="panel">
  <div class="box"><h3 id="mtitle">Microscope</h3>
   <canvas id="micro" width="276" height="180"></canvas>
   <div class="mono" id="minfo">select a creature</div></div>
  <div class="box"><h3>Creature</h3><div class="mono" id="ainfo">—</div></div>
 </div>
</div>
<script>
const DATA=__DATA__;const meta=DATA.meta,traces=DATA.traces;
const L=137/3;
let ti=0,ri=0,playing=null,sel=null;
const cv=document.getElementById('cv'),cx=cv.getContext('2d');
const mc=document.getElementById('micro'),mx=mc.getContext('2d');
// plane bounds from all recorded positions/goals
let B={x0:0,x1:13,y0:-1.6,y1:1.6};
(function(){let xs=[],ys=[];traces.forEach(t=>t.per_round.forEach(s=>{
 [s.z||{},s.g||{}].forEach(m=>Object.values(m).forEach(([x,y])=>{xs.push(x);ys.push(y);}));}));
 if(xs.length){B.x0=Math.min(...xs)-1;B.x1=Math.max(...xs)+1;
 B.y0=Math.min(...ys)-1;B.y1=Math.max(...ys)+1;}})();
const px=x=>(x-B.x0)/(B.x1-B.x0)*cv.width;
const py=y=>cv.height-(y-B.y0)/(B.y1-B.y0)*cv.height;
const hue=i=>i*137.5%360;
function lam(zr,zi,wr,wi){ // Λ(z,w) = Λ·2Re(z̄w)/(Λ+|z|²+|w|²)
 const re=zr*wr+zi*wi;
 return L*2*re/(L+zr*zr+zi*zi+wr*wr+wi*wi);}
function field(snap){
 const goals=sel!==null&&snap.g&&snap.g[sel]?[snap.g[sel]]:Object.values(snap.g||{});
 if(!goals.length)return;
 const gw=92,gh=42,cw=cv.width/gw,ch=cv.height/gh;
 let vals=[],mx0=0;
 for(let j=0;j<gh;j++)for(let i=0;i<gw;i++){
  const x=B.x0+(i+.5)/gw*(B.x1-B.x0),y=B.y0+(1-(j+.5)/gh)*(B.y1-B.y0);
  let v=0;goals.forEach(([wr,wi])=>v+=lam(x,y,wr,wi));
  vals.push(v);mx0=Math.max(mx0,Math.abs(v));}
 for(let j=0;j<gh;j++)for(let i=0;i<gw;i++){
  const v=vals[j*gw+i]/(mx0||1);
  const a=Math.abs(v);
  cx.fillStyle=v>=0?`rgba(40,110,190,${a*0.55})`:`rgba(190,70,110,${a*0.55})`;
  cx.fillRect(i*cw,j*ch,cw+1,ch+1);}
}
function trail(t,aid){
 const pts=[];
 for(let k=Math.max(0,ri-12);k<=ri;k++){
  const s=t.per_round[k];if(s.z&&s.z[aid])pts.push(s.z[aid]);}
 return pts;}
function render(){
 const t=traces[ti],snap=t.per_round[ri];
 document.getElementById('slider').value=ri;
 document.getElementById('rlabel').textContent='round '+snap.r+' / '+t.rounds_used;
 cx.clearRect(0,0,cv.width,cv.height);
 field(snap);
 // goals
 Object.entries(snap.g||{}).forEach(([a,[gxr,gyi]])=>{
  const x=px(gxr),y=py(gyi);
  cx.strokeStyle='#e8c86a';cx.lineWidth=1.4;
  cx.beginPath();for(let k=0;k<5;k++){const an=-Math.PI/2+k*4*Math.PI/5;
   cx[k?'lineTo':'moveTo'](x+8*Math.cos(an),y+8*Math.sin(an));}
  cx.closePath();cx.stroke();
  const task=snap.assign&&snap.assign[a];
  if(task){cx.fillStyle='#e8c86a';cx.font='10px sans-serif';
   cx.textAlign='center';cx.fillText(task,x,y-12);}});
 // creatures
 Object.entries(snap.z||{}).forEach(([a,[zr,zi]])=>{
  const x=px(zr),y=py(zi),h=hue(+a);
  const pts=trail(t,a);
  cx.strokeStyle=`hsla(${h},70%,60%,0.5)`;cx.lineWidth=1.2;
  cx.beginPath();pts.forEach(([tx,ty],k)=>cx[k?'lineTo':'moveTo'](px(tx),py(ty)));cx.stroke();
  const yielded=snap.ev.some(e=>e.t==='idle'&&e.a==+a);
  cx.fillStyle=`hsl(${h},70%,${yielded?35:60}%)`;
  cx.beginPath();cx.arc(x,y,sel==+a?9:7,0,7);cx.fill();
  if(sel==+a){cx.strokeStyle='#fff';cx.lineWidth=1.5;
   cx.beginPath();cx.arc(x,y,12,0,7);cx.stroke();}
  cx.fillStyle='#04060a';cx.font='9px sans-serif';cx.textAlign='center';
  cx.fillText(a,x,y+3);});
 micro();info();
}
function micro(){
 mx.clearRect(0,0,mc.width,mc.height);
 const t=traces[ti],snap=t.per_round[ri];
 document.getElementById('mtitle').textContent=
  sel===null?'Microscope':'Microscope — creature '+sel;
 if(sel===null||!snap.z||!snap.z[sel]){
  document.getElementById('minfo').textContent='select a creature to magnify its ε-motion';return;}
 const pts=trail(t,String(sel));
 if(pts.length<2){document.getElementById('minfo').textContent='no motion history yet';return;}
 let xs=pts.map(p=>p[0]),ys=pts.map(p=>p[1]);
 let x0=Math.min(...xs),x1=Math.max(...xs),y0=Math.min(...ys),y1=Math.max(...ys);
 const pad=Math.max((x1-x0),(y1-y0),1e-4)*0.25;
 x0-=pad;x1+=pad;y0-=pad;y1+=pad;
 const mpx=x=>(x-x0)/(x1-x0)*mc.width,mpy=y=>mc.height-(y-y0)/(y1-y0)*mc.height;
 const h=hue(sel);
 mx.strokeStyle=`hsl(${h},70%,60%)`;mx.lineWidth=1.5;
 mx.beginPath();pts.forEach(([tx,ty],k)=>mx[k?'lineTo':'moveTo'](mpx(tx),mpy(ty)));mx.stroke();
 pts.forEach(([tx,ty],k)=>{mx.fillStyle=k===pts.length-1?'#fff':`hsla(${h},70%,60%,0.7)`;
  mx.beginPath();mx.arc(mpx(tx),mpy(ty),k===pts.length-1?4:2.5,0,7);mx.fill();});
 let steps=[];for(let k=1;k<pts.length;k++){
  steps.push(Math.hypot(pts[k][0]-pts[k-1][0],pts[k][1]-pts[k-1][1]));}
 const last=steps[steps.length-1];
 document.getElementById('minfo').textContent=
  'window '+(x1-x0).toExponential(1)+' wide · last step |Δz| = '+
  (last?last.toExponential(2):'0')+
  (last&&last<=0.0011?'  (ε-bounded ✓)':last?'  (Φ jump / re-init)':'');
}
function info(){
 const t=traces[ti],snap=t.per_round[ri];
 const el=document.getElementById('ainfo');
 if(sel===null){el.textContent='click a creature — each is one agent: its own FieldContext, registers, trajectory';return;}
 const z=snap.z&&snap.z[sel],g=snap.g&&snap.g[sel];
 const task=snap.assign&&snap.assign[String(sel)];
 let s='agent '+sel+'\n';
 s+='task: '+(task||'(none)')+'\n';
 if(z)s+='@self = '+z[0].toFixed(4)+' + '+z[1].toFixed(4)+'i\n';
 if(g)s+='@goal = '+g[0].toFixed(4)+' + '+g[1].toFixed(4)+'i\n';
 if(z&&g)s+='|@self−@goal| = '+Math.hypot(z[0]-g[0],z[1]-g[1]).toFixed(4)+'\n';
 if(snap.lam&&snap.lam[sel]!==undefined)s+='λ_obs = '+snap.lam[sel];
 el.textContent=s;el.style.whiteSpace='pre';
}
cv.onclick=e=>{
 const r=cv.getBoundingClientRect();
 const mxp=e.clientX-r.left,myp=e.clientY-r.top;
 const snap=traces[ti].per_round[ri];let hit=null;
 Object.entries(snap.z||{}).forEach(([a,[zr,zi]])=>{
  if(Math.hypot(px(zr)-mxp,py(zi)-myp)<12)hit=+a;});
 sel=hit;render();};
function tabs(){const el=document.getElementById('tabs');el.innerHTML='';
 traces.forEach((t,i)=>{const d=document.createElement('div');
  d.className='tab'+(i===ti?' on':'');d.textContent=t.label;
  d.onclick=()=>{ti=i;ri=0;sel=null;stop();tabs();render();};el.appendChild(d);});
 document.getElementById('slider').max=traces[ti].per_round.length-1;}
function step(){if(ri<traces[ti].per_round.length-1){ri++;render();}else stop();}
function stop(){if(playing){clearInterval(playing);playing=null;
 document.getElementById('play').textContent='▶ play';}}
document.getElementById('play').onclick=()=>{
 if(playing){stop();return;}
 if(ri>=traces[ti].per_round.length-1)ri=0;
 playing=setInterval(step,700);
 document.getElementById('play').textContent='⏸ pause';};
document.getElementById('stepb').onclick=()=>{stop();step();};
document.getElementById('slider').oninput=e=>{stop();ri=+e.target.value;render();};
tabs();render();
</script></body></html>
"""

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "harmonia_swarm_viz.html",
         sys.argv[2] if len(sys.argv) > 2 else "harmonia_terrarium.html")
