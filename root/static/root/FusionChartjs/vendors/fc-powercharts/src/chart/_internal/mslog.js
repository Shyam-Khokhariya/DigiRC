import MSCartesian from'../../../../fc-charts/src/chart/_internal/mscartesian';import logAxisFactory from'../../factories/log-axis';import{pluckNumber,pluckFontSize,pluck,chartPaletteStr}from'../../../../fc-core/src/lib';class MsLog extends MSCartesian{constructor(){super(),this.registerFactory('axis',logAxisFactory,['canvas'])}static getName(){return'MsLog'}_feedAxesRawData(){var a,b,c=this,d=c.getFromEnv('dataSource'),e=c.getFromEnv('chart-attrib');return a=c.getSpecificxAxisConf(),b=c.getSpecificyAxisConf(),'1'===b.base&&(b.base=10,b.logBase=10),b.minorDivlinecolor=pluck(e.minordivlinecolor,b.divLineColor),b.minorDivLineThickness=pluck(e.minordivlinethickness,1),b.minorDivLineAlpha=pluck(e.minordivlinealpha,b.divLineAlpha/2),a.vtrendlines=d.vtrendlines,b.trendlines=d.trendlines,{yAxisConf:[b],xAxisConf:[a]}}getSpecificxAxisConf(){var a=this,b=a.getFromEnv('chart-attrib'),c=a.getBasexAxisConf();return c.showZeroPlane=b.showvzeroplane,c.zeroPlaneThickness=b.vzeroplanethickness,c.zeroPlaneAlpha=b.vzeroplanealpha,c.showAxisLine=pluckNumber(b.showxaxisline,b.showaxislines,b.drawAxisLines,0),c.axisLineColor=pluck(b.xaxislinecolor,b.axislinecolor,'#000000'),c.isReverse=!1,c.showAlternateGridColor=pluckNumber(b.showalternatevgridcolor,0),c.numDivLines=b.numvdivlines,c.maxLabelHeight=b.maxlabelheight,c.axisName=b.xaxisname,c.setAdaptiveMin=b.setadaptivexmin,c.showLimits=b.showvlimits,c.showDivLineValues=pluckNumber(b.showvdivlinevalues,b.showvdivlinevalues),c}getSpecificyAxisConf(){var a=this,b=a.getFromEnv('chart-attrib'),c=a.config.is3D,d=c?chartPaletteStr.chart3D:chartPaletteStr.chart2D,e=!!pluckNumber(b.invertyaxis,0),f=a.getFromEnv('color-manager');return{isVertical:!0,isReverse:!e,isOpposit:!1,outCanfontFamily:pluck(b.outcnvbasefont,b.basefont,'Verdana,sans'),outCanfontSize:pluckFontSize(b.outcnvbasefontsize,b.basefontsize,10),outCancolor:pluck(b.outcnvbasefontcolor,b.basefontcolor,f.getColor(d.baseFontColor)).replace(/^#? ([a-f0-9]+)/ig,'#$1'),axisNamePadding:b.yaxisnamepadding,axisValuePadding:b.yaxisvaluespadding,axisNameFont:b.yaxisnamefont,axisNameFontSize:b.yaxisnamefontsize,axisNameFontColor:b.yaxisnamefontcolor,axisNameFontBold:b.yaxisnamefontbold,axisNameFontItalic:b.yaxisnamefontitalic,axisNameBgColor:b.yaxisnamebgcolor,axisNameBorderColor:b.yaxisnamebordercolor,axisNameAlpha:b.yaxisnamealpha,axisNameFontAlpha:b.yaxisnamefontalpha,axisNameBgAlpha:b.yaxisnamebgalpha,axisNameBorderAlpha:b.yaxisnameborderalpha,axisNameBorderPadding:b.yaxisnameborderpadding,axisNameBorderRadius:b.yaxisnameborderradius,axisNameBorderThickness:b.yaxisnameborderthickness,axisNameBorderDashed:b.yaxisnameborderdashed,axisNameBorderDashLen:b.yaxisnameborderdashlen,axisNameBorderDashGap:b.yaxisnameborderdashgap,axisNameWidth:b.yaxisnamewidth,useEllipsesWhenOverflow:b.useellipseswhenoverflow,rotateAxisName:pluckNumber(b.rotateyaxisname,1),axisName:b.yaxisname,divLineColor:pluck(b.divlinecolor,f.getColor(d.divLineColor)),divLineAlpha:pluck(b.divlinealpha,f.getColor('divLineAlpha')),divLineThickness:pluckNumber(b.divlinethickness,2),divLineIsDashed:!!pluckNumber(b.divlinedashed,b.divlineisdashed,0),divLineDashLen:pluckNumber(b.divlinedashlen,4),divLineDashGap:pluckNumber(b.divlinedashgap,2),showAlternateGridColor:pluckNumber(b.showalternatehgridcolor,1),alternateGridColor:pluck(b.alternatehgridcolor,f.getColor('altHGridColor')),alternateGridAlpha:pluck(b.alternatehgridalpha,f.getColor('altHGridAlpha')),numDivLines:b.numdivlines,axisMinValue:b.yaxisminvalue,axisMaxValue:b.yaxismaxvalue,setAdaptiveMin:b.setadaptiveymin,adjustDiv:b.adjustdiv,labelStep:b.yaxisvaluesstep,showAxisValues:pluckNumber(b.showyaxisvalues,b.showyaxisvalue),showLimits:pluckNumber(b.showyaxislimits,b.showlimits,a.showLimits),showDivLineValues:pluckNumber(b.showdivlinevalues,b.showdivlinevalue),showZeroPlane:b.showzeroplane,zeroPlaneColor:b.zeroplanecolor,zeroPlaneThickness:b.zeroplanethickness,zeroPlaneAlpha:b.zeroplanealpha,showZeroPlaneValue:b.showzeroplanevalue,trendlineColor:b.trendlinecolor,trendlineToolText:b.trendlinetooltext,trendlineThickness:b.trendlinethickness,trendlineAlpha:b.trendlinealpha,showTrendlinesOnTop:b.showtrendlinesontop,showAxisLine:pluckNumber(b.showyaxisline,b.showaxislines,b.drawAxisLines,0),axisLineThickness:pluckNumber(b.yaxislinethickness,b.axislinethickness,1),axisLineAlpha:pluckNumber(b.yaxislinealpha,b.axislinealpha,100),base:b.base,logBase:b.logbase,axisLineColor:pluck(b.yaxislinecolor,b.axislinecolor,'#000000'),showMinorDivLineValues:pluckNumber(b.showminordivlinevalues,0),numMinorDivLines:b.numminordivlines}}}export default MsLog;