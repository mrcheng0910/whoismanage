function domain(domains) {
    var show_data = new Array()   //显示的数据
    for (var i=0;i<domains.length;i++){
        if (i == 0){               //i=0时，为最大数据，设置为选择
            show_data[i] = {
                name : domains[i].tld_name,
                y:domains[i].domain_num,
                sliced: true,
                selected: true
            }
        }
        else
        {
            show_data[i] = new Array(domains[i].tld_name,domains[i].domain_num)
        }
     }
    $('#container').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false
        },
        title: {
            text: "各个顶级后缀域名所占比例"
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
            data:  show_data
        }]
    });
};

//域名排序
function domain_sort(domains) {
    var name_data = new Array()
    var num_data = new Array()
    for (var i=0;i<domains.length;i++){
        name_data[i] = domains[i].tld_name
        num_data[i] = domains[i].domain_num
    }

    $('#container_sort').highcharts({
        chart: {
            type: 'bar'
        },
        title: {
            text: "域名数量排名"
        },
        xAxis: {
            // categories: ['com', 'net', 'cn', 'info', 'biz'],
            categories: name_data,
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
            name: '域名数量',
            // data: [107, 31, 635, 203, 2]
            data: num_data
        }]
    });
};