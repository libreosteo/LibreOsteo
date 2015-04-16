function getFields(obj)
{
    "use strict";
    var r = [] ;
    for (var k in obj) {
        if (!obj.hasOwnProperty(k))
            continue;
        r.push(k)
    }
    return r ;
}

function formatGrowlError(obj) {
    "use strict";
    var result = "";
    var fields = getFields(obj);

    for (var f = 0; f < fields.length; f++ ){
        result += "<p>"+fields[f] +' :<p/>';
        if (Array.isArray(obj[fields[f]]))
        {
            result += "<ul>";
            var a = obj[fields[f]];
            for (var l = 0 ; l < a.length; l++) {
                result += '<li>'+a[l]+'</li>';
            }
            result += "</ul>";
        } else {
            result += "<p>"+obj[fields[f]]+"</p>";
        }
    }
    return result;
}

String.prototype.endsWith = function(suffix) {
    return this.indexOf(suffix, this.length - suffix.length) !== -1;
};