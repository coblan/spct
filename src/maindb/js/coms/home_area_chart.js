Vue.component('com-home-area-chart',{
    props:['ctx'],
    data:function(){
        return {
            barRows: [],
        }
    },
    template:` <div class="chart" style="height:100%;width: 100%"></div>`,
    mounted:function(){
        this.myChart = echarts.init(this.$el);
        this.getRows()
    },
    methods:{
        getRows:function(){
            var self=this
            cfg.show_load()
            ex.director_call('trend_data',{key:this.ctx.key,merchant:search_args.merchant},function(resp){
                self.barRows=resp
                cfg.hide_load()
            })
        }
    },
    watch:{
        barRows:function(v){
            var self=this
            var x_data=ex.map(v,function(item){
                return item.time
            })
            var android=ex.map(v,function(item){
                return item.android
            })
            var unknown=ex.map(v,function(item){
                return item.unknown
            })
            var pc=ex.map(v,function(item){
                return item.pc
            })
            var h5=ex.map(v,function(item){
                return item.h5
            })
            var ios=ex.map(v,function(item){
                return item.ios
            })

            var option = {
                title: {
                },
                tooltip : {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'cross',
                        label: {
                            backgroundColor: '#6a7985'
                        }
                    }
                },
                legend: {
                    data:['Android','iOS','PC','H5','Unknown']
                },
                xAxis: {
                    data: x_data
                },
                yAxis: {},
                series: [{
                    name: 'Android',
                    data: android,
                    type:'line',
                    areaStyle: {},
                    stack: '总量',
                    color:'#79E773',
                    smooth:true,
                    symbol: 'none',
                },{
                    name: 'iOS',
                    data: ios,
                    type:'line',
                    areaStyle: {},
                    stack: '总量',
                    color:'#DDDFD9',
                    smooth:true,
                    symbol: 'none',
                },{
                    name: 'PC',
                    data: pc,
                    type:'line',
                    areaStyle: {},
                    stack: '总量',
                    color:'#6187E5',
                    smooth:true,
                    symbol: 'none',
                },{
                    name: 'H5',
                    data: h5,
                    type:'line',
                    areaStyle: {},
                    stack: '总量',
                    color:'#E05B41',
                    smooth:true,
                    symbol: 'none',
                },{
                    name: 'Unknown',
                    data: unknown,
                    type:'line',
                    areaStyle: {},
                    stack: '总量',
                    color:'#707070',
                    smooth:true,
                    symbol: 'none',
                },]
            };
            this.myChart.setOption(option);
        }
    }
})
