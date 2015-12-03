$(function () {
    var raw_data;
    var categories_data=[];
    var series_data =[];
    $.ajax({
            url: '/top_sec/query',
            type: "get",
            timeout: 5000, //超时时间
            success: function (data) {  //成功后的处理
                raw_data = JSON.parse(data);
                categories_data = raw_data.map(function(val){
                   return val.top_svr;
                });
                series_data = raw_data.map(function(val){
                   return val.num;
                });
                test(categories_data,series_data);
                $("#top").text(categories_data.length);
            }, 
            error: function (xhr) {
                if (xhr.status == "0") {
                    alert("超时，稍后重试");
                } else {
                    alert("错误提示：" + xhr.status + " " + xhr.statusText);
                }
            } // 出错后的处理
        });
})

function test(c,s){
        $('#container').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: '含有二级WHOIS服务器分布'
        },
        xAxis: {
            categories: c,   //x坐标显示内容，即whois服务器
            crosshair: true
        },
        yAxis: {
            min: 0,
            title: {
                text: '二级WHOIS服务器数量 (个)'
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.f} 个</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            name: '数量',
            data: s  //Y坐标显示内容，即数量

        }]
    });
}