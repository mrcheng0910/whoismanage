//初始化页面以及绑定函数
$(function () {
    //初始化页面
    $('#datetimepicker-start').datetimepicker({
        format: "YYYY-MM-DD",
        defaultDate: new Date(),
        showTodayButton: true
    });
    $('#datetimepicker-end').datetimepicker({
        useCurrent: false, //Important! See issue #1075
        format: "YYYY-MM-DD",
        defaultDate: new Date(),
        showTodayButton: true
    });
    $("#datetimepicker-start").on("dp.change", function (e) {
        $('#datetimepicker-end').data("DateTimePicker").minDate(e.date);
    });
    $("#datetimepicker-end").on("dp.change", function (e) {
        $('#datetimepicker-start').data("DateTimePicker").maxDate(e.date);
    });
    
    var start = $("#start_date").val(); //获取初始化后页面的起始日期
    var end = $("#end_date").val(); //获取初始化后页面的终止日期
    
    get_data(start,end);  //初始化趋势
    
    $("#query").bind('click',function(){  //为查询按钮绑定查询函数
        start = $("#start_date").val();
        end = $("#end_date").val();
        get_data(start,end);
    });
});

function init(categories,series_total,series_increase){
    //更新数据趋势
    $("#detect_period").text('探测时间段为：'+categories[0]+'至'+categories[categories.length-1]);
    $('#container').highcharts({
        credits: {
            enabled: false,
            text: '域名分析团队',
            href: '#'
        },
        chart: {
            zoomType: 'x'  //x轴方向缩放
        },
        title: {
            text: '域名WHOIS信息增长趋势统计'
        },
        subtitle: {
            text: '增长数量与增长趋势'
        },
        xAxis: [{
            categories: categories,   //x轴显示数据
            crosshair: true,
            tickInterval: 2 //显示间隔，与step类似，但是其用的多
        }],
        yAxis: [{ // Primary yAxis
            labels: {
                format: '{value}个',   //格式化标签
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            },
            title: {
                text: '增长率',
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            }
        }, { // Secondary yAxis
            title: {
                text: '域名WHOIS总量',
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            },
            labels: {
                format: '{value} M个',
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            },
            opposite: true,
            // startOnTick: false,
            // endOnTick: false,
            // tickInterval: 0.01,
            // min: series_increase[0]
            min: series_total[0]-0.08,     //添加最大和最小值后，坐标显示很好，下次需要将增长率也这样，但是需要不断修改才能使图表最漂亮
            max: series_total[series_total.length-1],
            alignTicks: false,
            gridLineWidth: 0
        }],
        tooltip: {
            shared: true
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            x: 120,
            verticalAlign: 'top',
            y: 40,
            floating: true,
            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
        },
        series: [{
            name: '域名WHOS总量',
            type: 'column',
            yAxis: 1,
            data: series_total,
            tooltip: {
                valueSuffix: ' M个'
            }
            
        }, {
            name: '增长率',
            type: 'spline',
            data: series_increase,
            tooltip: {
                valueSuffix: '个'
            }
           
        }]
    });
}

function get_data(start,end) {
    //ajax获取最新统计数据，并更新页面
    var raw_data;
    var categories =[];
    var series_total = [];
    var series_increase = [];
    var flag=false;  //flag用来控制时间截取日期or小时
    if (start==end){
        flag = true;
    }
    $.ajax({
            url: '/detect/increase',
            type: "get",
            data: {
                start: start,
                end: end,
                stamp: Math.random()   // preventing "get" method using cache send to client
            },
            timeout: 5000, //超时时间
            success: function (data) {  //成功后的处理
                
                raw_data = JSON.parse(data); //json格式化原始数据
                var value;
                for(var i=0,arrLength=raw_data.length;i<arrLength;i++){
                    value = raw_data[i]
                    if (flag==true){//添加时间，截取详细时间
                        categories.unshift(value.insert_time.slice(11,value.insert_time.length)); 
                    }
                    else{
                        categories.unshift(value.insert_time.slice(0,10)); 
                    }
                    series_total.unshift((Math.round((value.sum/1000000.0)*1000)/1000)); //添加数量，两位小数，百万级别
                }
                for(var i=1,arrLength=raw_data.length;i<arrLength;i++){
                    series_increase.unshift(raw_data[i-1].sum-raw_data[i].sum)
                }
                init(categories.slice(1,categories.length),series_total.slice(1,series_total.length),series_increase);
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
