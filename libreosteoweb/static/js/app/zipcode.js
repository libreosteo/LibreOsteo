var zipcode = angular.module('loZipCode', []);

/** ZipCodeServ − a service to lookup a Zip code related API
 *
 * Allows to lookup the /zipcode_lookup API to query information about a zip
 * code.
*/

let RE_PARTIAL_ZIPCODE = new RegExp('[0-9]{2,}');


/** Extracts the zipcode (or part of zipcode) from a string
 */
function extractZipCodePart(val) {
    let matches = val.match(RE_PARTIAL_ZIPCODE);
    if (matches) {
        return matches[0];
    } else {
        return null;
    }
}


zipcode.factory('ZipCodeServ', ['$http',
    function($http) {
        return {
            /** Gives the matching cities matching a zipcode
             *
             * @param val : a string containing a zipcode or part of a zipcode
             * @return an array of zipcode informations, with zero to several
             *   items like `{city: 'ACME', zipcode: '12000'}`
             */
            lookup: function(val) {
                let zipCodePart = extractZipCodePart(val)
                if (zipCodePart) {
                    console.log('Looking up…', zipCodePart);
                    return $http.get('/zipcode_lookup/zipcode_lookup/'+zipCodePart).then(
                        function(response){
                            console.debug('received', response.data)
                            return response.data;
                        });
                } else {
                    console.log('Nothing looking like a zipcode in', val)
                }
            }
        }
    }
]);
