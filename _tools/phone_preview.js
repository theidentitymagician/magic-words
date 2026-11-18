// Paste into javascript_tool on ANY live page you own (same origin) to see it at phone width.
// Then take a screenshot / zoom on region [0,0,410,744]. Scroll the phone with:
//   document.getElementById('m').contentWindow.scrollTo(0, Y)
document.body.innerHTML=''; document.body.style.background='#bbb';
const f=document.createElement('iframe'); f.src=location.href; f.id='m';
f.style.cssText='width:390px;height:740px;border:0;margin:8px;background:#fff';
document.body.appendChild(f); 'ok'
