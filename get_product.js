var page = require('webpage').create(),
    system = require('system'),
    postPage = require('webpage').create();
var data = "",
    re_price = /"price": ([0-9]+)/g,
    re_id = /"id": ([0-9]+)/g,
    // re_img_url = /"pictureUrl": "([^"]+)"/g,
    // re_vendor = /'vendor': '([^']+)'/g,
    // re_name = /                'name': '([^']+)'/g,
    // re_typePrefix = /'typePrefix': '([^']+)'/g,
    re_publish = /Товар распродан/;
    // re_params = /"params": (\{[^\}]+\})/g,
    // re_comma = /,[^А-яA-z]+}/g,
    // re_quote= /&#034;\(/g;
page.settings.loadImages=false;
page.settings.javascriptEnabled=false;
page.open(system.args[1], function() {
    // if (status !== 'success') {
    //     console.log('success');
    // }

    data+="price="+re_price.exec(page.content)[1];

    data+="&id="+re_id.exec(page.content)[1];

    // data+="&img_src=http:"+re_img_url.exec(page.content)[1];
    // data+="&vendor="+re_vendor.exec(page.content)[1];
    //
    // data+="&name="+re_name.exec(page.content)[1];
    //
    // data+="&typePrefix="+re_typePrefix.exec(page.content)[1];
    if (re_publish.test(page.content)) data+="&publish="+'false';
    // data+="&category_id="+system.args[3];
    data+="&murl="+system.args[1];

    // var params = re_params.exec(page.content)[1];
    //
    //   if (re_comma.exec(params) != null) params = params.replace(re_comma, '}');
    //   if (re_quote.exec(params) != null) params = params.replace(re_quote, "''(");
    //
    //     data += "&params=" + params;

    postPage.open("http://dielstore.ru/set_product/", 'post', encodeURI(data.replace(/[\s]{2}|[\n\t]+/g, "")), function (status) {
        // if (status !== 'success') {
        //     console.log('Unable to post!');
        // } else {
        //     console.log("post success");
        // }
        phantom.exit();
    });

});