require('./styl/bet_abstract_chart.styl')

var bet_chart={
    template:`<div class="live-bet-chart">
        <div class="mychart betusernum" ></div>
          <div class="mychart betamount" ></div>
        <div class="mychart betnum" ></div>

        <div class="mychart userprofit" ></div>
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
            this.draw1()
            this.draw_betnum()
            this.draw_betamount()
            this.draw_betoutcome()
        }
    },
    methods:{
        draw1(){
            var myChart = echarts.init( $(this.$el).find('.betusernum')[0] );

            // 指定图表的配置项和数据
            var option = {
                title: {
                    text: ''
                },
                tooltip: {},
                legend: {
                    data:['用户数']
                },
                xAxis: {
                    data: this.parStore.rows.map(item=>{return item.starttime}).reverse()
                    //data: ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
                },
                yAxis: {},
                series: [{
                    name: '用户数',
                    type: 'bar',
                    data: this.parStore.rows.map(item=>{return item.betusernum}).reverse(),
                    barMaxWidth: 30,
                    itemStyle: {
                        normal: {
                            color:'#27B6AC'
                        },
                    },

                }]
            };

            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
        },
        draw_betnum(){
            var myChart = echarts.init( $(this.$el).find('.betnum')[0] );

            // 指定图表的配置项和数据
            var option = {
                title: {
                    text: ''
                },
                tooltip: {},
                legend: {
                    data:['注单量','注单金额']
                },
                xAxis: {
                    data: this.parStore.rows.map(item=>{return item.starttime}).reverse()
                    //data: ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
                },
                yAxis: [
                    {
                        type: 'value',
                        name: '注单量',
                    },
                    {
                        type: 'value',
                        name: '注单金额',
                    }
                ],
                series: [{
                    name: '注单量',
                    type: 'bar',
                    yAxisIndex:0,
                    data: this.parStore.rows.map(item=>{return item.betnum}).reverse(),
                    barMaxWidth: 30,
                    itemStyle: {
                        normal: {
                            color:'#27B6AC'
                        },
                    },
                },
                    {
                        name: '注单金额',
                        type: 'line',
                        yAxisIndex:1,
                        data: this.parStore.rows.map(item=>{return item.betamount}).reverse()
                        //data: [5, 20, 36, 10, 10, 20]
                    },
                ]
            };

            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
        },
        draw_betamount(){
            var myChart = echarts.init( $(this.$el).find('.betamount')[0] );

            // 指定图表的配置项和数据
            var option = {
                title: {
                    text: ''
                },
                tooltip: {},
                legend: {
                    data:['投注金额','派奖金额']
                },
                xAxis: {
                    data: this.parStore.rows.map(item=>{return item.starttime}).reverse()
                    //data: ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
                },
                yAxis: {},
                series: [{
                    name: '投注金额',
                    type: 'bar',
                    data: this.parStore.rows.map(item=>{return item.betamount}).reverse(),
                    barMaxWidth: 30,
                },
                    {
                        name: '派奖金额',
                        type: 'bar',
                        data: this.parStore.rows.map(item=>{return item.betoutcome}).reverse()
                    },

                ]
            };

            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
        },
        draw_betoutcome(){
            var myChart = echarts.init( $(this.$el).find('.userprofit')[0] );

            // 指定图表的配置项和数据
            var option = {
                title: {
                    text: ''
                },
                tooltip: {},
                legend: {
                    data:['平台毛利']
                },
                xAxis: {
                    data: this.parStore.rows.map(item=>{return item.starttime}).reverse()
                    //data: ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
                },
                yAxis: {},
                series: [{
                    name: '平台毛利',
                    type: 'bar',
                    data: this.parStore.rows.map(item=>{return item.userprofit}).reverse(),
                    barMaxWidth: 30,
                    itemStyle: {
                        normal: {
                            color:'#27B6AC'
                        }
                    },
                }]
            };

            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
        }
    }
}

Vue.component('com-bet-chart',function(resolve,reject){
    ex.load_js(js_config.js_lib.echarts).then(function(){
            resolve(bet_chart)
    })
})
