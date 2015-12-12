$(function(){
    
    //探测效率统计
    $('#container-speed').highcharts({

        chart: {
            type: 'gauge',
            plotBackgroundColor: null,
            plotBackgroundImage: null,
            plotBorderWidth: 0,
            plotShadow: false
        },

        title: {
            text: '探测效率'
        },

        pane: {
            startAngle: -150,
            endAngle: 150,
            background: [{
                backgroundColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                    stops: [
                        [0, '#FFF'],
                        [1, '#333']
                    ]
                },
                borderWidth: 0,
                outerRadius: '109%'
            }, {
                backgroundColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                    stops: [
                        [0, '#333'],
                        [1, '#FFF']
                    ]
                },
                borderWidth: 1,
                outerRadius: '107%'
            }, {
                // default background
            }, {
                backgroundColor: '#DDD',
                borderWidth: 0,
                outerRadius: '105%',
                innerRadius: '103%'
            }]
        },

        // the value axis
        yAxis: {
            min: 0,
            max: 200,

            minorTickInterval: 'auto',
            minorTickWidth: 1,
            minorTickLength: 10,
            minorTickPosition: 'inside',
            minorTickColor: '#666',

            tickPixelInterval: 30,
            tickWidth: 2,
            tickPosition: 'inside',
            tickLength: 10,
            tickColor: '#666',
            labels: {
                step: 2,
                rotation: 'auto'
            },
            title: {
                text: '个/小时'
            },
            plotBands: [{
                from: 0,
                to: 120,
                color: '#55BF3B' // green
            }, {
                from: 120,
                to: 160,
                color: '#DDDF0D' // yellow
            }, {
                from: 160,
                to: 200,
                color: '#DF5353' // red
            }]
        },

        series: [{
            name: '效率',
            data: [100],
            tooltip: {
                valueSuffix: ' 个/小时'
            }
        }]

    },
    // Add some life
    function (chart) {
        if (!chart.renderer.forExport) {
            setInterval(function () {
                var point = chart.series[0].points[0],
                    newVal,
                    inc = Math.round((Math.random() - 0.5) * 20);

                newVal = point.y + inc;
                if (newVal < 0 || newVal > 200) {
                    newVal = point.y - inc;
                }
                newVal=100;

                point.update(newVal);

            }, 3000);
        }
    });
    
    
});

function init_total(total){
    //初始化已探测与未探测域名数量
    $('#container-total').highcharts({
        credits: {
            enabled: false
        },
        chart: {
            
            margin: [2, 2, 2, 2],
            plotBackgroundColor: null,
            plotBorderWidth: 0,
            plotShadow: false,
            // spacingBottom: 1,
            // spacingTop: 5
        },
        title: {
            text: '域名总数<br>'+total[0]+'M',
            align: 'center',
            // verticalAlign: 'middle',
            y: 140
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                dataLabels: {
                    enabled: true,
                    distance: -40,
                    style: {
                        fontWeight: 'bold',
                        color: 'white',
                        textShadow: '0px 1px 2px black'
                    }
                },
                // startAngle: -90,
                // endAngle: 180,
                center: ['50%', '50%']
            }
        },
        series: [{
            type: 'pie',
            name: '域名百分比',
            innerSize: '50%',
            data: [
                {
                    y: total[1],
                    name: '已探测',
                    color: '#8085e9'
                    
                },
                {
                    y: total[2],
                    name: '未探测',
                    color: '#e4d354'
                }
            ]
        }]
    });
}

function get_data(start,end) {
    //ajax获取最新统计数据，并更新页面
    var raw_data;
    $.ajax({
            url: '/detect/increase',
            type: "get",
            data: {
                start: start,
                end: end,
                stamp: Math.random()   // preventing "get" method using cache send to client
            },
            timeout: 5000, //超时时间
            success: function (data) {  //成功后的处理
                
                raw_data = JSON.parse(data); //json格式化原始数据
                var value;
                for(var i=0,arrLength=raw_data.length;i<arrLength;i++){
                    value = raw_data[i]
                    if (flag==true){//添加时间，截取详细时间
                        categories.unshift(value.insert_time.slice(11,value.insert_time.length)); 
                    }
                    else{
                        categories.unshift(value.insert_time.slice(0,10)); 
                    }
                    series_total.unshift((Math.round((value.sum/1000000.0)*1000)/1000)); //添加数量，两位小数，百万级别
                }
                for(var i=1,arrLength=raw_data.length;i<arrLength;i++){
                    series_increase.unshift(raw_data[i-1].sum-raw_data[i].sum)
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
};