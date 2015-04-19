var officesettings = angular.module('loOfficeSettings', ['ngResource', 'ui.grid', 'ui.grid.edit', 'ui.grid.cellNav']);

officesettings.factory('OfficeSettingsServ', ['$resource',
    function ($resource) {
        "use strict";
        return $resource('api/settings/:settingsId', null, {
            get : {method: 'GET', isArray : true},
            save : {method : 'PUT'},
        });
    }
]);

officesettings.factory('OfficeUsersServ', ['$resource',
  function($resource) {
    return $resource('api/office-users/:userId', null, {
      get : {method : 'GET', params : {userId : 'userId'}},
      save : {method : 'PUT', params: {userId : 'userId'}},
      add : { method : 'POST'},
      query : { method : 'GET', isArray : true},
      setpassword : {method : 'POST', params: {userId : 'userId'}, 
        url : 'api/office-users/:userId/set_password'},
    });
  }
  ]);

officesettings.filter('true_false', function() {
              return function(text, length, end) {
                if (text) {
                  return 'oui';
                }
                return 'non';
              }
          });


officesettings.controller('OfficeSettingsCtrl', ['$scope', '$http', 'growl', 
  'OfficeSettingsServ', 'OfficeUsersServ', 'i18nService', '$modal',
    function($scope, $http, growl, OfficeSettingsServ, OfficeUsersServ, i18nService, $modal){
        "use strict";

        i18nService.setCurrentLang('fr');
        OfficeSettingsServ.get(function(settings){
          $scope.officesettings = settings[0];
          if (!$scope.officesettings)
          {
            $scope.officesettings = {'id' : 1,};
          }
        });

        $scope.users = OfficeUsersServ.query(function(data)
        {
          $scope.users = data;
        });

        $scope.gridOptions = {
          enableSorting: true,
          columnDefs: [
              { name: 'username', field: 'username', enableSorting: true, enableCellEdit : false},
              { name: 'first_name', field: 'first_name', enableSorting : true, displayName : 'Prénom', enableCellEdit : false},
              { name: 'last_name', field: 'last_name', enableSorting : true , displayName : 'Nom',enableCellEdit : false},
              { name: 'is_staff', field: 'is_staff', displayName : 'Administrateur', cellTemplate : '<div class="ui-grid-cell-contents">{$ row.entity.is_staff|true_false$}</div>'},
              { name: 'is_active', field: 'is_active', displayName : 'Actif', cellTemplate: '<div class="ui-grid-cell-contents">{$ row.entity.is_active|true_false$}</div>'},
              { name: 'set_password', type : 'object', displayName : 'Mot de passe', allowCellFocus : false, cellTemplate : '<div class="ui-grid-cell-contents"><button ng-click="grid.appScope.setPassword(row.entity)">modifier</button></div>' }
          ],
          data : $scope.users,
          };
        $scope.gridOptions.onRegisterApi = function(gridApi){
            //set gridApi on scope
            $scope.gridApi = gridApi;
            gridApi.edit.on.afterCellEdit($scope, function(rowEntity, colDef, newValue, oldValue){
              if (newValue != oldValue)
              {
                var data = {
                  'id' : rowEntity.id,
                  'username' : rowEntity.username,
                  'is_staff' : rowEntity.is_staff,
                  'is_active' : rowEntity.is_active,
                }
                OfficeUsersServ.save({userId : rowEntity.id}, data);
              }
            });
        };

        $scope.updateSettings = function(settings) {
          OfficeSettingsServ.save({settingsId : $scope.officesettings.id }, settings).
            $promise.then( function(settings){
              $scope.officesettings = settings;
              // Display info that it is updated
              var e = document.getElementById('update-info');
              var text = angular.element(e).text();
              growl.addSuccessMessage(text);
              },
                function(reason) {
                  // Should display the error
                  if(reason.data.detail) {
                    growl.addErrorMessage(reason.data.detail);
                  } else {
                    growl.addErrorMessage(formatGrowlError(reason.data), {enableHtml:true});
                  }
                });
        };

        $scope.setPassword = function(entity)
        {
          console.log("Ask for change password for "+entity.username);
          var modalInstance = $modal.open({
                templateUrl: 'web-view/partials/set-password-modal',
                controller : 'SetPasswordFormCtrl'
          });
          modalInstance.result.then(function (newPassword){
            OfficeUsersServ.setpassword({userId : entity.id}, newPassword).
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
        };

        $scope.addUser = function()
        {
          var modalInstance = $modal.open({
                templateUrl: 'web-view/partials/add-user-modal',
                controller : 'AddUserFormCtrl'
          });
          modalInstance.result.then(function (newUser){
              OfficeUsersServ.add(newUser).$promise.then(function (data)
                {
                  OfficeUsersServ.setpassword({userId : data.id}, newUser).$promise.then(function (result)
                  { 
                    $scope.users.push(data);
                  });
                });
          });
        }
}]);

officesettings.controller('AddUserFormCtrl', ['$scope', '$modalInstance', 'OfficeUsersServ', '$q',
 function($scope, $modalInstance, OfficeUsersServ, $q) {
    "use strict";
    $scope.user = {
        username : null,
        password : null

    };
    $scope.ok = function () {
      $modalInstance.close($scope.user);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

    $scope.validateUsername = function(value)
    {

      var deferred = $q.defer();

      OfficeUsersServ
        .query(function(data) { 

            var user = data.find(function(element, index, array)
            {
                return element.username == value;
            });
            if (user !== undefined)
            {
              deferred.reject(false);
            } else {
              deferred.resolve(true)
            }
      });

      return deferred.promise;
    };
}
]);

officesettings.controller('SetPasswordFormCtrl', ['$scope', '$modalInstance',
 function($scope, $modalInstance) {
    "use strict";
    $scope.field = {
      password : null
    };

    $scope.ok = function () {
      $modalInstance.close($scope.field);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
}
]);

