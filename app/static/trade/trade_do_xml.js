function loadXMLStr(text) {
    try //Internet Explorer
    {
        xmlDoc = new ActiveXObject("Microsoft.XMLDOM");
        xmlDoc.async = "false";
        xmlDoc.loadXML(text);
    }
    catch (e) {
        try //Firefox, Mozilla, Opera, etc.
        {
            parser = new DOMParser();
            xmlDoc = parser.parseFromString(text, "text/xml");
            return xmlDoc;
        }
        catch (e) {
            alert(e.message)
        }
    }
}


function add(var1, var2, var3, var4) {
    xmlDoc = loadXMLStr('<?xml version="1.0" encoding="UTF-8"?>\n' +
        '<trades>\n' +
        '</trades>');
    newcustomer = xmlDoc.createElement('trade');


    newname = xmlDoc.createElement('customer');
    newtext = xmlDoc.createTextNode(var1);
    newname.appendChild(newtext);
    newcustomer.appendChild(newname);

    sex = xmlDoc.createElement('product');
    newtext = xmlDoc.createTextNode(var2);
    sex.appendChild(newtext);
    newcustomer.appendChild(sex);

    age = xmlDoc.createElement('num');
    newtext = xmlDoc.createTextNode(var3);
    age.appendChild(newtext);
    newcustomer.appendChild(age);

    phone = xmlDoc.createElement('total');
    newtext = xmlDoc.createTextNode(var4);
    phone.appendChild(newtext);
    newcustomer.appendChild(phone);

    x = xmlDoc.getElementsByTagName('trades')[0];
    x.appendChild(newcustomer);

    return xmlDoc;
}


function prase_xml(data1) {
    data_list = [];
    data1 = data1.substring(1, data1.length - 1);
    var data = JSON.parse(data1);
    data = data['trades'];
    if (!data.length)
        return '';
    for (i = 0; i < data.length; i++) {
        item_customer = {};
        item_customer['id'] = data[i].id;
        var xmlDoc = loadXMLStr(data[i].info);
        item_customer['customer'] = xmlDoc.getElementsByTagName('customer')[0].childNodes[0].nodeValue;
        item_customer['product'] = xmlDoc.getElementsByTagName('product')[0].childNodes[0].nodeValue;
        item_customer['num'] = xmlDoc.getElementsByTagName('num')[0].childNodes[0].nodeValue;
        item_customer['total'] = xmlDoc.getElementsByTagName('total')[0].childNodes[0].nodeValue;
        data_list.push(item_customer)
    }
    return data_list
}

function get_xml(data1) {
    content = '<tr>';
    //console.log(data1)
    data1 = data1.substring(1, data1.length - 1)
    var data = JSON.parse(data1);
    //var data = eval('(' + data + ')');
    data = data['trades'];
    //console.log(data)
    if (!data.length)
        return '';
    for (i = 0; i < data.length; i++) {
        content += '<td>' + data[i].id + '</td>';
        console.log(data[i].info)
        content += xml2obj(data[i].info);
        content += '<td><a class="btn" onclick="javascript:modify(this)" >M</a></td>';
        content += '<td><a class="btn" onclick="javascript:del(' + data[i].id + ')" >X</a></td>';
        content += '</tr>';
    }


    return content;
}

function xml2obj(str) {
    var xmlDoc = loadXMLStr(str)
    // var customer = xmlDoc.getElementsByTagName('customers');
    var name = xmlDoc.getElementsByTagName('customer')[0].childNodes[0].nodeValue;
    var sex = xmlDoc.getElementsByTagName('product')[0].childNodes[0].nodeValue;
    var age = xmlDoc.getElementsByTagName('num')[0].childNodes[0].nodeValue;
    var phone = xmlDoc.getElementsByTagName('total')[0].childNodes[0].nodeValue;
    // console.log(xmlDoc.documentElement);
    //  x = xmlDoc.documentElement.childNodes[0].childNodes;
    //  console.log(x[0]);
    content = '';
    content += '<td>' + name + '</td>';
    content += '<td>' + sex + '</td>';
    content += '<td>' + age + '</td>';
    content += '<td>' + phone + '</td>';
    //console.log(xmlDoc[0].childNodes[0].nodeValue);
    //  content = ''
    //  for (i=0;i<x.length;i++){
    //
    //          content += '<td>'+x[i].childNodes[0].nodeValue + '</td>'
    //  }
    return content;
}

function del(id) {
    $.ajax({
        url: '/trade/del?id=' + id,
        data: null,
        type: 'get',
        success: function (data) {
            if (data.msg == 'success') {
                location.reload();
            }
        }
    });
}

function modify(obj) {
    var $td = $(obj).parents('tr').children('td');
    var id = $td.eq(0).text();
    // var name = $td.eq(1).text();
    // var sex = $td.eq(2).text();
    // var age = $td.eq(3).text();
    // var phone = $td.eq(4).text();

    window.location.href = '/trade/getModify?id=' + id;

}
