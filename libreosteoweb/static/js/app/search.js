var search = angular.module('loSearch', []);

// Define the Controller in the index.html page
search.controller('SearchCtrl', ['$scope', '$location', function ($scope, $location) {
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
        $location.path('/search/'+$scope.query);
    };
}]);



search.controller('SearchResultCtrl', function($scope, $location){
    "use strict";

});
