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
                format: '{point.name}: {point.y:.f}个'
            }
        }
    },

    tooltip: {
        headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
        pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.f}个</b> of total<br/>'
    },
    series: [{
        name: "whois服务器",
        colorByPoint: true,
        data: first
    }],
    drilldown: {
        series: svr_name
    }
});
}