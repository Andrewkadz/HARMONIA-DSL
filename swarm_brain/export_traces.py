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


def main(out_path: str = "harmonia_swarm_viz.html"):
    with contextlib.redirect_stdout(io.StringIO()):
        meta, traces = collect_traces()
    html = build_html(meta, traces)
    Path(out_path).write_text(html, encoding="utf-8")
    print(f"wrote {out_path} ({len(html)//1024} KB)")


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

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "harmonia_swarm_viz.html")
