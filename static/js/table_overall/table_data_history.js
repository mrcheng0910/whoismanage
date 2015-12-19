function showTable(results){
    var categories = [];
    var unDetected = [];
    var noSvr = [];
    var noConnect = [];
    var regInfo = [];
    var regDate = [];
    var partInfo = [];
    for(var i=0,len=results.length;i<len;i++){
        categories.unshift(results[i].update_time.slice(11));
        unDetected.unshift(results[i].flag_undetected);
        noSvr.unshift(results[i].flag_no_svr);
        noConnect.unshift(results[i].flag_no_connect);
        regInfo.unshift(results[i].flag_reg_info);
        regDate.unshift(results[i].flag_reg_date);
        partInfo.unshift(results[i].flag_part_info);
    }
    initHistoryChart(categories,unDetected,noSvr,noConnect,regInfo,regDate,partInfo);
    
}


function initHistoryChart(categories,unDetected,noSvr,noConnect,regInfo,regDate,partInfo){
    $('#container').highcharts({
        credits: {
                enabled: false,
        },
        title: {
            text: '数据库表探测变化趋势',
            x: -20 //center
        },
        subtitle: {
            text: '12小时',
            x: -20
        },
        xAxis: {
               categories: categories
        },
        yAxis: {
            title: {
                text: '域名数量'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            valueSuffix: '个'
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [{
            name: '未探测域名',
            data: unDetected
        }, {
            name: '无服务器',
            data: noSvr
        }, {
            name: '无法连接',
            data: noConnect
        }, {
            name: '注册者信息',
            data: regInfo
        },{
            name: '注册时间',
            data: regDate
        },{
            name: '部分信息',
            data: partInfo
        }]
    });
}