Vue.component('com-bar-chart',{
    props:['ctx'],
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
            ex.director_call('trend_data',{key:this.ctx.key},function(resp){
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
            var option = {
                title: {
                },
                tooltip: {},
                xAxis: {
                    data: x_data
                },
                yAxis: {},
                series: [{
                    name: self.ctx.label,
                    data: y_data,
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
                }]
            };
            this.myChart.setOption(option);
        }
    }
})
