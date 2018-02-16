
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
var search = angular.module('loSearch', []);

// Define the Controller in the index.html page
search.controller('SearchCtrl', ['$scope', '$location', '$templateCache', '$state',  
    function ($scope, $location, $templateCache, $state) {
        $scope.query = '';
        $scope.onEnterKeyDown = function($event)
        {
            "use strict";
            if($event.keyCode == 13)
            {
                $scope.search();
            }
        }
        $scope.search = function()
        {
            var url = $state.get('search').templateUrl({query : $scope.query});
            $templateCache.remove(url);
            $location.path('/search/'+$scope.query);
        };
}]);



search.controller('SearchResultCtrl', function($scope, $location){
    "use strict";

});
