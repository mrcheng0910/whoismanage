$(function () {
    var raw_data;
    var categories =[]
    var series_total = []
    var series_increase = []
    $.ajax({
            url: '/rate_of_increase',
            type: "get",
            timeout: 5000, //超时时间
            success: function (data) {  //成功后的处理
                raw_data = JSON.parse(data);
                for(var i=0,arrLength=raw_data.length;i<arrLength;i++){
                    var value = raw_data[i]
                    categories.unshift(value.insert_time.slice(0,10)); //添加时间，截取年月日
                    series_total.unshift((Math.round((value.sum/1000000.0)*100)/100)); //添加数量，两位小数，百万级别
                }
                for(var i =1;i<series_total.length;i++){
                    var single_value = (series_total[i]-series_total[i-1])/series_total[i-1];
                    series_increase.push(Math.round(single_value*100)/100);
                }
                init(categories.slice(1,categories.length),series_total.slice(1,series_total.length),series_increase);
            },
            error: function (xhr) {
                if (xhr.status == "0") {
                    alert("超时，稍后重试");
                } else {
                    alert("错误提示：" + xhr.status + " " + xhr.statusText);
                }
            } // 出错后的处理
        });
});

function init(categories,series_total,series_increase){
    $('#container').highcharts({
        credits: {
            enabled: false,
            text: '域名分析团队',
            href: '#'
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
                format: '{value}%',   //格式化标签
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            },
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
                format: '{value} M个',
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            },
            opposite: true,
            startOnTick: false,
            endOnTick: false,
            // tickInterval: 0.01,
            // min: series_increase[0]
            min: series_total[0],
            max: series_total[series_total.length-1],
            alignTicks: false,
            gridLineWidth: 0
            // gridLineWidth: 0
            // max: null
        }],
        tooltip: {
            shared: true
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
                valueSuffix: ' M个'
            }
            
        }, {
            name: '增长率',
            type: 'spline',
            data: series_increase,
            tooltip: {
                valueSuffix: '%'
            }
           
        }]
    });
}