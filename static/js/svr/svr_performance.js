//含有和不含有whois服务器的饼图
function tld_svr_pie(count,count_null) {
    $('#container').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false
        },
        title: {
            text: null
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
                            tld_svr_tb(flag=true);
                        }
                        else if(e.point.name=='不含有whois服务器'){
                            tld_svr_tb(flag=false);
                        }
                    }
                },
                dataLabels: {
                    enabled: false,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    }
                },
                showInLegend: true
            }
        },
        series: [{
            type: 'pie',
            name: '百分比',
            data: [
                {name: '含有whois服务器', y: count},
                {name: '不含有whois服务器', y: count_null},
            ]

        }]
    });
}
// 详细信息
function tld_svr_tb(flag) {
    var url = ''
    if (flag){
        url = '/svr_table?flag=True';
        //title = '含有whois服务器域名列表'
    }
    else{
        url = '/svr_table?flag=False';
        //title = '不含有whois服务器域名列表'
    }
    layer.open({
        type: 2,
        title: "域名WHOIS详细信息",
        closeBtn: false,
        shadeClose: true,
        shade: 0.8,
        area: ['68%', '75%'],
        content: url
    });
}

//含有和不含有whois服务器的饼图
function tld_svr_reg(reg_n,reg_p,reg_y) {
    $('#container_reg').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false
        },
        title: {
            text: null
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

                        tld_svr_info();
                    }
                },
                dataLabels: {
                    enabled: false,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    }
                },
                showInLegend: true
            }
        },
        series: [{
            type: 'pie',
            name: '百分比',
            data: [
                {name: '无注册人信息', y: reg_n},
                {name: '部分注册人信息', y: reg_p},
                {name: '完整注册人信息',y: reg_y}
            ]

        }]
    });
}
 //详细信息
function tld_svr_info(flag) {
    var url = '/svr_table_info'
    layer.open({
        type: 2,
        title: "域名WHOIS详细信息",
        closeBtn: false,
        shadeClose: true,
        shade: 0.8,
        area: ['68%', '75%'],
        content: url
    });
}