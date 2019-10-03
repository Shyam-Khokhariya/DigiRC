const MONTHS_IN_YEAR=12,MILLISECOND='millisecond',SECOND='second',MINUTE='minute',HOUR='hour',DAY='day',MONTH='month',YEAR='year',GET='get',SET='set',MILLISECONDS_IN_SECOND=1e3,SECONDS_IN_MINUTE=60,MINUTES_IN_HOUR=60,HOURS_IN_DAY=24,DAYS_IN_MONTH=30,DAYS_IN_YEAR=365;function getFloorOfDate(a,b='day',c=1,d=''){var e,f=Math.floor,g=Math.min,h=new Date(a.valueOf());return b===MILLISECOND?(e=h[GET+d+'Milliseconds'](),c=g(c,MILLISECONDS_IN_SECOND),h[SET+d+'Milliseconds'](f(e/c)*c)):b===SECOND?(e=h[GET+d+'Seconds'](),c=g(c,SECONDS_IN_MINUTE),h[SET+d+'Seconds'](f(e/c)*c,0)):b===MINUTE?(e=h[GET+d+'Minutes'](),c=g(c,MINUTES_IN_HOUR),h[SET+d+'Minutes'](f(e/c)*c,0,0)):b===HOUR?(e=h[GET+d+'Hours'](),c=g(c,HOURS_IN_DAY),h[SET+d+'Hours'](f(e/c)*c,0,0,0)):b===DAY?(e=h[GET+d+'Date'](),c=g(c,31),h[SET+d+'Date'](Math.max(f(e/c)*c,1)),h[SET+d+'Hours'](0,0,0,0)):b===MONTH?(e=h[GET+d+'Month'](),c=g(c,MONTHS_IN_YEAR),h[SET+d+'Month'](f(e/c)*c,1),h[SET+d+'Hours'](0,0,0,0)):b===YEAR?(h[SET+d+'Month'](0,1),h[SET+d+'Hours'](0,0,0,0)):void 0,h}function modifyDate(a,b='day',c=1,d=!1,e=''){var f=new Date(a.valueOf());return b===MILLISECOND?f[SET+e+'Milliseconds'](f[GET+e+'Milliseconds']()+c):b===SECOND?(f[SET+e+'Seconds'](f[GET+e+'Seconds']()+c),d&&f[SET+e+'Milliseconds'](0)):b===MINUTE?(f[SET+e+'Minutes'](f[GET+e+'Minutes']()+c),d&&f[SET+e+'Seconds'](0,0)):b===HOUR?(f[SET+e+'Hours'](f[GET+e+'Hours']()+c),d&&f[SET+e+'Minutes'](0,0,0)):b===DAY?(f[SET+e+'Date'](f[GET+e+'Date']()+c),d&&f[SET+e+'Hours'](0,0,0,0)):b===MONTH?(f[SET+e+'Month'](f[GET+e+'Month']()+c),d&&f[SET+e+'Date'](0,0,0,0,0)):b===YEAR?(f[SET+e+'FullYear'](f[GET+e+'FullYear']()+c),d&&f[SET+e+'Month'](0,0,0,0,0,0)):void 0,f}export{getFloorOfDate,modifyDate,MILLISECONDS_IN_SECOND,SECONDS_IN_MINUTE,MINUTES_IN_HOUR,HOURS_IN_DAY,DAYS_IN_MONTH,DAYS_IN_YEAR};