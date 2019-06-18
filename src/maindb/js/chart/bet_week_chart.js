
var bet_chart={
    template:`<div class="live-bet-week-chart" style="margin: 20px">
        <div class="mychart betweek" style="width: 700px;height: 500px;"></div>
    </div>`,
    data(){
        return {
        }
    },
    beforeCreate(){
        this.parStore = ex.vueParStore(this)
    },
    mounted(){
        //this.draw1()
    },
    computed:{
        rows(){
            return this.parStore.rows
        }
    },

    watch:{
        rows(){
            this.draw_betweek()
        }
    },
    methods:{
        draw_betweek(){
            var myChart = echarts.init( $(this.$el).find('.betweek')[0] );

            // 指定图表的配置项和数据
            var option = {
                title: {
                    text: ''
                },
                tooltip: {},
                legend: {
                    data:['投注额']
                },
                xAxis: {
                    data: this.parStore.rows.map(item=>{return item.Year+'/'+item.Week})
                },
                yAxis: {},
                axisTick: {
                    inside: true
                },
                grid: {
                    left: 100
                },
                series: [{
                    name: '投注额',
                    type: 'bar',
                    barMaxWidth: 30,
                    data: this.parStore.rows.map(item=>{return item.BetAmount}),
                    itemStyle: {
                        normal: {
                            color: new echarts.graphic.LinearGradient(
                                0, 0, 0, 1,
                                [
                                    {offset: 0, color: '#83bff6'},
                                    {offset: 0.5, color: '#188df0'},
                                    {offset: 1, color: '#188df0'}
                                ]
                            )
                        },
                        emphasis: {
                            color: new echarts.graphic.LinearGradient(
                                0, 0, 0, 1,
                                [
                                    {offset: 0, color: '#2378f7'},
                                    {offset: 0.7, color: '#2378f7'},
                                    {offset: 1, color: '#83bff6'}
                                ]
                            )
                        }
                    },
                    //data: [5, 20, 36, 10, 10, 20]
                }]
            };

            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
        },
    }
}

Vue.component('com-bet-week-chart',function(resolve,reject){
    ex.load_js(js_config.js_lib.echarts).then(function(){
        resolve(bet_chart)
    })
})
