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

user.factory('TherapeutSettingsServ', ['$resource', 
  function($resource) {
    "use strict";
    return $resource('api/profiles/:settingsId', null, {
        get : {method : 'GET', params: {settingsId : 'settings'}},
        add : {method : 'POST'},
        save : {method : 'PUT'},
        'get_by_user' : {method : 'GET', url: 'api/profiles/get_by_user'},
      });
  }
]);

user.controller('UserProfileCtrl', ['$scope', '$http', 'UserServ', 'TherapeutSettingsServ', 'growl',
    function($scope, $http, UserServ, TherapeutSettingsServ, growl){
        "use strict";
        $scope.userid = null;

        $http.get('myuserid').then(
            function(result){
                $scope.userid = result.data;
                $scope.user = UserServ.get({userId : $scope.userid });
                $scope.therapeutsettings = TherapeutSettingsServ.get_by_user();
            });


        $scope.updateUser = function(user, therapeutsettings){
          
          var manageTherapeutSettings = function (callback) {
            if ($scope.therapeutsettings.id)
            {
              TherapeutSettingsServ.save({settingsId : $scope.therapeutsettings.id}, $scope.therapeutsettings).$promise.then(callback);
            } else {
              TherapeutSettingsServ.add($scope.therapeutsettings).$promise.then(callback);
            }
          }

          UserServ.update({userId : $scope.userid }, user).
            $promise.then( function(user){
                            manageTherapeutSettings( function ( settings )
                            {
                              $scope.user = user;
                              $scope.therapeutsettings = settings;
                              // Display info that it is updated
                              var e = document.getElementById('update-info');
                              var text = angular.element(e).text();
                              growl.addSuccessMessage(text);
                            })
            });
          }
}]);