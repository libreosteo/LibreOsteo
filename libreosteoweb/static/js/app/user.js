
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
var user = angular.module('loUser', ['ngResource']);

user.factory('UserServ', ['$resource',
    function ($resource) {
        "use strict";
        return $resource('api/users/:userId', null, {
            get : {method: 'GET', params: {userId: 'user'}},
            'update' : {method : 'PUT' , params : {userId : 'userId'}},
            setpassword : {method : 'POST', params: {userId : 'userId'},
                    url : 'api/office-users/:userId/set_password'},
	    query : {method: 'GET', isArray : true }
        });
    }
]);

user.factory('MyUserIdServ', ['$http', 'UserServ',
		function($http, UserServ) {
      return $http.get('myuserid').then(
        function(result){
          return UserServ.get({userId : result.data }).$promise.then(function(data) {
            data.id = result.data;
            return data;
            });
          });
		}]);

user.factory('TherapeutSettingsServ', ['$resource',
  function($resource) {
    "use strict";
    return $resource('api/profiles/:settingsId', null, {
        get : {method : 'GET', params: {settingsId : 'settings'}},
        save : {method : 'PUT'},
        'get_by_user' : {method : 'GET', url: 'api/profiles/get_by_user'},
      });
  }
]);

user.controller('UserProfileCtrl', ['$scope', '$http', 'UserServ', 'TherapeutSettingsServ', 'growl','$uibModal',
    function($scope, $http, UserServ, TherapeutSettingsServ, growl, $uibModal){
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
              TherapeutSettingsServ.save({settingsId : $scope.therapeutsettings.id}, $scope.therapeutsettings).$promise.then(callback);
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
        $scope.setPassword = function()
        {
          var uibModalInstance = $uibModal.open({
                templateUrl: 'web-view/partials/set-password-modal',
                controller : 'SetPasswordFormCtrl'
          });
          uibModalInstance.result.then(function (newPassword){
            UserServ.setpassword({userId : $scope.userid}, newPassword).
              $promise.then( function(result)
                {
                  growl.addSuccessMessage("Le mot de passe a été modifié.")
                },
                  function(reason) {
                    // Should display the error
                    if(reason.data.detail) {
                      growl.addErrorMessage(reason.data.detail);
                    } else {
                      growl.addErrorMessage(formatGrowlError(reason.data), {enableHtml:true});
                    }
                  });
                });
        }
}])
.controller('SetPasswordFormCtrl', ['$scope', '$uibModalInstance',
 function($scope, $uibModalInstance) {
    "use strict";
    $scope.field = {
      password : null
    };

    $scope.ok = function () {
      $uibModalInstance.close($scope.field);
    };

    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
}
]);
