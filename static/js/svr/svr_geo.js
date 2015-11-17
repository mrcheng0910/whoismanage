//whois服务器地理分布地图
function svr_geo(code_num) {
    var data = new Array();
    for (var i = 0; i < code_num.length; i++) {
        var obj = {
            'code': code_num[i].code,
            'value': code_num[i].value
        };
        data[i] = obj;
    };

    $('#container_map').highcharts('Map', {

        title: {
            text: '全球WHOIS服务器地理分布'
        },

        mapNavigation: {
            enabled: true,
            enableDoubleClickZoomTo: true
        },

        colorAxis: {
            min: 1,
            max: 50,
            type: 'logarithmic'
        },

        series: [{
            data: data,
            mapData: Highcharts.maps['custom/world'],
            joinBy: ['iso-a2', 'code'],
            name: '服务器个数',
            states: {
                hover: {
                    color: '#BADA55'
                }
            },
            tooltip: {
                valueSuffix: '个'
            }
        }]
    });
};
