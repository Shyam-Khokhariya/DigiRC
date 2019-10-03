import GaugeWidget from'./gaugewidget';import MessageLogger from'../../../../fc-features/src/messagelogger';import AlertManager from'../../../../fc-features/src/alertmanager';import FusionCharts from'../../../../fc-core/src/constructor';import{pluck,pluckNumber,pluckFontSize,chartPaletteStr,BLANK}from'../../../../fc-core/src/lib';var UNDEF;class Gauge extends GaugeWidget{constructor(){super(),FusionCharts.addDep(MessageLogger),FusionCharts.addDep(AlertManager),this.chartLeftMargin=15,this.chartRightMargin=15,this.chartTopMargin=10,this.chartBottomMargin=10,this.minChartHeight=10,this.minCanvasWidth=0}_feedAxesRawData(){var a,b,c=this,d=c.getFromEnv('color-manager'),e=c.getFromEnv('dataSource'),f=e.chart,g=chartPaletteStr.chart2D,h=pluckNumber(f.ticksbelowgauge),i=pluckNumber(f.ticksonright),j=pluckNumber(f.axisontop,f.axisonleft===UNDEF?UNDEF:!pluckNumber(f.axisonleft),h===UNDEF?UNDEF:!h,i===UNDEF?UNDEF:i,c.isAxisOpposite),k=pluckNumber(f.reverseaxis,c.isAxisReverse),l=pluckNumber(f.showtickmarks,1),m=c.getFromEnv('number-formatter'),n=pluckNumber(f.showtickvalues);return b=!!(n||n===UNDEF)&&!!(l||n!==UNDEF),a={isVertical:!c.isHorizontal,isReverse:c.isHorizontal?k:!k,isOpposit:j,outCanfontFamily:pluck(f.outcnvbasefont,f.basefont,'Verdana,sans'),outCanfontSize:pluckFontSize(f.outcnvbasefontsize,f.basefontsize,10),outCancolor:pluck(f.outcnvbasefontcolor,f.basefontcolor,d.getColor(g.baseFontColor)).replace(/^#?([a-f0-9]+)/ig,'#$1'),useEllipsesWhenOverflow:f.useellipseswhenoverflow,divLineColor:pluck(f.vdivlinecolor,d.getColor(g.divLineColor)),divLineAlpha:pluck(f.vdivlinealpha,d.getColor('divLineAlpha')),divLineThickness:pluckNumber(f.vdivlinethickness,1),divLineIsDashed:!!pluckNumber(f.vdivlinedashed,f.vdivlineisdashed,0),divLineDashLen:pluckNumber(f.vdivlinedashlen,4),divLineDashGap:pluckNumber(f.vdivlinedashgap,2),showAlternateGridColor:pluckNumber(f.showalternatevgridcolor,0),alternateGridColor:pluck(f.alternatevgridcolor,d.getColor('altVGridColor')),alternateGridAlpha:pluck(f.alternatevgridalpha,d.getColor('altVGridAlpha')),numDivLines:f.numvdivlines,labelFont:f.labelfont,labelFontSize:f.labelfontsize,labelFontColor:f.labelfontcolor,labelFontAlpha:f.labelalpha,labelFontBold:f.labelfontbold,labelFontItalic:f.labelfontitalic,axisName:f.xaxisname,axisMinValue:m.getCleanValue(f.lowerlimit),axisMaxValue:m.getCleanValue(f.upperlimit),setAdaptiveMin:f.setadaptivemin,adjustDiv:f.adjusttm,labelDisplay:f.labeldisplay,showLabels:f.showlabels,rotateLabels:f.rotatelabels,slantLabel:pluckNumber(f.slantlabels,f.slantlabel),labelStep:pluckNumber(f.labelstep,f.xaxisvaluesstep),showAxisValues:pluckNumber(f.showxaxisvalues,f.showxaxisvalue),showDivLineValues:pluckNumber(f.showvdivlinevalues,f.showvdivlinevalues),showZeroPlane:f.showvzeroplane,zeroPlaneColor:f.vzeroplanecolor,zeroPlaneThickness:f.vzeroplanethickness,zeroPlaneAlpha:f.vzeroplanealpha,showZeroPlaneValue:f.showvzeroplanevalue,trendlineColor:f.trendlinecolor,trendlineToolText:f.trendlinetooltext,trendlineThickness:f.trendlinethickness,trendlineAlpha:f.trendlinealpha,showTrendlinesOnTop:f.showtrendlinesontop,showAxisLine:pluckNumber(f.showxaxisline,f.showaxislines,f.drawAxisLines,0),axisLineThickness:pluckNumber(f.xaxislinethickness,f.axislinethickness,1),axisLineAlpha:pluckNumber(f.xaxislinealpha,f.axislinealpha,100),axisLineColor:pluck(f.xaxislinecolor,f.axislinecolor,'#000000'),majorTMNumber:f.majortmnumber,majorTMColor:f.majortmcolor,majorTMAlpha:f.majortmalpha,majorTMHeight:f.majortmheight,tickValueStep:f.tickvaluestep,showTickMarks:f.showtickmarks,connectTickMarks:f.connecttickmarks,showTickValues:f.showtickvalues,majorTMThickness:f.majortmthickness,reverseScale:f.reversescale,showLimits:f.showlimits||b,minorTMNumber:pluckNumber(f.minortmnumber,c.minorTMNumber,4),minorTMColor:f.minortmcolor,minorTMAlpha:f.minortmalpha,minorTMHeight:pluckNumber(f.minortmheight,f.minortmwidth),minorTMThickness:f.minortmthickness,tickMarkDistance:pluckNumber(f.tickmarkdistance,f.tickmarkgap),tickValueDistance:pluckNumber(f.tickvaluedistance,f.displayvaluedistance),placeTicksInside:f.placeticksinside,placeValuesInside:f.placevaluesinside,upperLimitDisplay:f.upperlimitdisplay,lowerLimitDisplay:f.lowerlimitdisplay,drawTickMarkConnector:c.isHorizontal?1:0},a.vtrendlines=e.trendpoints,[a]}_setAxisLimits(){var a,b=this,c=b.getFromEnv('dataSource').chart,d=b.getChildren('scale')[0];a=b.getChildren('dataset')[0].getDataLimits(),a.max===-Infinity&&(a.max=0),a.min===1/0&&(a.min=0),b.colorRange&&d.setAxisConfig({axisMinValue:pluckNumber(c.lowerlimit,a.forceMin?a.min:UNDEF),axisMaxValue:pluckNumber(c.upperlimit,a.forceMax?a.max:UNDEF)}),d.setDataLimit(a.max,a.min)}_getDataJSON(){var a,b,c=0,d=[],e=[],f=[],g=this.getChildren('dataset')[0].components.data;for(a=g&&g.length?g.length:0;c<a;c+=1)b=g[c].config,d.push(b.itemValue),e.push(b.formatedVal||BLANK),f.push(b.toolText||BLANK);return{values:d,labels:e,toolTexts:f}}_postSpaceManagement(){var a=this,b=a.config,c=a.getChildren('canvas')[0],d=a.getChildren('scale')[0],e=a.isHorizontal,f=c.config;e?d.setAxisDimention({axisLength:b.canvasWidth,y:f.canvasTop+(d.config.isOpposit?0:f.canvasHeight),x:f.canvasLeft}):d.setAxisDimention({axisLength:b.canvasHeight,x:f.canvasLeft+(d.config.isOpposit?f.canvasWidth:0),y:f.canvasTop}),a.allocateDimensionOfChartMenuBar()}_clearChart(){}}export default Gauge;