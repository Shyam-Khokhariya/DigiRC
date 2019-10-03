import DataTable from'./datatable';import{addHandler,triggerEvent,removeHandler}from'./utils/event-handler';import{parseAndIndexData,createTableID,buildDateColumnsFormatter,parseData,indexData}from'./utils/datatable-utils';export default class DataStore{constructor(a,b,c){this.dataTables={},this._defaultDataTable=null,this._id=+new Date+'',a&&b&&a.constructor===Array&&b.constructor===Array&&this.createDataTable(a,b,c)}createDataTable(a,b,c,d){if(!a||!b)throw new Error('Both data and schema must be provided to build DataTable');if(a.constructor!==Array)throw new Error('Data must be provided in 2D array format or array of json objects');if(b.constructor!==Array||0===b.length)throw new Error('Input schema is not in a correct format - schema must be an array of column configurations');let e,f,g,h={};if(g=Object.keys(this.dataTables),!d)d=createTableID(g);else if(g.includes(d))throw new Error('A table with the id '+d+' already exists in the DataStore. Please use a different id.');return Object.assign(h,{enableIndex:!0,enableUTC:!1},c),e=parseAndIndexData(a,b,h),f=new DataTable(this,e,b,h,null,null,d),0===g.length&&(this._defaultDataTable=f),this.dataTables[d]=f,f}appendRows(a,b){let c,d,e,f=this.getDataTable(b);d=f.getSchema(),e=buildDateColumnsFormatter(d),c=parseData(a,d,e),f._data.push(...c),indexData(f._data,d,f._config,e),f._appendRows(c),this.trigger('itemsAdded',{rows:a,tableID:b})}getDataTable(a){if(a){if(!this.dataTables[a])throw new Error('DataTable with id '+a+' is not found in the DataStore.');return this.dataTables[a]}return this._defaultDataTable}on(a,b){addHandler(a,b,this)}off(a,b){removeHandler(a,b,this)}trigger(a,b){triggerEvent(a,this,b)}dispose(){var a=this;for(let b in a.dataTables)a.dataTables[b].dispose(),delete a.dataTables[b];delete a._id,delete a.dataTables,delete a._defaultDataTable,this.trigger('disposed'),a=null}_propagate(a){var b=this;for(let c in this.trigger('payloadReceived',a),b.dataTables)b.dataTables[c]._payloadReceiver(a)}}