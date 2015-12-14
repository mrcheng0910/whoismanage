var domain_detecting,detecting_speed,domain_total,domain_detected;

function init_total(total){
    //初始化已探测与未探测域名数量
    domain_detecting = total[2];
    domain_total= total[0];
    domain_detected = total[1];
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


function init_speed(speed){
    //探测效率统计
    detecting_speed = speed;
    $('#container-speed').highcharts({
        credits: {
            enabled: false
        },
        chart: {
            type: 'gauge',
            plotBackgroundColor: null,
            plotBackgroundImage: null,
            plotBorderWidth: 0,
            plotShadow: false
        },

        title: {
            // text: '探测效率(个/小时)'
            text: null
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
            max: 36000,

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
                to: 12000,
                color: '#DF5353' // green '#DF5353'
            }, {
                from: 12000,
                to: 24000,
                color: '#DDDF0D' // yellow
            }, {
                from: 24000,
                to: 36000,
                color: '#55BF3B' // red '#55BF3B'
            }]
        },

        series: [{
            name: '效率',
            data: [speed],
            tooltip: {
                valueSuffix: ' 个/小时'
            }
        }]

    }
    // // Add some life
    // function (chart) {
    //     if (!chart.renderer.forExport) {
    //         setInterval(function () {
    //             var point = chart.series[0].points[0],
    //                 newVal,
    //                 inc = Math.round((Math.random() - 0.5) * 20);

    //             newVal = point.y + inc;
    //             if (newVal < 0 || newVal > 200) {
    //                 newVal = point.y - inc;
    //             }
    //             newVal=speed;

    //             point.update(newVal);

    //         }, 3000);
    //     }
    // }
    );
    $("#detecting-speed").text(detecting_speed);
    var tmp = domain_detecting*1000000/(detecting_speed*24);
    $("#detecting-days").text(Math.ceil(tmp));
    $("#detecting-months").text(Math.ceil(tmp/30));
    $("#domain-detecting").text(Math.round(domain_detecting*100)/100);
    $("#domain-detected").text(domain_detected);
    $("#domain-total").text(domain_total);
    
}


function get_data(period) {
    //ajax获取最新统计数据，并更新页面
    var raw_data;
    $.ajax({
            url: '/forcast/period',
            type: "get",
            data: {
                period: period,
                stamp: Math.random()   // preventing "get" method using cache send to client
            },
            timeout: 5000, //超时时间
            success: function (data) {  //成功后的处理
                raw_data = JSON.parse(data); //json格式化原始数据
                // alert(data);
                init_speed(raw_data);
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