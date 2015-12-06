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
                    categories.unshift(value.insert_time.slice(0,10));
                    series_total.unshift(value.tld_sum);
                }
                for(var i =1;i<series_total.length;i++){
                    series_increase.push((series_total[i]-series_total[i-1])/series_total[i-1]);
                }
                init(categories,series_total.slice(1,series_total.length),series_increase);
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
        chart: {
            zoomType: 'xy'
        },
        title: {
            text: '域名WHOIS信息增长趋势统计'
        },
        subtitle: {
            text: '增长数量与增长趋势'
        },
        xAxis: [{
            // categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            //     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            categories: categories,
            crosshair: true
        }],
        yAxis: [{ // Primary yAxis
            labels: {
                format: '{value}%',
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
                format: '{value} 个',
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            },
            opposite: true
        }],
        tooltip: {
            shared: true
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            x: 120,
            verticalAlign: 'top',
            y: 100,
            floating: true,
            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
        },
        series: [{
            name: '域名WHOS总量',
            type: 'column',
            yAxis: 1,
            // data: [49.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4],
            data: series_total,
            tooltip: {
                valueSuffix: ' 个'
            }

        }, {
            name: '增长率',
            type: 'spline',
            // data: [7.0, 6.9, 9.5, 14.5, 18.2, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6],
            data: series_increase,
            tooltip: {
                valueSuffix: '%'
            }
        }]
    });
}