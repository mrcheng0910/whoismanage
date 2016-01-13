function tbDetail(tbName){
    url = '/table/increase/detail?table='+tbName;
    layer.open({
        type: 2,
        title: null,
        // closeBtn: false,
        shadeClose: true,
        shade: 0.8,
        area: ['55%', '56%'],
        content: url
    });

}



