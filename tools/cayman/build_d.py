"""Concept D, "Gearbox": concept A's four lights as the base, with B's rev counter, speedometer and H-pattern gate as a
small fixed instrument plate (the gate is also chapter navigation), and three WebGL effects on real <img>s:
rain on the windscreen (c2530), a gear-change speed blur on each chapter's first big photo, low-sun glare in April.
No intro. Prototype only (13 Oct 2026): concepts/cayman/d/index.html.

    python3 concepts/cayman/build_d.py
"""
import html
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_a as A  # noqa: E402  (reuse A's data, palette, pictures, captions, day line and base CSS)

P, E = A.P, html.escape
LIGHTS = A.LIGHTS
# chapter titles and lines from David's interview (notes/cayman-interview.md in the main checkout, 13 Oct 2026)
TITLES = {"rain": "Ready", "moor": "Wales", "april": "Low sun", "cabin": "Behind the wheel"}
CHAPTERS = [(c, d, t, TITLES[c], b) for c, d, t, _, b in A.CHAPTERS]
LINES = {
    "rain": "New tyres, new discs, new pads. Washed. Then it rained.",
    "moor": "Up at 3:00 and on the road to Wales. I got there just as the sun was rising: a beautiful sunrise and no traffic "
            "whatsoever. I drove the road up and down, twice, because I loved it so much, and was home by 10:00.",
    "cabin": "\u201cIt puts a smile on my face every single time I open the door.\u201d",
}
DAY = [("03:00", "moor", "leave"), ("06:14", "moor", "sunrise"), ("06:50", "april", ""), ("10:00", "moor", "home"),
       ("17:21", "cabin", ""), ("17:56", "rain", "")]


def dayline():
    marks = "".join(f'<li style="--x:{(int(t[:2]) * 60 + int(t[3:])) / 1440:.4f}" data-light="{c}"><span>{t}{(" " + w) if w else ""}</span></li>'
                    for t, c, w in DAY)
    hours = "".join(f'<li style="--x:{h / 24:.4f}">{h:02d}</li>' for h in (0, 6, 12, 18, 24))
    return f'<ol class="hours" aria-hidden="true">{hours}</ol><ol class="marks">{marks}</ol>'
NEEDLE = {"rain": "#e5443d", "moor": "#b3221d", "april": "#b3221d", "cabin": "#e5443d"}
# first big photo of each chapter gets the gear-change blur; c2530 also gets rain, c4846 the low sun
FIFTH = "c8706"   # 5th gear from this photo on
FX = {"c2530": "rain shift", "c2738": "shift", "c4846": "sun shift", "i3056": "sun", "c8464": "shift"}
SUN = {"i3056": (0.62, 0.575)}   # where the real sun is in the frame (x, y up, 0-1): the glare sits on it
CH_OF = {k: i + 1 for i, ch in enumerate(CHAPTERS) for b in ch[4] for k in b[1:]}


def fig(k, sizes, cls=""):
    pic = A.picture(k, sizes)
    attrs = ""
    if k in FX:
        tex = P[k]["src"]["1200"]["jpg"]
        pic = f'<div class="fxw">{pic}</div>'
        attrs = f' data-fx="{FX[k]}" data-tex="{tex}" data-ch="{CH_OF[k]}"'
        if k in SUN:
            attrs += f' data-sun="{SUN[k][0]},{SUN[k][1]}"'
    if k == FIFTH:
        attrs += ' data-gear="5"'
    return f'<figure class="ph {cls}" data-t="{P[k]["taken"]}"{attrs}>{pic}{A.cap(k)}</figure>'


def block(b):
    kind, *ks = b
    if kind == "full":
        return fig(ks[0], "100vw", "full")
    if kind == "end":
        return fig(ks[0], "100vw", "full end")
    if kind in ("offset-l", "offset-r"):
        return fig(ks[0], "(min-width:56rem) 62vw, 100vw", kind)
    if kind == "tall":
        return fig(ks[0], "(min-width:56rem) 40vw, 90vw", "tall")
    if kind == "pair":
        return '<div class="pair">' + "".join(fig(k, "(min-width:48rem) 48vw, 100vw") for k in ks) + "</div>"
    if kind == "trio":
        return '<div class="trio">' + "".join(fig(k, "(min-width:48rem) 32vw, 100vw") for k in ks) + "</div>"


# ---- instruments (static SVG, drawn once at build time; port of concept B's dial maths) ----
def pol(r, a):
    t = math.radians(a - 90)
    return 100 + r * math.cos(t), 100 + r * math.sin(t)


def arc(r, a0, a1):
    (x0, y0), (x1, y1) = pol(r, a0), pol(r, a1)
    return f"M{x0:.2f} {y0:.2f}A{r} {r} 0 {1 if a1 - a0 > 180 else 0} 1 {x1:.2f} {y1:.2f}"


def dial(kind):
    tach = kind == "tach"
    mx, major, minor = (8, 1, 0.5) if tach else (175, 25, 12.5)
    s = [f'<svg class="dial {kind}" viewBox="0 0 200 200" focusable="false">',
         '<circle class="ring" cx="100" cy="100" r="97"/>']
    if tach:
        s.append(f'<path class="red" d="{arc(94, -135 + 270 * 7 / 8, 135)}"/>')
    v = 0.0
    while v <= mx + 1e-6:
        a = -135 + 270 * v / mx
        big = abs(v / major - round(v / major)) < 1e-6
        (x0, y0), (x1, y1) = pol(91, a), pol(77 if big else 84, a)
        hot = tach and v >= 7
        s.append(f'<line class="{"ma" if big else "mi"}{" hot" if hot else ""}" x1="{x0:.2f}" y1="{y0:.2f}" x2="{x1:.2f}" y2="{y1:.2f}"/>')
        if big and (tach or v > 0):
            nx, ny = pol(62 if tach else 58, a)
            m = " m" if (tach or int(v) % 50 == 0) else ""
            s.append(f'<text class="num{m}" x="{nx:.2f}" y="{ny:.2f}">{int(v)}</text>')
        v += minor
    s.append(f'<text class="unit" x="100" y="{128 if tach else 130}">{"×1000 r/min" if tach else "mph"}</text>')
    s.append('<g class="needle" transform="rotate(-135 100 100)"><path d="M98.7 116 L99.55 18 L100.45 18 L101.3 116 Z"/></g>')
    s.append('<circle class="hub" cx="100" cy="100" r="7.5"/><circle class="cap" cx="100" cy="100" r="2.2"/></svg>')
    return "".join(s)


GP = {1: (14, 18), 2: (14, 58), 3: (38, 18), 4: (38, 58), 5: (62, 18), 6: (62, 58)}


def gate():
    s = ['<svg viewBox="0 0 76 76" aria-hidden="true" focusable="false">',
         '<path class="slot" d="M14 18V58M38 18V58M62 18V58M14 38H62"/>',
         '<path class="line" d="M14 18V58M38 18V58M62 18V58M14 38H62"/>']
    for g, label in ((5, "5"), (6, "R")):   # David's 987 2.7 is a five-speed: reverse sits where a sixth would be
        x, y = GP[g]
        s.append(f'<text class="{"off" if label == "R" else "off five"}" x="{x}" y="{y - 11 if y < 38 else y + 12}">{label}</text>')
    s.append('<circle class="knob" cx="0" cy="0" r="4.6" transform="translate(38 38)"/></svg>')
    links = []
    for i, (c, _, _, title, _) in enumerate(CHAPTERS, 1):
        x, y = GP[i]
        ty = y - 11 if y < 38 else y + 12
        links.append(f'<a href="#{c}" data-g="{i}" style="left:{x / 76 * 100:.2f}%;top:{(y + ty) / 2 / 76 * 100:.2f}%">'
                     f'<span class="n" aria-hidden="true">{i}</span><span class="sr">Gear {i}, {E(title)}</span>'
                     f'<span class="tip" aria-hidden="true">{E(title)}</span></a>')
    return "".join(s) + "".join(links)


CSS = A.CSS + """
.hr{display:flex;align-items:center;gap:1.4rem}
details.sm{position:relative}
details.sm summary{list-style:none;cursor:pointer;font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);padding:.4rem 0}
details.sm summary::-webkit-details-marker{display:none}
details.sm[open] summary{color:var(--ink)}
details.sm nav{position:absolute;right:0;top:calc(100% + .4rem);display:flex;flex-direction:column;min-width:12rem;padding:.4rem 1.1rem;background:var(--bg);border:1px solid color-mix(in srgb,var(--ink) 18%,transparent);border-radius:6px;box-shadow:0 12px 30px rgba(0,0,0,.18)}
details.sm nav a{font:500 .72rem/1 system-ui,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--ink);padding:.75rem 0}
details.sm nav a[aria-current=page]{text-decoration:underline;text-underline-offset:.3em}
footer{align-items:center}
footer nav{display:flex;flex-wrap:wrap;gap:.2rem 1.1rem}
footer a{display:inline-block;padding:.35rem 0;min-height:24px}
footer .next{font:300 1.25rem News,serif;text-decoration:none}
footer .next .lbl{margin-right:.6rem}
.hero h1{font-size:clamp(3.1rem,10.6vw,10.5rem);line-height:.9}
.opener .line{max-width:34rem;margin-top:1.2rem;font:300 clamp(1.15rem,2vw,1.45rem)/1.45 News,serif;color:var(--ink);transition:color var(--fade)}
.day .marks span{font-size:.62rem}
.day{margin-bottom:2.6rem}
.day .marks li:nth-child(4n+1) span{bottom:1.1rem;top:auto}
.day .marks li:nth-child(4n+2) span{bottom:auto;top:1.9rem}
.day .marks li:nth-child(4n+3) span{bottom:2.1rem;top:auto}
.day .marks li:nth-child(4n+4) span{bottom:auto;top:2.9rem}
@property --bg{syntax:'<color>';inherits:true;initial-value:#f4f2ec}
@property --ink{syntax:'<color>';inherits:true;initial-value:#1b1b1a}
@property --muted{syntax:'<color>';inherits:true;initial-value:#66645e}
@property --accent{syntax:'<color>';inherits:true;initial-value:#b3221d}
@property --needle{syntax:'<color>';inherits:true;initial-value:#b3221d}
html{transition:--bg var(--fade) ease,--ink var(--fade) ease,--muted var(--fade) ease,--accent var(--fade) ease,--needle var(--fade) ease;scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.fxw{position:relative}
.fxw canvas{position:absolute;inset:0;width:100%;height:100%;display:block;pointer-events:none;opacity:0}
.fxw canvas.on{opacity:1}
.inst{position:fixed;right:16px;bottom:14px;z-index:20;display:flex;align-items:center;gap:2px;padding:5px 6px 5px 5px;border-radius:18px;
 background:color-mix(in srgb,var(--bg) 88%,transparent);-webkit-backdrop-filter:blur(14px) saturate(1.2);backdrop-filter:blur(14px) saturate(1.2);
 border:1px solid color-mix(in srgb,var(--ink) 13%,transparent);box-shadow:0 14px 34px -18px rgb(0 0 0/.45)}
.dials{display:flex;gap:2px}
.dial{display:block;width:104px;height:104px;overflow:visible}
.dial .ring{fill:none;stroke:var(--ink);stroke-opacity:.18;stroke-width:1}
.dial .red{fill:none;stroke:var(--needle);stroke-width:3.2}
.dial .ma{stroke:var(--ink);stroke-width:2.6;stroke-linecap:round}
.dial .mi{stroke:var(--muted);stroke-width:1.3}
.dial .hot{stroke:var(--needle)}
.dial text{text-anchor:middle;dominant-baseline:central;font-family:Sans,system-ui,sans-serif}
.dial .num{fill:var(--ink);font-size:19px}
.speed .num{font-size:14px;letter-spacing:-.02em}
.dial .unit{fill:var(--muted);font-size:9.5px;letter-spacing:.08em}
.needle path{fill:var(--needle)}
.needle{filter:drop-shadow(0 0 1.5px color-mix(in srgb,var(--needle) 55%,transparent))}
.hub{fill:var(--ink)}.cap{fill:var(--needle)}
.gate{position:relative;width:84px;height:84px;margin-left:10px}
.gate svg{position:absolute;inset:0;width:100%;height:100%;overflow:visible}
.gate .slot{fill:none;stroke:var(--ink);stroke-opacity:.09;stroke-width:8;stroke-linecap:round;stroke-linejoin:round}
.gate .line{fill:none;stroke:var(--ink);stroke-opacity:.45;stroke-width:1;stroke-linecap:round}
.gate .off{fill:var(--muted);font:400 10.5px Sans,system-ui,sans-serif;text-anchor:middle;dominant-baseline:central;opacity:.75}
.gate .five{fill:var(--ink);opacity:.9}
.gate .knob{fill:var(--needle);stroke:var(--bg);stroke-width:1.5}
.gate a{position:absolute;width:24px;height:34px;transform:translate(-50%,-50%);display:flex;justify-content:center;
 text-decoration:none;color:var(--ink);font:400 11px/1 Sans,system-ui,sans-serif;border-radius:7px}
.gate a[data-g="1"],.gate a[data-g="3"]{align-items:flex-start;padding-top:5px}
.gate a[data-g="2"],.gate a[data-g="4"]{align-items:flex-end;padding-bottom:5px}
.gate a .n{border-bottom:1.5px solid transparent;padding:0 1px 1px}
.gate a[aria-current] .n{border-color:var(--needle)}
.gate a:hover{background:color-mix(in srgb,var(--ink) 8%,transparent)}
.gate a:focus-visible{outline-offset:0}
.tip{position:absolute;right:calc(100% + 2px);top:50%;transform:translateY(-50%);white-space:nowrap;padding:.3rem .55rem;border-radius:6px;
 background:var(--ink);color:var(--bg);font:400 .7rem/1 Sans,system-ui,sans-serif;letter-spacing:.06em;opacity:0;pointer-events:none;transition:opacity .2s}
.gate a:hover .tip,.gate a:focus-visible .tip{opacity:1}
footer{padding-bottom:10rem}
.clock{padding:8px 12px 9px;border-radius:16px;background:color-mix(in srgb,var(--bg) 88%,transparent);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);border:1px solid color-mix(in srgb,var(--ink) 13%,transparent)}
@media (max-width:44rem){
 .hero{padding-bottom:calc(9vh + 84px)}
 .inst{right:12px;bottom:12px;padding:3px 4px 3px 3px;border-radius:14px}
 .dial{width:64px;height:64px}
 .dial .num:not(.m){display:none}.speed .num{font-size:20px}.dial .num{font-size:23px}.dial .unit{display:none}
 .gate{width:80px;height:80px;margin-left:6px}
 .clock{left:12px;bottom:12px;padding:6px 9px 7px}
 .clock b{font-size:1.45rem}
}
@media (max-width:22rem){.dial{width:56px;height:56px}.gate{width:76px;height:76px}}
"""

JS = r"""
(()=>{'use strict';
const d=document,root=d.documentElement,RM=matchMedia('(prefers-reduced-motion: reduce)');
let reduce=RM.matches;
const NEEDLE=__NEEDLE__,IDS=__IDS__;
const chs=[...d.querySelectorAll('.chapter')],G5=d.querySelector('[data-gear="5"]'),END=d.querySelector('.ph.end');
const tachN=d.querySelector('.tach .needle'),spdN=d.querySelector('.speed .needle'),knob=d.querySelector('.knob');
const gl8=[...d.querySelectorAll('.gate a')];
const GP={0:[38,38],1:[14,18],2:[14,58],3:[38,18],4:[38,58],5:[62,18],6:[62,58]};
const SPD=[0,30,60,90,120,150];
const clamp=(v,a=0,b=1)=>v<a?a:v>b?b:v;
let gear=-1,rpm=850,rpmV=0,spd=0,spdV=0,kn=null,kp=[38,38],last=0,raf=0;
let lastY=scrollY,lastYT=performance.now(),vel=0;
const fxs=[];
const kick=()=>{if(!raf)raf=requestAnimationFrame(frame)};

/* ---- gearbox ---- */
function shift(from,to,now){
  gear=to;
  root.style.setProperty('--needle',NEEDLE[IDS[Math.min(to||4,4)-1]]);
  gl8.forEach(a=>{if(+a.dataset.g===to)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current')});
  const a=kp.slice(),b=GP[to]||GP[0],pts=[a];
  if(a[1]!==38)pts.push([a[0],38]);
  if(a[0]!==b[0])pts.push([b[0],38]);
  if(b[1]!==38)pts.push(b);
  let len=0;for(let i=1;i<pts.length;i++)len+=Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1]);
  if(reduce||from<0||len<1){kn=null;kp=b.slice();setKnob();return}
  kn={pts,len,t0:now,dur:Math.min(520,180+len*4)};
}
function setKnob(){knob.setAttribute('transform','translate('+kp[0].toFixed(2)+' '+kp[1].toFixed(2)+')')}
function knobStep(now){
  if(!kn)return false;
  let u=clamp((now-kn.t0)/kn.dur);u=u<.5?4*u*u*u:1-Math.pow(-2*u+2,3)/2;
  let s=u*kn.len;const P=kn.pts;
  for(let i=1;i<P.length;i++){const L=Math.hypot(P[i][0]-P[i-1][0],P[i][1]-P[i-1][1]);
    if(s<=L||i===P.length-1){const f=L?clamp(s/L):1;kp=[P[i-1][0]+(P[i][0]-P[i-1][0])*f,P[i-1][1]+(P[i][1]-P[i-1][1])*f];break}s-=L}
  setKnob();if(u>=1){kn=null;return false}return true;
}
function spring(x,v,t,k,z,dt){const a=k*(t-x)-2*z*Math.sqrt(k)*v;v+=a*dt;x+=v*dt;return[x,v]}

/* ---- WebGL ---- */
const VS='attribute vec2 p;varying vec2 v;void main(){v=p*.5+.5;gl_Position=vec4(p,0.,1.);}';
const FS=`precision highp float;varying vec2 v;
uniform sampler2D uTex,uMask;uniform vec2 uSize,uSun;uniform float uT,uBlur,uRain,uSunOn;
#define S(a,b,t) smoothstep(a,b,t)
float wet=1.;
vec3 N13(float p){vec3 p3=fract(vec3(p)*vec3(.1031,.11369,.13787));p3+=dot(p3,p3.yzx+19.19);return fract(vec3((p3.x+p3.y)*p3.z,(p3.x+p3.z)*p3.y,(p3.y+p3.z)*p3.x));}
float N(float t){return fract(sin(t*12345.564)*7658.76);}
float Saw(float b,float t){return S(0.,b,t)*S(1.,b,t);}
vec2 Layer(vec2 uv,float t){
 vec2 UV=uv;uv.y+=t*.75;vec2 a=vec2(6.,1.),grid=a*2.;vec2 id=floor(uv*grid);
 uv.y+=N(id.x);id=floor(uv*grid);vec3 n=N13(id.x*35.2+id.y*2376.1);
 vec2 st=fract(uv*grid)-vec2(.5,0.);float x=n.x-.5;float y=UV.y*20.;
 x+=sin(y+sin(y))*(.5-abs(x))*(n.z-.5);x*=.7;
 float ti=fract(t+n.z);y=(Saw(.85,ti)-.5)*.9+.5;
 float dd=length((st-vec2(x,y))*a.yx);float main=S(.4,0.,dd);
 float r=sqrt(S(1.,y,st.y));float cd=abs(st.x-x);
 float trail=S(.23*r,.15*r*r,cd);float front=S(-.02,.02,st.y-y);trail*=front*r*r;
 float yy=fract(UV.y*10.)+(st.y-.5);float dr=S(.3,0.,length(st-vec2(x,yy)));
 return vec2(main+dr*r*front,trail);
}
float Beads(vec2 uv,float t,float sc,float sd){
 uv*=sc;vec2 id=floor(uv);uv=fract(uv)-.5;vec3 n=N13(id.x*107.45+id.y*3543.654+sd);
 vec2 p=(n.xy-.5)*.7;float th=fract(n.z*7.31);float g=S(th*.8,th*.8+.2,wet);
 float d=length(uv-p)/max(g,.02);
 float fade=mix(1.,Saw(.025,fract(t+n.z)),.55);
 return S(.3,0.,d)*fract(n.z*10.)*fade*step(.02,g);
}
vec2 Drops(vec2 uv,float t){
 float s=Beads(uv,t*.5,34.,0.)+Beads(uv+3.7,t*.35,17.,17.)*.9;
 float run=S(.15,.9,wet);
 vec2 m1=Layer(uv,t)*run,m2=Layer(uv*1.85,t)*run;
 float tr=max(m1.y,m2.y);s*=1.-S(0.,.25,tr);
 return vec2(S(.3,1.,s+m1.x+m2.x),tr);
}
vec3 zoom(vec2 uv,float k){
 vec2 c=vec2(.5),dd=(uv-c)*(1.-.05*k);float j=fract(sin(dot(gl_FragCoord.xy,vec2(12.9898,78.233)))*43758.5453);
 vec3 acc=vec3(0.);float ws=0.;
 for(int i=0;i<18;i++){float t=(float(i)+j)/18.;float s=1.-k*.2*t;float w=1.-t*.55;float ca=k*.014*(.4+t);
  acc+=vec3(texture2D(uTex,c+dd*(s+ca)).r,texture2D(uTex,c+dd*s).g,texture2D(uTex,c+dd*(s-ca)).b)*w;ws+=w;}
 return acc/ws;
}
void main(){
 vec2 uv=v;vec3 col=vec3(0.);float a=0.;
 if(uBlur>.001){float ba=S(0.,.07,uBlur);col=zoom(uv,uBlur)*ba;a=ba;}
 if(uRain>.5){
  wet=1.-texture2D(uMask,uv).r;
  float fa=.24*S(0.,.7,wet);col=(texture2D(uTex,uv,3.2).rgb*1.03+.012)*fa+col*(1.-fa);a=fa+a*(1.-fa);
  vec2 g=(uv-.5)*uSize/860.;float t=uT*.2;
  vec2 c=Drops(g,t);vec2 e=vec2(.0011,0.);
  vec2 n=vec2(Drops(g+e,t).x-c.x,Drops(g+e.yx,t).x-c.x);
  vec3 Nn=normalize(vec3(-n*2.4,1.));
  vec3 r=texture2D(uTex,uv-Nn.xy*30./uSize,2.4).rgb;
  vec3 L=normalize(vec3(-.35,.6,.72));
  r*=1.+(dot(Nn,L)-L.z)*1.1;
  r*=mix(1.,.62,S(.55,.05,c.x));
  r+=pow(max(dot(reflect(-L,Nn),vec3(0.,0.,1.)),0.),48.)*.75;
  float da=c.x;col=r*da+col*(1.-da);a=da+a*(1.-da);
 }
 if(uSunOn>.5){
  vec2 asp=vec2(uSize.x/uSize.y,1.);vec2 p=(uv-uSun)*asp;float dd=dot(p,p);
  float fl=.92+.08*sin(uT*1.1)*sin(uT*.63+1.3);
  vec3 warm=vec3(1.,.8,.56);
  vec3 hb=texture2D(uTex,uv,4.).rgb;float L=dot(hb,vec3(.2126,.7152,.0722));
  vec3 gl=warm*(exp(-dd*7.)*.3+exp(-dd*70.)*.28)*fl+warm*S(.5,1.,L)*exp(-dd*2.5)*.35;
  vec2 ax=vec2(.5)-uSun;
  for(int i=0;i<3;i++){float f=1.35+float(i)*.42;vec2 gp=(uSun+ax*f*2.-uv)*asp;float rr=.025+float(i)*.03;
   gl+=vec3(.55+.2*float(i),.75,1.-.25*float(i))*S(rr,rr*.55,length(gp))*.045;}
  gl+=vec3(1.,.55,.3)*S(1.,0.,length((uv-vec2(uSun.x,1.15))*asp*vec2(.55,1.)))*.12*fl;
  float ga=max(gl.r,max(gl.g,gl.b));col+=gl;a=a+ga*(1.-a);
 }
 gl_FragColor=vec4(col,a);
}`;
const MS=`precision mediump float;varying vec2 v;uniform sampler2D uPrev;uniform float uDec,uAsp,uBr,uWOn;uniform vec2 uA,uB,uW;
void main(){float m=texture2D(uPrev,v).r-uDec;vec2 s=vec2(uAsp,1.),q=v*s,a=uA*s,ab=uB*s-a;
 float h=clamp(dot(q-a,ab)/max(dot(ab,ab),1e-6),0.,1.);m=max(m,uBr*smoothstep(.15,.08,length(q-a-ab*h)));
 if(uWOn>.5){vec2 pv=q-vec2(.5*uAsp,-.1);float r=length(pv),an=atan(pv.x,pv.y);
  m=max(m,step(min(uW.x,uW.y)-.03,an)*step(an,max(uW.x,uW.y)+.03)*smoothstep(.12,.2,r)*smoothstep(1.2,1.12,r));}
 gl_FragColor=vec4(clamp(m,0.,1.),0.,0.,1.);}`;

function prog(g,fs){const p=g.createProgram();for(const[t,s]of[[g.VERTEX_SHADER,VS],[g.FRAGMENT_SHADER,fs]]){const sh=g.createShader(t);g.shaderSource(sh,s);g.compileShader(sh);
  if(!g.getShaderParameter(sh,g.COMPILE_STATUS)&&!g.isContextLost())throw new Error(g.getShaderInfoLog(sh));g.attachShader(p,sh)}
  g.bindAttribLocation(p,0,'p');g.linkProgram(p);const u={};const n=g.getProgramParameter(p,g.ACTIVE_UNIFORMS);
  for(let i=0;i<n;i++){const k=g.getActiveUniform(p,i).name;u[k]=g.getUniformLocation(p,k)}return{p,u}}
function tex(g,src,mip){const t=g.createTexture();g.bindTexture(g.TEXTURE_2D,t);
  g.texParameteri(g.TEXTURE_2D,g.TEXTURE_WRAP_S,g.CLAMP_TO_EDGE);g.texParameteri(g.TEXTURE_2D,g.TEXTURE_WRAP_T,g.CLAMP_TO_EDGE);
  g.texParameteri(g.TEXTURE_2D,g.TEXTURE_MIN_FILTER,mip?g.LINEAR_MIPMAP_LINEAR:g.LINEAR);g.texParameteri(g.TEXTURE_2D,g.TEXTURE_MAG_FILTER,g.LINEAR);
  if(src.width){g.pixelStorei(g.UNPACK_FLIP_Y_WEBGL,true);g.texImage2D(g.TEXTURE_2D,0,g.RGBA,g.RGBA,g.UNSIGNED_BYTE,src);if(mip)g.generateMipmap(g.TEXTURE_2D)}
  else g.texImage2D(g.TEXTURE_2D,0,g.RGBA,src[0],src[1],0,g.RGBA,g.UNSIGNED_BYTE,null);return t}

function setup(f){
  const g=f.gl;f.main=prog(g,FS);
  const b=g.createBuffer();g.bindBuffer(g.ARRAY_BUFFER,b);g.bufferData(g.ARRAY_BUFFER,new Float32Array([-1,-1,3,-1,-1,3]),g.STATIC_DRAW);
  g.enableVertexAttribArray(0);g.vertexAttribPointer(0,2,g.FLOAT,false,0,0);
  if(f.pot)f.t=tex(g,f.pot,true);
  if(f.rain){f.mprog=prog(g,MS);const w=192,h=Math.max(16,Math.round(192/f.asp));f.ms=[w,h];
    f.mt=[tex(g,[w,h]),tex(g,[w,h])];f.fb=f.mt.map(t=>{const fb=g.createFramebuffer();g.bindFramebuffer(g.FRAMEBUFFER,fb);
      g.framebufferTexture2D(g.FRAMEBUFFER,g.COLOR_ATTACHMENT0,g.TEXTURE_2D,t,0);g.clearColor(0,0,0,1);g.clear(g.COLOR_BUFFER_BIT);return fb});
    g.bindFramebuffer(g.FRAMEBUFFER,null);f.mi=0}
}
function init(f){
  if(f.c||(reduce&&!f.rain&&!f.sun))return;  // reduce motion: rain and sun still render, as a still frame
  const c=f.c=d.createElement('canvas');c.setAttribute('aria-hidden','true');
  const o={alpha:true,premultipliedAlpha:true,antialias:false,depth:false,stencil:false,powerPreference:'high-performance'};
  const g=f.gl=c.getContext('webgl2',o)||c.getContext('webgl',o);
  if(!g){f.dead=true;return}
  f.wrap.appendChild(c);
  c.addEventListener('webglcontextlost',e=>{e.preventDefault();f.lost=true;c.classList.remove('on')});
  c.addEventListener('webglcontextrestored',()=>{try{setup(f);f.lost=false;f.lastAmt=-1;kick()}catch(e){f.dead=true}});
  try{setup(f)}catch(e){f.dead=true;c.remove();return}
  const im=new Image();im.decoding='async';im.src=f.src;
  im.decode().then(()=>{const p=d.createElement('canvas');p.width=p.height=1024;p.getContext('2d').drawImage(im,0,0,1024,1024);f.pot=p;
    if(!f.lost){f.t=tex(g,p,true);f.ready=true;f.lastAmt=-1;kick()}}).catch(()=>{f.dead=true});
}
function maskStep(f,dt,now){
  const g=f.gl,M=f.mprog;f.dec=(f.dec||0)+dt/7;let dec=0;if(f.dec>=2/255){dec=f.dec;f.dec=0}
  let wOn=0,w0=0,w1=0;
  if(f.wip){const u=clamp((now-f.wip.t0)/1150);const ang=x=>-1.5+2.95*(1-Math.cos(2*Math.PI*x))/2;
    w0=f.wip.a;w1=ang(u);f.wip.a=w1;wOn=1;if(u>=1)f.wip=null}
  const pa=f.pa||f.pb,pb=f.pb;const br=pb?1:0;
  const src=f.mi,dst=1-f.mi;
  g.bindFramebuffer(g.FRAMEBUFFER,f.fb[dst]);g.viewport(0,0,f.ms[0],f.ms[1]);g.useProgram(M.p);
  g.activeTexture(g.TEXTURE0);g.bindTexture(g.TEXTURE_2D,f.mt[src]);g.uniform1i(M.u.uPrev,0);
  g.uniform1f(M.u.uDec,dec);g.uniform1f(M.u.uAsp,f.asp);g.uniform1f(M.u.uBr,br);g.uniform1f(M.u.uWOn,wOn);
  g.uniform2f(M.u.uA,(pa||[0,0])[0],(pa||[0,0])[1]);g.uniform2f(M.u.uB,(pb||[0,0])[0],(pb||[0,0])[1]);g.uniform2f(M.u.uW,w0,w1);
  g.drawArrays(g.TRIANGLES,0,3);g.bindFramebuffer(g.FRAMEBUFFER,null);
  f.mi=dst;f.pa=pb;f.pb=null;
}
function draw(f,r,now,dt,vh){
  const g=f.gl,M=f.main;
  const dpr=Math.min(devicePixelRatio||1,f.rain?1.5:1.25);
  const W=Math.max(1,Math.round(r.width*dpr)),H=Math.max(1,Math.round(r.height*dpr));
  if(f.c.width!==W||f.c.height!==H){f.c.width=W;f.c.height=H}
  if(f.rain&&!reduce)maskStep(f,dt,now);
  if(f.sun){let tx,ty;if(f.anchor){tx=f.anchor[0]+(f.hover&&!reduce?(f.hover[0]-f.anchor[0])*.06:0);ty=f.anchor[1]+(f.hover&&!reduce?(f.hover[1]-f.anchor[1])*.06:0)}else if(f.hover&&!reduce){tx=f.hover[0];ty=f.hover[1]}else{const q=clamp((vh-r.top)/(vh+r.height));tx=.74-.1*q;ty=.98-.3*q}
    f.sp=f.sp?[f.sp[0]+(tx-f.sp[0])*Math.min(1,dt*3),f.sp[1]+(ty-f.sp[1])*Math.min(1,dt*3)]:[tx,ty]}
  g.viewport(0,0,W,H);g.useProgram(M.p);
  g.activeTexture(g.TEXTURE0);g.bindTexture(g.TEXTURE_2D,f.t);g.uniform1i(M.u.uTex,0);
  if(f.rain){g.activeTexture(g.TEXTURE1);g.bindTexture(g.TEXTURE_2D,f.mt[f.mi]);g.uniform1i(M.u.uMask,1)}
  g.uniform2f(M.u.uSize,r.width,r.height);g.uniform1f(M.u.uT,reduce?37:(now/1000)%1000);
  g.uniform1f(M.u.uBlur,f.shift?f.amt:0);g.uniform1f(M.u.uRain,f.rain?1:0);g.uniform1f(M.u.uSunOn,f.sun?1:0);
  if(f.sun)g.uniform2f(M.u.uSun,f.sp[0],f.sp[1]);
  g.clearColor(0,0,0,0);g.clear(g.COLOR_BUFFER_BIT);g.drawArrays(g.TRIANGLES,0,3);
  f.c.classList.add('on');
}

d.querySelectorAll('[data-fx]').forEach(fig=>{
  const k=fig.dataset.fx,img=fig.querySelector('img');
  const f={fig,wrap:fig.querySelector('.fxw'),anchor:fig.dataset.sun?fig.dataset.sun.split(',').map(Number):null,src:fig.dataset.tex,ch:+fig.dataset.ch,rain:k.includes('rain'),shift:k.includes('shift'),sun:k.includes('sun'),
    asp:+img.getAttribute('width')/+img.getAttribute('height'),amt:1,lastAmt:-1,lastWipe:-1e9};
  fxs.push(f);
  if(f.rain||f.sun){
    const uvOf=e=>{const r=f.wrap.getBoundingClientRect();return[clamp((e.clientX-r.left)/r.width),clamp(1-(e.clientY-r.top)/r.height)]};
    f.wrap.addEventListener('pointermove',e=>{const p=uvOf(e);if(f.rain)f.pb=p;if(f.sun)f.hover=p;kick()},{passive:true});
    f.wrap.addEventListener('pointerleave',()=>{f.pa=f.pb=null;f.hover=null;kick()});
  }
});
const near=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){const f=fxs.find(x=>x.fig===e.target);init(f);near.unobserve(e.target)}}),{rootMargin:'120% 0px'});
// WebGL waits for the reader's first scroll, touch or key: nothing heavy runs while the page loads
let armed=false;const arm=()=>{if(armed)return;armed=true;['scroll','pointerdown','touchstart','keydown','wheel'].forEach(t=>removeEventListener(t,arm));
  fxs.forEach(f=>{if(!reduce||f.rain||f.sun)near.observe(f.fig)})};
['scroll','pointerdown','touchstart','keydown','wheel'].forEach(t=>addEventListener(t,arm,{passive:true}));
if(scrollY>0)arm();

/* ---- frame ---- */
function frame(now){
  raf=0;const dt=last?Math.min(.05,(now-last)/1000):1/60;last=now;
  const vh=innerHeight;let g=0,p=0;
  for(let i=0;i<chs.length;i++){const r=chs[i].getBoundingClientRect();if(r.top<vh*.5){g=i+1;p=clamp((vh*.5-r.top)/r.height)}}
  // 4th through the cabin details, 5th once David is driving, neutral on the last photograph (David, 13 Oct 2026)
  if(g===4&&G5){const a=chs[3].getBoundingClientRect().top,b=G5.getBoundingClientRect().top;p=clamp((vh*.5-a)/Math.max(1,b-a));
    if(b<vh*.5){const e=END?END.getBoundingClientRect().top:b+vh;g=5;p=clamp((vh*.5-b)/Math.max(1,e-b))}}
  if(END&&END.getBoundingClientRect().top<vh*.5)g=0;
  const rs=fxs.map(f=>f.ready&&!f.lost&&!f.dead&&(!reduce||f.rain||f.sun)?f.wrap.getBoundingClientRect():null);
  if(g!==gear)shift(gear,g,now);
  let flare=0,live=false;
  fxs.forEach((f,i)=>{const r=rs[i];if(!r)return;
    const c=r.top+r.height/2;f.amt=reduce?0:clamp((c-vh/2)/(vh/2+r.height/2));const a=f.amt;f.amt=a*a*(3-2*a);
    if(f.ch===g&&f.amt>0&&f.amt<1)flare=Math.max(flare,Math.sin(Math.PI*f.amt));
    f.vis=r.bottom>0&&r.top<vh;
    if(!reduce&&f.rain&&f.vis&&!f.wip&&Math.abs(vel)>1.5&&now-f.lastWipe>1800&&(Math.min(r.bottom,vh)-Math.max(r.top,0))/r.height>.35){f.wip={t0:now,a:-1.5};f.lastWipe=now}});
  const rT=g?1500+5300*Math.pow(p,.92)-650*flare:850;
  const sT=g?SPD[g-1]+(SPD[g]-SPD[g-1])*(1-Math.pow(1-p,1.6)):0;
  if(reduce){rpm=rT;rpmV=0;spd=sT;spdV=0}else{[rpm,rpmV]=spring(rpm,rpmV,rT,140,.72,dt);[spd,spdV]=spring(spd,spdV,sT,30,1,dt)}
  tachN.setAttribute('transform','rotate('+(-135+270*clamp(rpm/8000)).toFixed(2)+' 100 100)');
  spdN.setAttribute('transform','rotate('+(-135+270*clamp(spd/175)).toFixed(2)+' 100 100)');
  if(knobStep(now))live=true;
  if(Math.abs(rpm-rT)>2||Math.abs(rpmV)>2||Math.abs(spd-sT)>.05||Math.abs(spdV)>.05)live=true;
  vel*=Math.pow(.02,dt);
  fxs.forEach((f,i)=>{const r=rs[i];if(!r||!f.vis)return;
    const anim=(f.rain||f.sun)&&!reduce;
    if(anim||f.amt!==f.lastAmt||(reduce&&!f.still)){draw(f,r,now,dt,vh);f.lastAmt=f.amt;if(reduce)f.still=true}
    if(anim)live=true});
  if(live)kick();else last=0;
}
addEventListener('scroll',()=>{const now=performance.now(),y=scrollY,dt=now-lastYT;if(dt>0){const v=(y-lastY)/dt;vel=vel*.6+v*.4}lastY=y;lastYT=now;kick()},{passive:true});
addEventListener('resize',kick);
RM.addEventListener('change',e=>{reduce=e.matches;fxs.forEach(f=>{f.still=false;if(f.c)f.c.hidden=reduce&&!f.rain&&!f.sun;if(armed&&!f.c&&(!reduce||f.rain||f.sun))near.observe(f.fig)});kick()});
kick();
})();
"""


def page_html(site=None):
    """The page. site=None: the local preview (concepts/cayman/d/, noindex). site={head, nav, name}: the live /cayman/."""
    chapters = []
    for c, date, t, title, blocks in CHAPTERS:
        body = "".join(block(b) for b in blocks)
        chapters.append(f'<section class="chapter" id="{c}" aria-labelledby="{c}-h"><div class="opener">'
                        f'<p class="lbl" data-t="{P[blocks[0][1]]["taken"][:11]}{t}:00">{date}</p><p class="t" aria-hidden="true">{t}</p>'
                        f'<h2 id="{c}-h">{title}<span class="sr"> · {t}</span></h2>{f"<p class=line>{LINES[c]}</p>" if c in LINES else ""}</div>{body}</section>')
    nav = "".join(f'<a href="#{c}">{title}</a>' for c, _, _, title, _ in CHAPTERS)
    ids = [c for c, *_ in CHAPTERS]
    js = JS.replace("__NEEDLE__", json.dumps(NEEDLE)).replace("__IDS__", json.dumps(ids))
    if site:
        headtags = (site["head"] + '\n<meta name="color-scheme" content="light">'
                    '\n<link rel="preload" as="font" type="font/woff2" href="/fonts/Newsreader-italic-300.woff2" crossorigin>')
        links = "".join(f'<a href="{h}"{" aria-current=page" if h == "/cayman/" else ""}>{n}</a>' for n, h in site["nav"])
        sitemenu = f'<details class="sm"><summary>Menu</summary><nav aria-label="Site menu">{links}</nav></details>'   # the other pages (David, 14 Oct 2026)
        foot = (f'<footer><a class="next" href="/"><span class="lbl">Next</span> From last light to last train</a>'
                f'<nav aria-label="Site">{links}</nav><span>All photographs \u00a9 {site["name"]}. Please ask before using them.</span>'
                f'<span class="legal" style="width:100%;font-size:12px;line-height:1.6">{site["legal"]}</span></footer>')
    else:
        headtags = """<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Back to analogue · My Cayman · David Silva</title>
<meta name="robots" content="noindex">
<meta name="color-scheme" content="light">
<link rel="preload" href="/site/fonts/Newsreader-normal-300.woff2" as="font" type="font/woff2" crossorigin>"""
        foot = '<footer><a href="/">David Silva · London</a><span class="lbl">Preview</span></footer>'
        sitemenu = ''
    doc = f"""<!doctype html>
<html lang="en-GB">
<head>{headtags}
<style>{CSS}</style></head>
<body>
<a class="skip" href="#rain">Skip to the photographs</a>
<header class="top"><a href="/">David Silva</a><div class="hr"><nav class="ch" aria-label="Chapters">{nav}</nav>{sitemenu}</div></header>
<div class="inst"><div class="dials" aria-hidden="true">{dial("tach")}{dial("speed")}</div><nav class="gate" aria-label="Gears">{gate()}</nav></div>
<main>
<section class="hero" aria-labelledby="t"><p class="lbl">My Cayman · Porsche 987 · 2007</p><h1 id="t">Back to analogue</h1>
<p>I was looking for a manual car, something with visceral feedback. Nineteen years old, a 2.7-litre engine and a manual gearbox. You need to be switched on, though, and that\u2019s the whole point.</p>
<div class="day" aria-label="The times in this story, on a 24-hour line">{dayline()}</div></section>
{"".join(chapters)}
<section class="sign" aria-label="End"><p>Back to analogue</p><p class="lbl">Photographs by David Silva · Nikon Z 6II</p></section>
</main>
<div class="clock" aria-hidden="true" hidden><b>00:00:00</b><span></span><i></i></div>
{foot}
<script>{A.JS.replace("__LIGHTS__", json.dumps(LIGHTS))}</script>
<script>{js}</script>
</body></html>
"""
    if site:
        doc = doc.replace("/site/images/", "/images/").replace("/site/fonts/", "/fonts/")
    return doc


def build():
    out = HERE.parents[1] / "concepts/cayman/d"
    out.mkdir(parents=True, exist_ok=True)
    doc = page_html()
    (out / "index.html").write_text(doc)
    print(out / "index.html", len(doc))


if __name__ == "__main__":
    build()
