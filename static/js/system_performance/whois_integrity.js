function whois_chart(tldWhoisSum) {
    //实现首页whois信息类型的展示
    var tldName = []; // 顶级后缀姓名
    var noConnect = []; // 无连接数量
    var regInfo = [];  //注册者信息
    var regDate = [];  // 注册日期
    var partOfInfo = [];  //部分信息
    var tldLength = tldWhoisSum.length
    for (var i = 0; i < tldLength; i++) {

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
            text: '域名WHOIS信息完整性统计(TOP '+tldLength+')'
        },
        xAxis: {
            //categories: ['COM', 'NET', 'ORG', 'CN']
            categories: tldName.sort()
        },
        yAxis: {
            min: 0,
            title: {
                text: '域名WHOIS信息完整性情况分布'
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

function get_tld_data(tld){
    var raw_data;
    var flag = [0,0,0,0];
    var noConncet = [];
    var regInfo = [];
    var regDate = [];
    var partOfInfo = [];
    $.ajax({
            url: '/whois_integrity/assignment_tld',
            type: "get",
            data: {
                tld: tld,
                stamp: Math.random()   // preventing "get" method using cache send to client
            },
            timeout: 5000, //超时时间
            success: function (data) {  //成功后的处理
                if (data=='None'){
                    alert("无该顶级后缀内容");
                }
                else{
                    raw_data = JSON.parse(data); //json格式化原始数据
                    for(var i=0;i<raw_data.length;i++){
                        switch(raw_data[i].flag){
                            case '0':
                                flag[0] = flag[0] + (+raw_data[i].whois_sum);
                                noConncet.push([FlagToText(raw_data[i].flag_detail),+raw_data[i].whois_sum]);
                                break;
                            case '1':
                                flag[1] = flag[1] + (+raw_data[i].whois_sum);
                                regInfo.push([FlagToText(raw_data[i].flag_detail),+raw_data[i].whois_sum]);
                                break;
                            case '2':
                                flag[2] = flag[2] + (+raw_data[i].whois_sum);
                                regDate.push([FlagToText(raw_data[i].flag_detail),+raw_data[i].whois_sum]);
                                break;
                            case '3':
                                flag[3] = flag[3] + (+raw_data[i].whois_sum);
                                partOfInfo.push([FlagToText(raw_data[i].flag_detail),+raw_data[i].whois_sum]);
                                break;
                        }
                    }
                    init_assignment_tld(tld,flag,noConncet,regInfo,regDate,partOfInfo);
                }
            },
            error: function (xhr) {
                if (xhr.status == "0") {
                    alert("超时，稍后重试");
                } else {
                    alert("错误提示：" + xhr.status + " " + xhr.statusText);
                }
            } // 出错后的处理
        });
    
}
    
function FlagToText(flag){
    
    switch(flag){
        case '-1':
            return "连接超时";
        case '-2':
            return "解析失败";
        case '-3':
            return "无法连接";
        case '-4':
            return "其他连接错误";
        case '120':
            return "无注册日期"
        case '121':
            return "注册日期不完善";
        case '122':
            return "注册信息完整";
        case '110':
            return "注册者不完善，无注册时间";
        case '102':
            return "无注册者，注册时间完善";
        case '112':
            return "注册者信息不完善，注册时间完善"
        case '100':
            return "无注册者，无注册日期";
        case '101':
            return "无注册信息，注册日期不完善";
        case '111':
            return "两者都不完善";
    }
}
    
function init_assignment_tld(tld,flag,noConnect,regInfo,regDate,partOfInfo){
    $('#containerfz').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: '域名顶级后缀('+tld+')详细信息'
        },
        xAxis: {
            type: 'category'
        },
        yAxis:{
            title:{
                text: '域名数量'
            } 
        },
        credits: {
            enabled: false
        },
        legend: {
            enabled: false
        },
        series: [{
           name: '总数',
           colorByPoint: true,
           data: [{
                name: "无法连接",
                y: flag[0],
                drilldown: "无法连接"
            }, {
                name: "注册者完整",
                y: flag[1],
                drilldown: "注册者完整"
            }, {
                name: "时间完整",
                y: flag[2],
                drilldown: "时间完整"
            }, {
                name: "两者不完整",
                y: flag[3],
                drilldown: "两者不完整"
            }]
        }],
        
        drilldown: {
            series: [{
                name: "无法连接",
                id: "无法连接",
                
                data: noConnect
                }, {
                name: "注册者完整",
                id: "注册者完整",
                data: regInfo
            }, {
                name: "时间完整",
                id: "时间完整",
                data: regDate
            }, {
                name: "两者不完整",
                id: "两者不完整",
                data: partOfInfo
            }]
        }
        
    });
     
}

function get_type_data(type,type_name){
    $.ajax({
        url: '/whois_integrity/assignment_type',
        type: "get",
        data: {
                type: type,
                stamp: Math.random()   // preventing "get" method using cache send to client
        },
        timeout: 5000, //超时时间
        success: function (data) {  //成功后的处理
            var raw_data = JSON.parse(data); 
            var tld = [];
            var tld_type = raw_data[0];
            var tld_type_total = []
            var tld_no_type = raw_data[1];
            var tld_no_type_total = []
            for (var i=0,arr_len = tld_type.length;i<arr_len;i++){
                tld.push(tld_type[i].tld);
                tld_type_total.push(tld_type[i].total);
                tld_no_type_total.push(tld_no_type[i].total);
            }
            // alert(tld);
            // alert(tld_type_total);
            init_type(tld,tld_type_total,tld_no_type_total,type_name);
        },
        error: function (xhr) {
            if (xhr.status == "0") {
                alert("超时，稍后重试");
            } else {
                alert("错误提示：" + xhr.status + " " + xhr.statusText);
            }
        } // 出错后的处理
    });
}

function init_type(tld,tld_type_total,tld_no_type_total,type_name){
    var len = tld.length;
    $('#containera').highcharts({
    credits: {
            enabled: false,
    },
    chart: {
        type: 'bar',
        height: 30*len
    },
    title: {
        text: null
    },
    xAxis: {
        categories: tld
    },
    yAxis: {
        min: 0,
        title: {
            text: null
        }
    },
    tooltip: {
        pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.percentage:.0f}%)<br/>',
        shared: true
    },
    plotOptions: {
        series: {
            stacking: 'percent'
        }
    },
    series: [{
        name: type_name,
        data: tld_type_total
    }, {
        name: '其他类型',
        data: tld_no_type_total
    }]
});

}