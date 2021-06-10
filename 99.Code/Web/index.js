function splitData(rawData) {
    var categoryData = [];
    var values = []
    for (var i = 0; i < rawData.length; i++) {
        categoryData.push(rawData[i].splice(0, 1)[0]);
        values.push([rawData[i][0], parseFloat(rawData[i][1]), parseFloat(rawData[i][2]), parseFloat(rawData[i][3]), parseFloat(rawData[i][4])]);
    }
    return {
        categoryData: categoryData,
        values: values
    };
}

function splitMarkLine(rawData) {
    var result = [];
    if (rawData.length <= 1){
        return result;
    }
    for (var i = 1; i < rawData.length; i++) {
        var point1 = {
            coord: [rawData[i - 1][0], parseFloat(rawData[i - 1][1])],
            symbol: 'circle',
            symbolSize: 10,
        };
        var point2 = {
            coord: [rawData[i][0], parseFloat(rawData[i][1])],
            symbol: 'circle',
            symbolSize: 10,
        };
        result.push([point1, point2]);
    }
    return result;
}

var option = {
    grid: { top: '2%', left: '5%', right: '5%', bottom: '15%' },
    xAxis: { type: 'category', data: null, scale: true, boundaryGap: false, axisLine: {onZero: false}, splitLine: {show: false}, min: 'dataMin', max: 'dataMax' },
    yAxis: { scale: true,splitArea: {show: true} },
    dataZoom: [
        { type: 'inside', start: 50, end: 100 },
        { show: true, type: 'slider', top: '90%', start: 50, end: 100 }
    ],
    series: [
        {
            name: '日K', type: 'candlestick', data: null,
            markLine: {
                lineStyle: {color: "#fff", width: 2, type: "solid"},
                data: []
            }
        }
    ]
};

$(function(){
    vue = new Vue(vueConfig);
});

var myChart;
var vue;
var vueConfig = {
    el: '.condition',
    data: {
        stocks: [],
        periods: [["d", "日线"], ["w", "周线"], ["m", "月线"]],
        stock: "",
        period: "",
    },
    methods: {
        search: function (event) {
            if (!this.stock || !this.period) return;
            api.get("StockTool/GetK?code=" + this.stock + "&period=" + this.period).then(res => {
                // 数据意义：开盘(open)，收盘(close)，最低(lowest)，最高(highest)
                var data = splitData(res.k);
                option.xAxis.data = data.categoryData;
                option.series[0].data = data.values;
                option.series[0].markLine.data = splitMarkLine(res.strokes);
                myChart.setOption(option);
            });
        }
    },
    mounted: function () {
        myChart = echarts.init(document.getElementById('chart'));
        api.get("StockTool/GetStocks").then(res => {
            this.stocks = res;
            this.stock = this.stocks[0][0];
            this.period = this.periods[0][0];
            this.search();
        });
    }
}