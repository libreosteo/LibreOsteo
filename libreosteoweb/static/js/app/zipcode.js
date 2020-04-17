var zipcode = angular.module('loZipCode', []);

/** ZipCodeServ − a service to lookup a Zip code related API
 *
 * Allows to lookup the /zipcode_lookup API to query information about a zip
 * code.
*/
zipcode.factory('ZipCodeServ', ['$http',
    function($http) {
        return {
            /** Gives the matching cities matching a zipcode
             *
             * @param val : a full zipcode
             * @return an array of zipcode informations, with zero to several
             *   items like `{city: 'ACME', zipcode: '12000'}`
             */
            lookup: function(val) {
                console.log('Looking up…', val);
                return $http.get('/zipcode_lookup/zipcode_lookup/'+val).then(
                    function(response){
                        console.debug('received', response.data)
                        return response.data;
                    });
            }
        }
    }
]);
