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
                events:{
                    click: function(e){
                        if (e.point.name=='含有whois服务器'){
                            tld_svr_detail(flag=true);
                        }
                        else if(e.point.name=='不含有whois服务器'){
                            tld_svr_detail(flag=false);
                        }
                    }
                },
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
            name: '百分比',
            data: [
                {name: '含有whois服务器', y:145},
                {name: '不含有whois服务器', y:555},
            ]

        }]
    });
});

// 详细信息
function tld_svr_detail(flag) {
    var url = ''
    if (flag){
        url = '/svr_table?flag=True';
        title = '含有whois服务器域名列表'
    }
    else{
        url = '/svr_table?flag=False';
        title = '不含有whois服务器域名列表'
    }
    layer.open({
        type: 2,
        title: title,
        shadeClose: true,
        shade: 0.8,
        area: ['66%', '75%'],
        content: url
    });
};