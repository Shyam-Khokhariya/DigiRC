export default{"initial.dataset.pie3d":function(){return{"group.appearing":a=>{let b=a.component,c=b.getFromEnv('chartConfig');return'plots'===a.attr.name?[{initialAttr:{opacity:'0'},finalAttr:{opacity:'1'},slot:c.alphaanimation?'plot':'initial'}]:[{initialAttr:{opacity:'1'},finalAttr:{opacity:'1'},slot:'final'}]},"slice.appearing":a=>{var b=Math.PI;let c=a.component,d=c.getFromEnv('chart'),e=d.config,f=c.config,g=a.attr;return e.alphaanimation?[{initialAttr:{opacity:'1'},slot:'plot'}]:f.animateClockWise?[{initialAttr:{sAngle:0,eAngle:0,transform:''},finalAttr:{sAngle:g.sAngle,eAngle:g.eAngle,transform:''},slot:'plot',startEnd:{start:0,end:.75}},{finalAttr:{transform:g.transform},slot:'plot',startEnd:{start:.75,end:1}}]:[{initialAttr:{sAngle:2*b,eAngle:2*b,transform:''},finalAttr:{sAngle:g.sAngle,eAngle:g.eAngle,transform:''},slot:'plot',startEnd:{start:0,end:.75}},{finalAttr:{transform:g.transform},slot:'plot',startEnd:{start:.75,end:1}}]},"label.updating":[{initialAttr:{opacity:'1'},finalAttr:{opacity:'1'},slot:'final'}],"label.appearing":[{initialAttr:{opacity:'0'},finalAttr:{opacity:'1'},slot:'final'}],"connector.updating":a=>[{initialAttr:{path:a.el.attr('path')||a.attr.path,opacity:a.el.attr('opacity')},finalAttr:{path:a.attr.path},slot:'final'}],"connector.appearing":a=>{let b;return b='string'==typeof a.el?{opacity:'0'}:{path:a.attr.path,opacity:'0'},[{initialAttr:b,slot:'final'}]},"connector-sliced.updating":a=>[{initialAttr:{path:a.el.attr('path')},finalAttr:{path:a.attr.path},slot:'plot'}],"label-sliced.updating":a=>[{initialAttr:{x:a.el.attr('x'),y:a.el.attr('y')},slot:'plot'}],"*":null}}};