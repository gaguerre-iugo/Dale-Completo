# -*- coding: utf-8 -*-
"""Puente EVA para el runtime de este bundle (build 19.2.4, minificado B).

Agrega window.__adtKit / __adtPlayer y el audio suelto para actividades,
usando los nombres internos de ESTE build. No reemplaza el runtime: lo
parchea de forma idempotente.

Uso: python tools/eva/patch_runtime_bridge_b.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BUNDLE = ROOT / "assets" / "base.bundle.local.js"
ANCHOR = "var Kv=R(F(),1),TK=640;"

BRIDGE = r"""/* eva-bridge-b:start */
window.__adtKit={
get(){let g=k=>Ce().get(k);return{
easyRead:g(Ka),readAloud:g(Ui),autoplay:g(zv),describeImages:g(qv),
highlight:g(Uv),voice:g(Av),speed:g(Gv),hideMenus:g(Qy),reduceMotion:g(Ra),playing:g(WB)}},
set(k,v){let m={easyRead:Ka,readAloud:Ui,autoplay:zv,describeImages:qv,
highlight:Uv,voice:Av,speed:Gv,hideMenus:Qy,reduceMotion:Ra};if(m[k])Ce().set(m[k],v)},
click(label){let r=document.getElementById("interface-container"),
b=r&&r.querySelector('button[aria-label="'+label+'"]');
if(!b){let l=document.querySelectorAll('button[aria-label="'+label+'"]');
for(let i=0;i<l.length;i++){if(!l[i].closest("#reflow-tts-player")){b=l[i];break}}}
if(!b)return false;b.click();return !b.disabled},
disabled(label){let b=document.querySelector('button[aria-label="'+label+'"]');return !b||b.disabled}};
window.__adtKit.playText=function(id){
try{
var audios=Ce().get(Tv)||{},voices=Ce().get(Qf),voice=Ce().get(Av);
var map=voices&&voices.voices&&voices.voices[voice]&&voices.voices[voice].audios;
if(!map||!Object.keys(map).length)map=audios;
var filename=map[id]||audios[id];
if(!filename)return false;
try{if(window.__adtKit.pauseReading)window.__adtKit.pauseReading();}catch(e){}
var a=window.__adtTextAudio;
if(!a){a=window.__adtTextAudio=new Audio();a.preload="auto";}
try{a.pause();}catch(e){}
try{a.currentTime=0;}catch(e){}
a.src="./content/i18n/"+Ce().get(An)+"/audio/"+filename;
a.playbackRate=Ce().get(Gv)||1;
var vol=Ce().get(Wv);
a.volume=Math.max(0,Math.min(1,vol==null?1:vol));
var p=a.play();if(p&&p.catch)p.catch(function(){});
return true;
}catch(e){return false;}};
window.__adtKit.stopText=function(){var a=window.__adtTextAudio;if(a){try{a.pause();a.currentTime=0;}catch(e){}}};
/* eva-player-api:start */
function __adtSilenceExtras(){
  try{if(window.speechSynthesis)window.speechSynthesis.cancel();}catch(e){}
  var a=window.__adtTextAudio;
  if(a){try{a.pause();}catch(e){}}
}
window.__adtKit.hasItems=function(){var p=window.__adtPlayer;return !!(p&&p.hasItems)};
window.__adtKit.playingReal=function(){var p=window.__adtPlayer;return !!(p&&p.hasItems&&!p.isPaused())};
window.__adtKit.play=function(){var p=window.__adtPlayer;if(!p||!p.hasItems)return false;__adtSilenceExtras();if(p.isPaused())p.play();return true};
window.__adtKit.pause=function(){var p=window.__adtPlayer;if(!p||!p.hasItems)return false;if(!p.isPaused())p.pause();__adtSilenceExtras();return true};
window.__adtKit.togglePlay=function(){var p=window.__adtPlayer;if(!p||!p.hasItems)return false;if(p.isPaused()){__adtSilenceExtras();p.play();}else{p.pause();__adtSilenceExtras();}return true};
window.__adtKit.stopKeep=function(){var p=window.__adtPlayer;if(!p||!p.hasItems)return false;p.pause();__adtSilenceExtras();return true};
window.__adtKit.pauseReading=function(){var p=window.__adtPlayer;if(p&&p.hasItems&&!p.isPaused()){p.pause();return true}return false};
(function(){try{var s=window.speechSynthesis;if(!s||s.__adtSpeakPatched)return;var orig=s.speak;
s.speak=function(){try{if(window.__adtKit&&window.__adtKit.pauseReading)window.__adtKit.pauseReading();}catch(e){}return orig.apply(s,arguments)};s.__adtSpeakPatched=true;}catch(e){}})();
/* eva-player-api:end */
/* eva-bridge-b:end */
"""

PLAYER_OLD = (
    ",{isPlaying:r,hasItems:Y.length>0,play:se,pause:fe,togglePlayPause:xe,"
    "playNext:be,playPrevious:de,stop:re,playAtIndex:ae}}var CU="
)
PLAYER_NEW = (
    ",(window.__adtPlayer={isPlaying:r,hasItems:Y.length>0,play:se,pause:fe,"
    "togglePlayPause:xe,playNext:be,playPrevious:de,stop:re,stopKeep:fe,"
    "isPaused:()=>{let $=e.current;return !$||$.paused},playAtIndex:ae})}var CU="
)

CLOSE_OLD = "(0,ot.useEffect)(()=>{w||(z.current=!1,V.current=null,ee(),a(!1),s(0))},[w,ee,a,s])"
CLOSE_NEW = (
    "(0,ot.useEffect)(()=>{if(w)return;z.current=!1;"
    "let adtA=e.current;if(adtA&&!adtA.paused)adtA.pause();ee(),a(!1)},[w,ee,a])"
)

VOICE_EFFECT_OLD = (
    "(0,ot.useEffect)(()=>{H.current!==p&&(H.current=p,x===y&&D.current===x&&(V.current=null,s(0)),ee(),a(!1))},[p,x,y,s,a,ee])"
)
VOICE_EFFECT_NEW = (
    "(0,ot.useEffect)(()=>{if(H.current===p)return;"
    "let adtJ=e.current,adtSeguia=!!(adtJ&&adtJ.src&&!adtJ.paused),"
    "adtT=adtJ&&adtJ.src?adtJ.currentTime:0;"
    "H.current=p;if(!adtJ||!adtJ.src)return;"
    "ae(i,adtT,adtSeguia)},[p,i])"
)

PLAY_INDEX_OLD = "let ae=(0,ot.useCallback)($=>{o.current=!0;"
PLAY_INDEX_NEW = "let ae=(0,ot.useCallback)(($,adtSeek,adtPlay)=>{o.current=!0;"

META_OLD = 'ie.onloadedmetadata=()=>{if(t.current&&t.current.mode==="word"&&!I[Q.id])'
META_NEW = (
    'ie.onloadedmetadata=()=>{'
    'if(typeof adtSeek==="number"&&isFinite(adtSeek)&&adtSeek>0){'
    'try{ie.currentTime=Math.min(adtSeek,Math.max(0,(ie.duration||adtSeek)-.05))}catch(adtE){}}'
    'if(t.current&&t.current.mode==="word"&&!I[Q.id])'
)

PLAY_OLD = (
    'Z(Q,ie),ie.play().then(()=>{U===n.current&&(u("tts"),a(!0))})'
    '.catch(he=>{U===n.current&&(console.warn("[adt-runtime] audio.play() rejected",he),q(),a(!1))})'
)
PLAY_NEW = (
    'Z(Q,ie),adtPlay!==!1&&('
    'typeof adtSeek==="number"&&isFinite(adtSeek)?'
    'ie.addEventListener("loadedmetadata",()=>{ie.play().then(()=>{U===n.current&&(u("tts"),a(!0))})'
    '.catch(he=>{U===n.current&&(console.warn("[adt-runtime] audio.play() rejected",he),q(),a(!1))})},{once:true}):'
    'ie.play().then(()=>{U===n.current&&(u("tts"),a(!0))})'
    '.catch(he=>{U===n.current&&(console.warn("[adt-runtime] audio.play() rejected",he),q(),a(!1))}))'
)


def replace_once(src, old, new, label):
    if src.count(old) != 1:
        raise SystemExit(f"ancla inesperada en {label}: {src.count(old)}")
    return src.replace(old, new, 1)


def main():
    src = BUNDLE.read_bytes().decode("utf-8")
    out = src

    if "/* eva-bridge-b:start */" not in out:
        out = replace_once(out, ANCHOR, BRIDGE + "\n" + ANCHOR, "puente EVA")
        print("puente EVA agregado")

    if "window.__adtPlayer=" not in out:
        out = replace_once(out, PLAYER_OLD, PLAYER_NEW, "API del reproductor")
        out = replace_once(out, CLOSE_OLD, CLOSE_NEW, "cierre sin reinicio")
        print("API del reproductor publicada")

    if "adtSeek" not in out:
        out = replace_once(out, PLAY_INDEX_OLD, PLAY_INDEX_NEW, "firma playAtIndex")
        out = replace_once(out, META_OLD, META_NEW, "seek en metadata")
        out = replace_once(out, PLAY_OLD, PLAY_NEW, "play condicionado")
        out = replace_once(out, VOICE_EFFECT_OLD, VOICE_EFFECT_NEW, "cambio de voz sin reinicio")
        print("cambio de voz continuo")

    if out == src:
        print("puente ya actualizado")
        return

    BUNDLE.write_bytes(out.encode("utf-8"))
    print("bundle parcheado:", len(src.encode("utf-8")), "->", len(out.encode("utf-8")), "bytes")


if __name__ == "__main__":
    main()
