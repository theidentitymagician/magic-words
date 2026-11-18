const {chromium,devices}=require('playwright');const fs=require('fs');
const css=fs.readFileSync(__dirname+'/fonts.css','utf8');
const [,, file, out, w, h, sel, full] = process.argv;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:+w,height:+h},deviceScaleFactor:1});
await p.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.fulfill({status:200,contentType:'text/css',body:css}));
await p.route(/systeme|kasiarutkowiak\.com/,r=>r.abort());
await p.goto('file://'+file,{waitUntil:'load'});await p.addStyleTag({content:css});await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(600);
const ov=await p.evaluate(()=>document.documentElement.scrollWidth-window.innerWidth);
if(sel&&sel!=='-'){const el=await p.$(sel);await el.screenshot({path:out,type:'jpeg',quality:75});}
else await p.screenshot({path:out,fullPage:full==='1',type:'jpeg',quality:70});
console.log(out,'overflow',ov);await b.close();})();
