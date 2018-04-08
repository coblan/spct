var com_date_range={
    props:['head','search_args'],
    data:function(){
        if(! this.search_args['_start_'+this.head.name]){
            Vue.set(this.search_args,'_start_'+this.head.name,'')
        }
        if(! this.search_args['_end_'+this.head.name]){
            Vue.set(this.search_args,'_end_'+this.head.name,'')
        }
        return {

        }
    },
    template:`<div  class="date-filter flex flex-ac">
                     <date v-model="search_args['_start_'+head.name]" :placeholder="head.label"></date>
                    <div style="display: inline-block;margin: 0 2px;" >-</div>
                        <date  v-model="search_args['_end_'+head.name]" :placeholder="head.label"></date>
                </div>`,

}
Vue.component('com-date-range-filter',com_date_range)

//var com_date_range={
//    props:['head','search_args'],
//    template:`<div  v-for='filter in heads' v-if="['time','date','month'].indexOf(filter.type)!=-1" class="date-filter flex flex-ac">
//                    <span v-text="filter.label"></span>
//                    <span>{From}</span>
//                    <div>
//                        <date v-if="filter.type=='month'" set="month" v-model="search['_start_'+filter.name]"></date>
//                        <date v-if="filter.type=='date'"  v-model="search['_start_'+filter.name]"></date>
//                    </div>
//                    <span>{To}</span>
//                    <div>
//                        <date v-if="filter.type=='month'" set="month" v-model="search['_end_'+filter.name]"></date>
//                        <date v-if="filter.type=='date'"  v-model="search['_end_'+filter.name]"></date>
//                    </div>
//                </div>`,
//
//}