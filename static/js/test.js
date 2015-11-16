function domain(domains) {
    var test = new Array()
    for (var i=0;i<domains.length;i++){
        test[i] = new Array(domains[i].tld_name,domains[i].domain_num)
     }
     document.write(test[0])

};