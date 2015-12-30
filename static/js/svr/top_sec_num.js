//获得各个服务器提供服务的域名数量
function test () {
    var rawData=[];
    $.ajax({
        url: '/top_sec/query_num',
        type: "get",
        timeout: 5000, //超时时间
        success: function (data) {  //成功后的处理
            rawData = JSON.parse(data);
            init(rawData[0],rawData[1]);
            $("#top").text(rawData[0].length);
        },
        error: function (xhr) {
            if (xhr.status == "0") {
                alert("超时，稍后重试");
            } else {
                alert("错误提示：" + xhr.status + " " + xhr.statusText);
            }
        }
    });

}

function init(first,svr_name){
    $('#container1').highcharts({
    chart: {
        type: 'pie'
    },
    credits: {
            enabled: false
    },
    title: {
        text: null
    },
    plotOptions: {
        series: {
            dataLabels: {
                enabled: true,
                format: '{point.name}: <br>{point.y:.f}个'
            }
        }
    },

    tooltip: {
        headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
        pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.f}个</b> <br/>'
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