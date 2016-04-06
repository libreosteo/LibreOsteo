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
