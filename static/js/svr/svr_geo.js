//whois服务器地理分布地图
function svr_geo(code_num) {
    var data = [];
    var dataPie = [];
    var countryCategories = [];
    var svrNum = [];
    var total = [0];
    var top = 12;
    for (var i = 0; i < code_num.length; i++) {
        
        data.push({
            'code': code_num[i].code,
            'value': code_num[i].value
        });
        total.push(total[i]+code_num[i].value);
        dataPie.push([code_num[i].country,code_num[i].value]);
        countryCategories.push(code_num[i].country);
        svrNum.push(code_num[i].value);
    }
    dataPie = dataPie.slice(0,top);
    dataPie.push(['Other',total[total.length-1]-total[top]]);
    countryCategories = countryCategories.slice(0,top);
    countryCategories.push('Other');
    svrNum = svrNum.slice(0,top);
    svrNum.push(total[total.length-1]-total[top]);
    
    
    $('#container_map').highcharts('Map', {
        
        credits: {
            enabled: false
        },
        
        title: {
            text: '全球WHOIS服务器地理分布'
            // text: null
        },

        mapNavigation: {
            enabled: true,
            enableDoubleClickZoomTo: true
        },
        legend: {
            title: {
                text: '含有域名WHOIS服务器数量(个)',
                style: {
                    color: (Highcharts.theme && Highcharts.theme.textColor) || 'black'
                }
            },
            align: 'left',
            verticalAlign: 'bottom',
            floating: true,
            layout: 'vertical',
            valueDecimals: 0,
            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || 'rgba(255, 255, 255, 0.85)',
            symbolRadius: 0,
            symbolHeight: 14
        },
        colorAxis: {
            dataClasses: [{
                to: 3
            }, {
                from: 3,
                to: 10
            }, {
                from: 10,
                to: 30
            }, {
                from: 30,
                to: 50
            }, {
                from: 50,
                to: 70
            }, {
                from: 70,
                to: 100
            }]
        },
        series: [{
            data: data,
            mapData: Highcharts.maps['custom/world'],
            joinBy: ['iso-a2', 'code'],
            name: '服务器个数',
            states: {
                hover: {
                    color: '#BADA55'
                }
            },
            point: {
                events: {
                    click: function(){
                        layer.open({
                            type: 2,
                            title: null,
                            // closeBtn: false,
                            shadeClose: true,
                            shade: 0.8,
                            area: ['70%', '65%'],
                            content: "/svr_geo_table?country="+this.code
                        });
                    }
                }
            },
            tooltip: {
                valueSuffix: '个'
            }
        }]
    });
    
    $('#container-pie').highcharts({
        credits: {
            enabled: false
        },
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false
        },
        title: {
            // text: '域名WHOIS服务器国家分布百分比'
            text: null
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    }
                }
            }
        },
        series: [{
            type: 'pie',
            name: 'WHOIS服务器数量',
            data: dataPie
        }]
    });
    
    $('#container-sort').highcharts({
        chart: {
            type: 'bar'
        },
        title: {
            // text: "域名数量排名"
            text: null
        },
        xAxis: {
            categories: countryCategories,
            title: {
                text: null
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: '数量',
                align: 'high'
            },
            labels: {
                overflow: 'justify'
            }
        },
        tooltip: {
            valueSuffix: '个'
        },
        plotOptions: {
            bar: {
                dataLabels: {
                    enabled: true
                }
            }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'top',
            // x: -20,
            y: 120,
            floating: true,
            borderWidth: 1,
            backgroundColor: '#FFFFFF',
            shadow: true
        },
        credits: {
            enabled: false
        },
        series: [{
            name: 'WHOIS服务器数量',
            data: svrNum
        }]
    });

}
