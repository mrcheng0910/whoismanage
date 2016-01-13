
function detect(results) {
    var categories = [];
    var unDetectTld = [];
    var noConnectTld = [];
    var noSvrTld = [];
    var regInfoTld = [];
    var regDateTld = [];
    var partInfoTld = [];
    for (var i=0,arr_len = results.length;i<arr_len;i++)
    {   
        categories.unshift(results[i].table_name.slice(13));
        noConnectTld.unshift(results[i].flag_no_connect);
        unDetectTld.unshift(results[i].flag_undetected);
        noSvrTld.unshift(results[i].flag_no_svr);
        regInfoTld.unshift(results[i].flag_reg_info);
        regDateTld.unshift(results[i].flag_reg_date);
        partInfoTld.unshift(results[i].flag_part_info);
    }
    init_overall("#container1",categories,noConnectTld,unDetectTld,noSvrTld,regInfoTld,regDateTld,partInfoTld);
}
function init_overall(contain_name,categories,noConnectTld,unDetectTld,noSvrTld,regInfoTld,regDateTld,partInfoTld){
        $(contain_name).highcharts({
            credits: {
                enabled: false,
            },
            chart: {
                type: 'column',
            },
            title: {
                text: null
            },
            xAxis: [{
                categories: categories
            }],
            yAxis: {
                title: {
                    text: null
                },
                labels: {
                    enabled: false,
                },
            },
            legend: {
                reversed: true,
            },
            
            plotOptions: {
                series: {
                    stacking: 'percent',
                    cursor: 'pointer',
                    events:{
                        click: function(e){
                            // alert(e.point.category);
                            layer.open({
                                type: 2,
                                title: null,
                                shadeClose: true,
                                shade: 0.8,
                                area: ['70%', '63%'],
                                content: '/table/overall/history?table_name=domain_whois_' + e.point.category
                            }); 
                        }
                    }
                
                },
            },
            tooltip: {
                //下列函数就是用来把负值变为正数输出
                formatter: function () {
                    var s = '<b>' + this.x + '</b>';
                    var domainCount = 0;
                    $.each(this.points, function () {
                        domainCount += this.y;
                        s += '<br>' + this.series.name + ': ' + this.y + '个'
                           +' <b>('+ Math.round(this.percentage*100)/100 + '%)</b>';
                    });
                    s += '<br><b>域名总数: '+(domainCount)+'个</b>';
                    return s;
                },
                shared: true,
                crosshairs: true,
                valueSuffix: ' 个',
            },

            series: [{
                name: '无法连接',
                data: noConnectTld
            }, {
                name: '暂未探测',
                data: unDetectTld
            },{
                name: '注册者完整',
                data: regInfoTld
            },{
                name: '注册日期完整',
                data: regDateTld
            },{
                name: '部分信息',
                data: partInfoTld
            },{
                name: '无域名服务器',
                data: noSvrTld
            }]
        });
}