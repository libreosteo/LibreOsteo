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

Array.prototype.find = function(predicate, thisArg) {
    "use strict";
    //TODO: Check predicate is a function.
    var lastValue;
    if(!Array.prototype.some.call(this, function(val, index, arr) {
        return predicate.call(thisArg, lastValue = val, index, arr);
    })) {
        return;
    }
    return lastValue;
}


function convertUTCDateToLocalDate(date) {
    var newDate = new Date(date.getTime()+date.getTimezoneOffset()*60*1000);

    var offset = date.getTimezoneOffset() / 60;
    var hours = date.getHours();

    newDate.setHours(hours - offset);

    return newDate;   
}