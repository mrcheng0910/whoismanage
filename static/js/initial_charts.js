function whois_chart() {
    //实现首页whois信息类型的展示
    $('#containertb').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'WHOIS信息类型统计'
        },
        xAxis: {
            categories: ['COM', 'NET', 'ORG', 'CN', 'BTI','NL']
        },
        yAxis: {
            min: 0,
            title: {
                text: '域名WHOIS信息获取情况分布'
            }
        },
        tooltip: {
            pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.percentage:.0f}%)<br/>',
            shared: true
        },
        plotOptions: {
            column: {
                stacking: 'percent'
            }
        },
        series: [{
            name: '无法连接',
            data: [5, 3, 4, 7, 2]
        }, {
            name: '注册者信息完整',
            data: [2, 2, 3, 2, 1]
        }, {
            name: '注册时间完整',
            data: [3, 4, 4, 2, 5]
        },{
            name: '注册者和时间不完整',
            data: [3,4,5,6,7]

        }]
    });
};