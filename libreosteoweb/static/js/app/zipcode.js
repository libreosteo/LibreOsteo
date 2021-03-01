/**
    This file is part of LibreOsteo.

    LibreOsteo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    LibreOsteo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with LibreOsteo.  If not, see <http://www.gnu.org/licenses/>.
*/
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

/** For a given row, tels if it fuzzy-matches the query
 *
 * Matches if all the terms of the words of the query can be found in the
 * row.
 * @rtype bool
 */
function fuzzyMatch(query, row) {
    words = query.split(' ');
    let hasNonMatchingWord = words.some(function(word) {
        return ! (
            row.zipcode.startsWith(word)
            ||
            row.city.toLowerCase().includes(word.toLowerCase())
        );
    });
    return ! hasNonMatchingWord;
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
                            console.debug('received', response.data);
                            let filtered = response.data.filter(
                                x => fuzzyMatch(val, x)
                            );
                            console.debug('after filtering', response.data)
                            return filtered;
                        });
                } else {
                    console.log('Nothing looking like a zipcode in', val)
                }
            }
        }
    }
]);
