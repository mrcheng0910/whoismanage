function whois_chart(tldWhoisSum) {
    //实现首页whois信息类型的展示
    var tldName = []; // 顶级后缀姓名
    var noConnect = []; // 无连接数量
    var regInfo = [];  //注册者信息
    var regDate = [];  // 注册日期
    var partOfInfo = [];  //部分信息
    for (var i = 0; i < tldWhoisSum.length; i++) {

        tldName[i] = tldWhoisSum[i].tld_name;
        noConnect[i] = Number(tldWhoisSum[i].no_connect);//注意字符串转数字
        regInfo[i] = Number(tldWhoisSum[i].reg_info);//注意字符串转数字
        regDate[i] = Number(tldWhoisSum[i].reg_date);//注意字符串转数字
        partOfInfo[i] = Number(tldWhoisSum[i].part_info); //注意字符串转数字
    }
    $('#containertb').highcharts({
        credits: {
            enabled: false,
        },
        chart: {
            type: 'column'
        },
        title: {
            text: 'WHOIS信息类型统计'
        },
        xAxis: {
            //categories: ['COM', 'NET', 'ORG', 'CN']
            categories: tldName.sort()
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
        // legend: {
        //   reversed: true  
        // },
        plotOptions: {
            column: {
                stacking: 'percent'
            }
        },
        series: [{
            name: '无法连接',
            //data: [ 3, 4, 7, 2]
            data: noConnect
        }, {
            name: '注册者信息完整',
            //data: [ 2, 3, 2, 1]
            data: regInfo
        }, {
            name: '注册时间完整',
            //data: [ 4, 4, 2, 5]
            data: regDate
        }, {
            name: '注册者和时间不完整',
            //data: [4,5,6,7]
            data: partOfInfo

        }]
    });
    
}

function aaa(){
    $('#containerfz').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: '顶级后缀详细信息'
        },
        xAxis: {
            type: 'category'
        },
        credits: {
            enabled: false
        },
        legend: {
            enabled: false
        },
        series: [{
           name: '个数',
           colorByPoint: true,
           data: [{
                name: "无法连接",
                y: 100,
                drilldown: "无法连接"
            }, {
                name: "注册者完整",
                y: 80,
                drilldown: "注册者完整"
            }, {
                name: "时间完整",
                y: 110,
                drilldown: "时间完整"
            }, {
                name: "两者不完整",
                y: 60,
                drilldown: "两者不完整"
            }]
        }],
        
        drilldown: {
            series: [{
                name: "无法连接",
                id: "无法连接",
                data: [
                    [
                        "v11.0",
                        24
                    ],
                    [
                        "v8.0",
                        26
                    ],
                    [
                        "v9.0",
                        20
                    ],
                    [
                        "v10.0",
                        30
                    ]
    
                   ]
                }, {
                name: "注册者完整",
                id: "注册者完整",
                data: [
                    [
                        "v40.0",
                        10
                    ],
                    [
                        "v41.0",
                        20
                    ],
                    [
                        "v42.0",
                        20
                    ],
                    [
                        "v39.0",
                        30
                    ]
                    
                ]
            }, {
                name: "时间完整",
                id: "时间完整",
                data: [
                    [
                        "v35",
                        40
                    ],
                    [
                        "v36",
                        70
                    ]
                    
                ]
            }, {
                name: "两者不完整",
                id: "两者不完整",
                data: [
                    [
                        "v8.0",
                        10
                    ],
                    [
                        "v7.1",
                        10
                    ],
                    [
                        "v5.1",
                        20
                    ],
                    [
                        "v5.0",
                        20
                    ]
                ]
            }]
        }
      
    });
     
}