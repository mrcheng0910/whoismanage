//获得各个服务器提供服务的域名数量
function test () {
    var raw_data=[];
    var svr_name = []
    var first = []
    $.ajax({
            url: '/top_sec/query_num',
            type: "get",
            timeout: 5000, //超时时间
            success: function (data) {  //成功后的处理
                raw_data = JSON.parse(data);
                // svr_name.push({
                //                 name: raw_data[0].top_svr,
                //                 id: raw_data[0].top_svr,
                //                 data: [[raw_data[0].sec_svr,raw_data[0].whois_sum]]               
                //              });
                // first.push({
                //     name: raw_data[0].top_svr,
                //     y: raw_data[0].whois_sum,
                //     drilldown: raw_data[0].top_svr 
                // });
                // for(var r_i=1,arrLength=raw_data.length;r_i<arrLength;r_i++){
                //     for(var s_i=0,svrLength=svr_name.length;s_i<svrLength;s_i++){
                //         if(svr_name[s_i].name==raw_data[r_i].top_svr){
                //             svr_name[s_i].data.push([raw_data[r_i].sec_svr,raw_data[r_i].whois_sum]);
                //             first[s_i].y=first[s_i].y+raw_data[r_i].whois_sum;
                //             break;
                //         }else{
                //             svr_name.push({
                //                 name: raw_data[r_i].top_svr,
                //                 id: raw_data[r_i].top_svr,
                //                 data: [[raw_data[r_i].sec_svr,raw_data[r_i].whois_sum]]               
                //                  });
                //             first.push({
                //                 name: raw_data[r_i].top_svr,
                //                 y: raw_data[r_i].whois_sum,
                //                 drilldown: raw_data[r_i].top_svr
                //             });
                //         }
                //     }
                // }
                // alert(first[1].y);
                // alert(svr_name[0].data);
                // var newarr = svr_name.filter(function(val){
                //     var y=0;
                //     alert(val.data.length);
                //     for(var i=0,l=val.data.length;i<l;i++){
                //         y = y + val.data[i][1]
                //     }
                //     // alert(y);
                // });
                // alert(newarr);
                init(raw_data[0],raw_data[1]);
               
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

function init(first,svr_name){
    $('#container1').highcharts({
    chart: {
        type: 'pie'
    },
    title: {
        text: '二级服务器提供服务域名数量比'
    },
    subtitle: {
        text: '已有域名whois信息域名'
    },
    plotOptions: {
        series: {
            dataLabels: {
                enabled: true,
                format: '{point.name}: {point.y:.1f}%'
            }
        }
    },

    tooltip: {
        headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
        pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}%</b> of total<br/>'
    },
    series: [{
        name: "whois服务器",
        colorByPoint: true,
        // data: [{
        //     name: "job",
        //     y: 56.33,
        //     drilldown: "job"
        // }, {
        //     name: "Chrome",
        //     y: 24.03,
        //     drilldown: "Chrome"
        // }, {
        //     name: "Firefox",
        //     y: 10.38,
        //     drilldown: "Firefox"
        
        // }]
        data: first
    }],
    drilldown: {
        series: svr_name
        // series: [{
        //     name: "job",
        //     id: "job",
        //     data: [
        //         ["v11.0", 24.13],
        //         ["v8.0", 17.2],
        //         ["v9.0", 8.11],
        //         ["v10.0", 5.33],
        //         ["v6.0", 1.06],
        //         ["v7.0", 0.5]
        //     ]
        // }, {
        //     name: "Chrome",
        //     id: "Chrome",
        //     data: [
        //         ["v40.0", 5],
        //         ["v41.0", 4.32],
        //         ["v42.0", 3.68],
        //         ["v39.0", 2.96],
        //         ["v36.0", 2.53],
        //         ["v43.0", 1.45],
        //         ["v31.0", 1.24],
        //         ["v35.0", 0.85],
        //         ["v38.0", 0.6],
        //         ["v32.0", 0.55],
        //         ["v37.0", 0.38],
        //         ["v33.0", 0.19],
        //         ["v34.0", 0.14],
        //         ["v30.0", 0.14]
        //     ]
        // }, {
        //     name: "Firefox",
        //     id: "Firefox",
        //     data: [
        //         ["v35", 2.76],
        //         ["v36", 2.32],
        //         ["v37", 2.31],
        //         ["v34", 1.27],
        //         ["v38", 1.02],
        //         ["v31", 0.33],
        //         ["v33", 0.22],
        //         ["v32", 0.15]
        //     ]

        // }]
    }
});
    
    
}