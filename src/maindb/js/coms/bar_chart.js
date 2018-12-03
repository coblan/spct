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
            ex.director_call('trend_data',{key:this.trend.key},function(resp){
                self.barRows=resp
            })
        }
    },
    watch:{
        barRows:function(v){
            var x_data=ex.map(v,function(item){
                return item.time
            })
            var y_data=ex.map(v,function(item){
                return item.amount
            })

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
                series: [{
                    name: '销量',
                    type: 'bar',
                    data: y_data,
                }]
            };
            this.myChart.setOption(option);
        }
    }
})