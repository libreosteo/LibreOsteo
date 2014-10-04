var user = angular.module('loUser', ['ngResource']);

user.factory('UserServ', ['$resource',
    function ($resource) {
        "use strict";
        return $resource('api/users/:userId', null, {
            get : {method: 'GET', params: {userId: 'user'}},
            'update' : {method : 'PUT' , params : {userId : 'userId'}},
        });
    }
]);

user.controller('UserProfileCtrl', ['$scope', '$http', 'UserServ', 'growl',
    function($scope, $http, UserServ, growl){
        "use strict";
        $scope.userid = null;

        $http.get('myuserid').then(
            function(result){
                $scope.userid = result.data;
                $scope.user = UserServ.get({userId : $scope.userid });
            });

        $scope.updateUser = function(user){
          UserServ.update({userId : $scope.userid }, user).$promise.then(function(user){
              $scope.user = user;
              // Display info that it is updated
              var e = document.getElementById('update-info');
              var text = angular.element(e).text();
              growl.addSuccessMessage(text);
          });
        };
}]);