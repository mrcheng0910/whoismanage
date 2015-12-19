function test() {
    
    var gaugeOptions = {

        chart: {
            type: 'solidgauge'
        },

        title: null,

        pane: {
            center: ['50%', '85%'],
            size: '140%',
            startAngle: -90,
            endAngle: 90,
            background: {
                backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || '#EEE',
                innerRadius: '60%',
                outerRadius: '100%',
                shape: 'arc'
            }
        },

        tooltip: {
            enabled: false
        },

        // the value axis
        yAxis: {
            stops: [
                [0.1, '#DDDF0D'], //颜色
                [0.5, '#55BF3B'], //
                [0.9, '#9ACD32'] //
            ],
            lineWidth: 0,
            minorTickInterval: null,
            tickPixelInterval: 400,
            tickWidth: 0,
            //tickPositions:[0,300],
            title: {
                y: -70
            },
            labels: {
                y: 16
            }
        },

        plotOptions: {
            solidgauge: {
                dataLabels: {
                    y: 5,
                    borderWidth: 0,
                    useHTML: true
                }
            }
        }
    };

    // The domain
    $('#container-domain').highcharts(Highcharts.merge(gaugeOptions, {
        yAxis: {
            min: 0,
            max: 300,
            title: {
                text: '收录域名数量/全球域名数量'
            },
            tickPositions:[0,300]

        },

        credits: {
            enabled: false
        },

        series: [{
            name: '数量',
            data: [106],
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:25px;color:' +
                    ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y}</span><br/>' +
                       '<span style="font-size:12px;color:silver">百万(million)</span></div>'
            },
            tooltip: {
                valueSuffix: 'million'
            }
        }]

    }));
    $('#container-tld').highcharts(Highcharts.merge(gaugeOptions, {
        yAxis: {
            min: 0,
            max: 1126,
            title: {
                text: '收录顶级后缀/全球顶级后缀数量'
            },
             tickPositions:[0,1126]
        },

        credits: {
            enabled: false
        },

        series: [{
            name: '数量',
            data: [287],
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:25px;color:' +
                    ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y}</span><br/>' +
                       '<span style="font-size:12px;color:silver">个</span></div>'
            },
            tooltip: {
                valueSuffix: '个'
            }
        }]

    }));
};