
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
var officesettings = angular.module('loOfficeSettings', ['ngResource',
  'ui.grid', 'ui.grid.edit', 'ui.grid.cellNav'
  ]);

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

officesettings.factory('OfficePaimentMeansServ', ['$resource',
		function($resource) {
			return $resource('api/paiment-mean/:paimentMeanId', null, {
				get : {method :  'GET', params: {paimentMeanId : 'paimentMeanId'}},
				save : {method : 'PUT', params: {paimentMeanId: 'paimentMeanId'}},
				add : {method: 'POST'},
				query : {method: 'GET', isArray: true}
			});
		}]);

officesettings.filter('true_false', function() {
              return function(text, length, end) {
                if (text) {
                  return 'oui';
                }
                return 'non';
              }
          });

officesettings.directive("validateInvoiceStart", function() {
  return {
    require: 'ngModel',
    link: function(scope, elm, attrs, ctrl) {
      ctrl.$validators.validateInvoiceStart = function(modelValue, viewValue) {
        if (!isNaN(modelValue) && modelValue >= scope.officesettings.invoice_min_sequence) {
          return true;
        }
        return false;
      }
    }
  }
});

officesettings.controller('OfficeSettingsCtrl', ['$scope', '$http', 'growl',
  'OfficeSettingsServ', 'OfficeUsersServ', 'OfficePaimentMeansServ', 'i18nService', '$uibModal', '$q',
    function($scope, $http, growl, OfficeSettingsServ, OfficeUsersServ, OfficePaimentMeansServ, i18nService, $uibModal, $q){
        "use strict";

        i18nService.setCurrentLang('fr');
        OfficeSettingsServ.get(function(settings){
            $scope.officesettings = settings[0];
        });

        $scope.users = OfficeUsersServ.query(function(data)
        {
          $scope.users = data;
        });

	$scope.paiment_means = OfficePaimentMeansServ.query(function(data)
			{
				$scope.paiment_means = data;
			});
        
        $scope.gridOptions = {
          enableSorting: true,
          columnDefs: [
              { name: 'username', field: 'username', enableSorting: true, enableCellEdit : false},
              { name: 'first_name', field: 'first_name', enableSorting : true, displayName : 'Prénom', enableCellEdit : true},
              { name: 'last_name', field: 'last_name', enableSorting : true , displayName : 'Nom',enableCellEdit : true},
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
                  'first_name': rowEntity.first_name,
                  'last_name' : rowEntity.last_name,
                  'is_staff' : rowEntity.is_staff,
                  'is_active' : rowEntity.is_active,
                }
                OfficeUsersServ.save({userId : rowEntity.id}, data);
              }
            });
        };

	$scope.resetPaimentMeans = function(paimentmeans) {
		angular.forEach($scope.paiment_means, function(paiment_mean, key) {
			angular.forEach(paimentmeans, function(update, key) {
				if (paimentmeans.id == this.id) {
					this.enable = paimentmeans.enable;
				}

			}, paiment_mean);
		});
    return $scope.paiment_means;
	};

	$scope.updateSettings = function(settings) {
		var update1 = OfficeSettingsServ.save({settingsId : $scope.officesettings.id }, settings);
		var updatePromises = [ update1.$promise ];
		angular.forEach($scope.paiment_means, function(paimentmean, key) {
			var updatePaimentMean = OfficePaimentMeansServ.save({paimentMeanId : paimentmean.id}, paimentmean);
			this.push(updatePaimentMean.$promise);
		}
		, updatePromises);
		$q.all(updatePromises).then(function(settings) {
      $scope.officesettings = settings[0];
			$scope.paiment_means = $scope.resetPaimentMeans(settings.slice(0));
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
          var modalInstance = $uibModal.open({
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
          var modalInstance = $uibModal.open({
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

officesettings.controller('AddUserFormCtrl', ['$scope', '$uibModalInstance', 'OfficeUsersServ', '$q',
 function($scope, $uibModalInstance, OfficeUsersServ, $q) {
    "use strict";
    $scope.user = {
        username : null,
        password : null

    };
    $scope.ok = function () {
      $uibModalInstance.close($scope.user);
    };

    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
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

officesettings.controller('SetPasswordFormCtrl', ['$scope', '$uibModalInstance',
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

