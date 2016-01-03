/**
 * Created by mrcheng on 15-12-31.
 */

function getTldNum(tld){
    var url = '/domain/tld-query';
    $.ajax({
            url: url,
            type: "get",
            data: {tld: tld},
            timeout: 5000, //超时时间
            success: function (data) {  //成功后的处理
                var results = JSON.parse(data); //json格式化原始数据

                var domainTotal = results[0]['total'];
                var tldTotal = results[0]['tld'];
                var tldWhois = results[0]['whois_tld'];
                var whoisTotal = results[0]['whois_total'];
                initTldChart(tld,domainTotal,tldTotal,tldWhois,whoisTotal);
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

function initTldChart(tld,domainTotal,tldTotal,tldWhois,whoisTotal){
    $("#title-pie").html(tld);
    var colors = Highcharts.getOptions().colors;
    var categories = [tld, '其他域名顶级后缀'];
    var data = [{
             y: tldTotal,
             color: '#8085e9',
             drilldown: {
                 name: tld,
                 categories: ['已探测', '未探测'],
                 data: [tldWhois, tldTotal-tldWhois ],
                 color: '#8085e9'
             }
        }, {
            y: domainTotal-tldTotal,
            color: colors[7],
            drilldown: {
                name: 'Other',
                categories: ['已探测','未探测'],
                data: [whoisTotal-tldWhois,domainTotal-tldTotal-whoisTotal],
                color: colors[7]
            }

        }];
    var browserData = [];
    var versionsData = [];
    var i;
    var j;
    var dataLen = data.length;
    var drillDataLen;
    var brightness;


    // Build the data arrays
    for (i = 0; i < dataLen; i += 1) {

        // add browser data
        browserData.push({
            name: categories[i],
            y: data[i].y,
            color: data[i].color
        });

        // add version data
        drillDataLen = data[i].drilldown.data.length;
        for (j = 0; j < drillDataLen; j += 1) {
            brightness = 0.2 - (j / drillDataLen) / 5;
            versionsData.push({
                name: data[i].drilldown.categories[j],
                y: data[i].drilldown.data[j],
                color: Highcharts.Color(data[i].color).brighten(brightness).get()
            });
        }
    }

    // Create the chart
    $('#container-tld').highcharts({
        credits: {
            enabled: false
        },
        chart: {
            type: 'pie'
        },
        title: {
            text: null
        },
        plotOptions: {
            pie: {
                shadow: false,
                center: ['50%', '50%'],
                dataLabels: {
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                }
            }
        },
        tooltip: {
            valueSuffix: '个'
        },
        series: [{
            name: '域名数量',
            data: browserData,
            size: '60%',
            dataLabels: {
                formatter: function () {
                    return this.y > 5 ? this.point.name : null;
                },
                color: '#ffffff',
                distance: -30
            }
        }, {
            name: '域名数量',
            data: versionsData,
            size: '80%',
            innerSize: '60%',
            dataLabels: {
                formatter: function () {
                    // display only if larger than 1
                    return this.y > 1 ? '<b>' + this.point.name + ':</b> ' + this.y + '个' : null;
                }
            }
        }]
    });
}