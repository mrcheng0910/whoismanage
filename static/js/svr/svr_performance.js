//含有和不含有whois服务器的饼图
$(function() {
    $('#container').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false
        },
        title: {
            text: '含有和不含有域名WHOIS服务器所占数量比'
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
            name: 'Browser share',
            data: [
                ['含有域名whois', 45.0],
                ['没有域名whois', 55.0]
            ]
        }]
    });
});

// 详细信息
function exist_detail() {
    $('#btn_exist_detail').on('click', function() {
        layer.open({
            type: 2,
            title: '含有域名whois服务器域名',
            shadeClose: true,
            shade: 0.8,
            area: ['66%', '75%'],
            content: '/svr_table'
        });
    });
};