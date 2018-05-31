
/**
    This file is part of Libreosteo.

    Libreosteo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Libreosteo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Libreosteo.  If not, see <http://www.gnu.org/licenses/>.
*/

var utils = angular.module('loUtils', []) ;

utils.filter('translate', function() {
	return function(input) {
		if(input){
			return gettext(input);
		}
	};
});

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
