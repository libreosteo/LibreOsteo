var officesettings = angular.module('loOfficeSettings', ['ngResource', 'ui.grid', 'ui.grid.edit', 'ui.grid.cellNav']);

officesettings.factory('OfficeSettingsServ', ['$resource',
    function ($resource) {
        "use strict";
        return $resource('api/settings/:settingsId', null, {
            get : {method: 'GET', isArray : true},
            save : {method : 'PUT'}
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
  'OfficeSettingsServ', 'OfficeUsersServ', 'i18nService',
    function($scope, $http, growl, OfficeSettingsServ, OfficeUsersServ, i18nService){
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
        }

        $scope.addUser = function()
        {
          console.log("Ask for adding user");
        }
}]);