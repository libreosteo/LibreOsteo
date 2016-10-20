var rebuildindex = angular.module('loRebuildIndex', ['ngResource']);

rebuildindex.controller('RebuildIndexCtrl', ['$scope','$http', function($scope, $http)
{
    $scope.failed=false;
    $scope.finished=false;
    $scope.rebuildindex = function() {
      $http( {
                method: 'GET',
                url : 'internal/rebuild_index'
            }).then( function success(response)
            {
                $scope.finished = true;
            }, function error(response) {
                scope.failed = true
            });
    };
}]);