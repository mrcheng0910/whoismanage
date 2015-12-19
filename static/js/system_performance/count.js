
function GetDomainCount(argument,options){
    $.ajax({
            url: '/detect_count/data',
            type: "get",
            data: {
                argument: argument,
                options: options,
                stamp: Math.random()   // preventing "get" method using cache send to client
            },
            timeout: 5000, //超时时间
            success: function (data) {  //成功后的处理
                var raw_data = JSON.parse(data); //json格式化原始数据
                detect(raw_data);
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


function detect(results) {
    var categories = [];
    var detectTld = [];
    var unDetectTld = [];
    var categoryLen = results.length;
    for (var i=0;i<categoryLen;i++)
    {
        categories[i]=results[i].tld;
        detectTld[i]=results[i].detected;
        unDetectTld[i]=results[i].undetected;
    }
    var height = 200; //用来调整height的大小
    if (categoryLen>1){
        height = 50*categoryLen;
    }
    $('#container').highcharts({
        credits: {
            enabled: false,
        },
        chart: {
            type: 'bar',
            height: height,
        },
        title: {
            text: null
        },
        xAxis: [{
            categories: categories,
        }],
        yAxis: {
            title: {
                text: null
            },
            labels: {
                formatter: function () {
                    return (Math.abs(this.value)) + '%'; //输出正数百分比
                }
            },
        },
        legend: {
                reversed: true,
            },
        plotOptions: {
            series: {
                stacking: 'percent',
            }
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
            name: '已探测域名',
            data: detectTld
            // data: [-100000,]
        }, {
            name: '未探测域名',
            data: unDetectTld
        }]
    });
}