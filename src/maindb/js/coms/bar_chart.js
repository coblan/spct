Vue.component('com-bar-chart',{
    props:['trend'],
    data:function(){
        return {
            barRows: [],
        }
    },
    template:` <div class="chart" style="height:100%;width: 100%"></div>`,
    mounted:function(){
        //$('#mainjj').width($(this.$el).width()-30)
        //this. myChart = echarts.init(document.getElementById('mainjj'));
        this.myChart = echarts.init(this.$el);
        this.getRows()
    },
    methods:{
        getRows:function(){
            var self=this
            cfg.show_load()
            ex.director_call('trend_data',{key:this.trend.key},function(resp){
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
            var y_data=ex.map(v,function(item){
                return item.amount
            })

            var my_series ={
                name: self.trend.label,
                data: y_data,
            }
            var extra_option=char_kind[this.trend.kind || 'my_bar']
            Object.assign(my_series,extra_option)
            var option = {
                title: {
//                text: 'ECharts 入门示例'
                },
                tooltip: {},
//            legend: {
//                data:['销量']
//            },
                xAxis: {
                    data: x_data
                },
                yAxis: {},
                series: [my_series]
            };
            this.myChart.setOption(option);
        }
    }
})

var char_kind={
    my_bar:{
        type:'bar',
        itemStyle: {
            normal: {
                color: function(params) {
                    if(params.value>=0){
                        return '#C33531'
                    }else{
                        return 'green'
                    }
                }
            },
        },
    },
    my_area:{
        type:'line',
        areaStyle: {},
    },
    my_line:{
        type:'line',
    }
}