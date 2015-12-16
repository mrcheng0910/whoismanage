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
                text: '探测与未探测域名对比'
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
                // labels: {
                //     formatter: function () {
                //         return (Math.abs(this.value) / 1000000) + 'M';
                //     }
                // },
                min: -100,
                max: 100
            },

            plotOptions: {
                series: {
                    stacking: 'percent'
                }
            },

            tooltip: {
                formatter: function () {
                    return '<b>' + this.series.name + ', age ' + this.point.category + '</b><br/>' +
                        'Population: ' + Highcharts.numberFormat(Math.abs(this.point.y), 0);
                }
            },

            series: [{
                name: '已探测域名',
                //data: [-1746181, -1884428, -2089758, -2222362, -2537431, -2507081, -2443179,
                //    -2664537, -3556505, -3680231]
                data: detectTld.reverse()
            }, {
                name: '未探测域名',
                //data: [1656154, 1787564, 1981671, 2108575, 2403438, 2366003, 2301402, 2519874,
                //    3360596, 3493473]
                data: unDetectTld.reverse()
            }]
        });
    });
}
function detect1(results) {
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
        $('#container2').highcharts({
            chart: {
                type: 'bar'
            },
            title: {
                text: '探测与未探测域名对比'
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
                // labels: {
                //     formatter: function () {
                //         return (Math.abs(this.value) / 1000000) + 'M';
                //     }
                // },
                min: -100,
                max: 100
            },

            plotOptions: {
                series: {
                    stacking: 'percent'
                }
            },

            tooltip: {
                formatter: function () {
                    return '<b>' + this.series.name + ', age ' + this.point.category + '</b><br/>' +
                        'Population: ' + Highcharts.numberFormat(Math.abs(this.point.y), 0);
                }
            },
            
            series: [{
                name: '已探测域名',
                //data: [-1746181, -1884428, -2089758, -2222362, -2537431, -2507081, -2443179,
                //    -2664537, -3556505, -3680231]
                data: detectTld.reverse()
            }, {
                name: '未探测域名',
                //data: [1656154, 1787564, 1981671, 2108575, 2403438, 2366003, 2301402, 2519874,
                //    3360596, 3493473]
                data: unDetectTld.reverse()
            }]
        });
    });
}