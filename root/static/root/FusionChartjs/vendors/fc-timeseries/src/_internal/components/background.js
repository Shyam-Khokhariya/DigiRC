import{SmartRenderer}from'../../../../fc-core/src/component-interface';class Background extends SmartRenderer{__setDefaultConfig(){this.config.backgroundCss={fill:'#ffffff'}}configureAttributes(a={}){super.configureAttributes(a);let b=this,c=b.config,d=b.getFromEnv('chart-attrib'),e=d.style&&d.style.background;Object.keys(a).forEach(b=>c[b]=a[b]),c.backgroundCss=Object.assign(c.backgroundCss,b.getFromEnv('getStyleDef')(e))}setDimension(a={}){Object.assign(this.config,a)}draw(){let a=this,b=a.config;a.addGraphicalElement({el:'rect',attr:{height:b.height,width:b.width,transform:b.translate,opacity:b.backgroundCss.opacity},container:{id:'tropo',label:'group',isParent:!0},css:b.backgroundCss,component:a,id:'background',label:'rect'})}}export default Background;