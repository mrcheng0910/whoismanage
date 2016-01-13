function show(rawData){

    var categories =[];
    var seriesTotal = [];
    var seriesIncrease = [];

    for(var i=0,arrLength=rawData.length; i<arrLength; i++){
        var itemValue = rawData[i];
        categories.unshift(itemValue.insert_time);
        seriesTotal.unshift(itemValue.sum);
    }

    for(var i=1,arrLength=rawData.length; i<arrLength; i++){
        seriesIncrease.unshift(rawData[i-1].sum-rawData[i].sum)
    }

    initChart(categories.slice(1,categories.length),seriesTotal.slice(1,seriesTotal.length),seriesIncrease);
}

function initChart(categories, series_total, series_increase){
    $('#container').highcharts({
        credits: {
            enabled: false,
        },
        chart: {
            zoomType: 'x'  //x轴方向缩放
        },
        title: {
            text: '域名WHOIS信息增长趋势统计'
        },
        subtitle: {
            text: '增长数量与增长趋势'
        },
        xAxis: [{
            categories: categories,   //x轴显示数据
            crosshair: true,
            tickInterval: 2 //显示间隔，与step类似，但是其用的多
        }],
        yAxis: [{ // Primary yAxis
            labels: {
                formatter: function() {
                    if (this.value > 1000) {
                        return Highcharts.numberFormat(this.value / 1000, 1) + "K个";

                    }
                     return Highcharts.numberFormat(this.value,0);
                },
                style: {
                    color: Highcharts.getOptions().colors[1]
                },

            },
            //opposite: true,
            //startOnTick: false,
            //endOnTick: false,
            alignTicks: false,
            //gridLineWidth: 0,
            title: {
                text: '增长率',
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            }
        }, { // Secondary yAxis
            title: {
                text: '域名WHOIS总量',
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            },
            labels: {
                formatter: function() {
                    if (this.value > 1000000) {
                        return Highcharts.numberFormat(this.value/1000000, 1) + "M个";

                    }
                     return Highcharts.numberFormat(this.value,0);
                },
                //format: '{value} M个',
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            },
            opposite: true,
            startOnTick: false,
            endOnTick: false,
            alignTicks: false,
            gridLineWidth: 0
        }],
        tooltip: {
            shared: true,

        },
        legend: {
            layout: 'vertical',
            align: 'left',
            x: 120,
            verticalAlign: 'top',
            y: 40,
            floating: true,
            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
        },
        series: [{
            name: '域名WHOS总量',
            type: 'column',
            yAxis: 1,
            data: series_total,
            tooltip: {
                valueSuffix: ' 个'
            }
            
        }, {
            name: '增长率',
            type: 'spline',
            data: series_increase,
            tooltip: {
                valueSuffix: '个'
            }
           
        }]
    });
}
