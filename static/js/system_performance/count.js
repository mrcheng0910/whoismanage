function detect(results) {
    //var categories = ['com', 'cn', '10-14', '15-19',
    //        '20-24', '25-29', '30-34', '35-39', '40-44',
    //        '45-49'];
    var categories=[]
    var detectTld=[]
    var unDetectTld=[]
    for (var i=0;i<results.length;i++)
    {
        categories[i]=results[i].tld;
        detectTld[i]=-results[i].detected;
        unDetectTld[i]=results[i].undetected;
    }

    $(document).ready(function () {
        $('#container').highcharts({
            chart: {
                type: 'bar'
            },
            title: {
                text: '已探测与未探测域名百分比'
            },
            xAxis: [{
                categories: categories.reverse(),
                reversed: false,
                labels: {
                    step: 1
                }
            }, { // mirror axis on right side
                opposite: true,
                reversed: false,
                categories: categories,
                linkedTo: 0,
                labels: {
                    step: 1
                }
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
                min: -100,
                max: 100
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
                    $.each(this.points, function () {
                        if (this.y<0){
                            s += '<br/>' + this.series.name + ': ' +
                            (-this.y) + '个'+' <b>(' + Math.round(-this.percentage*100)/100 + '%)</b>';
                        }
                        else{
                            s += '<br/>' + this.series.name + ': ' +
                            this.y + '个'+' <b>(' + Math.round(this.percentage*100)/100 + '%)</b>';
                            }
                        });
                        return s;
                    },
                shared: true,
                crosshairs: true,
                valueSuffix: ' 个',
            },

            series: [{
                name: '已探测域名',
                data: detectTld.reverse()
            }, {
                name: '未探测域名',
                data: unDetectTld.reverse()
            }]
        });
    });
}