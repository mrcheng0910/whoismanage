function domain(domains) {
    var showData = []   //显示的数据
    for (var i=0;i<domains.length;i++){
        showData.push([domains[i].tld_name,domains[i].domain_num])
    }
    $('#container').highcharts({
        credits: {
            enabled: false
        },
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false
        },
        title: {
            text: "顶级域名所占比例分布"
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
                    color: '#000000',
                    connectorColor: '#000000',
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                }
            }
        },
        series: [{
            type: 'pie',
            name: '域名百分比',
            data:  showData
        }]
    });
};

//域名排序
function domainSort(domains) {
    var categories = [];
    var seriesData = [];
    for (var i=0;i<domains.length;i++){
        categories.push(domains[i].tld_name);
        seriesData.push(domains[i].domain_num);
    }

    $('#container-sort').highcharts({
        chart: {
            type: 'bar'
        },
        title: {
            text: "顶级域名数量排名"
        },
        xAxis: {
            categories: categories,
            title: {
                text: null
            },
            crosshair: true
        },
        yAxis: {
            min: 0,
            title: {
                text: '域名数量',
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
            name: '域名数量',
            data: seriesData
        }]
    });
};

