
function detect(results) {
    var categories = [];
    var detectTld = [];
    var unDetectTld = [];
    var len = results.length;
    for (var i=0,arr_len = results.length;i<arr_len;i++)
    {   
        categories.unshift(results[i].table_name);
        detectTld.unshift(results[i].flag_no_connect);
        unDetectTld.unshift(results[i].flag_undetected);
        // categories[i]=results[i].table_name;
        // detectTld[i]=results[i].flag_no_connect;
        // unDetectTld[i]=results[i].flag_undetected;
    }
    test("#container1",categories.slice(0,14),detectTld.slice(0,14),unDetectTld.slice(0,14));
    test("#container2",categories.slice(14,28),detectTld.slice(14,28),unDetectTld.slice(14,28));
}
function test(contain_name,categories,detectTld,unDetectTld){
        $(contain_name).highcharts({
            credits: {
                enabled: false,
            },
            chart: {
                type: 'bar',
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
            
            plotOptions: {
                series: {
                    stacking: 'percent'
                }
            },

            tooltip: {
                //下列函数就是用来把负值变为正数输出
                formatter: function () {
                    var s = '<b>' + this.x + '</b>';
                    var detectedDomainCount = 0;
                    var detectingDomainCount = 0;
                    $.each(this.points, function () {
                        if (this.y<0){
                            detectedDomainCount = (-this.y);
                            s += '<br>' + this.series.name + ': ' + detectedDomainCount + '个'
                                 +' <b>(' + Math.round(-this.percentage*100)/100 + '%)</b>';
                        }
                        else{
                            detectingDomainCount = this.y;
                            s += '<br>' + this.series.name + ': ' + detectingDomainCount + '个'
                                  +' <b>('+ Math.round(this.percentage*100)/100 + '%)</b>';
                            }
                        });
                        s += '<br><b>域名总数: '+(detectedDomainCount+detectingDomainCount)+'个</b>';
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