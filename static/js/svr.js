function test(svrs) {
    if (typeof(svrs)!='object'){
        svrs = eval('(' + svrs + ')');
    }
    var show_data = new Array()   //初始化显示的数据
    for (var i=0;i<svrs.length;i++){

        if (i == 1){               //i=1时，为最大数据，设置为选择
            show_data[i] = {
                name : svrs[i].svr_name,
                y:svrs[i].domain_sum,
                sliced: true,
                selected: true
            }
        }
        else
        {
            show_data[i] = new Array(svrs[i].svr_name,svrs[i].domain_sum)
        }
     }

    $('#container').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false
        },
        title: {
            text: "WHOIS服务器负责域名所占顶级后缀百分比"
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
function domain_sort(svrs) {
    if (typeof(svrs)!='object'){
        svrs = eval('(' + svrs + ')');
    }
    var name_data = new Array()
    var num_data = new Array()
    for (var i=0;i<svrs.length;i++){
        name_data[i] = svrs[i].svr_name
        num_data[i] = svrs[i].domain_sum
    }

    $('#container_sort').highcharts({
        chart: {
            type: 'bar'
        },
        title: {
            text: "WHOIS服务器负责域名所占顶级后缀数量"
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
            name: '顶级后缀数量',
            // data: [107, 31, 635, 203, 2]
            data: num_data
        }]
    });
};