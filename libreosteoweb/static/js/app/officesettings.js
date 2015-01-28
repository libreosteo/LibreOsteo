var officesettings = angular.module('loOfficeSettings', ['ngResource']);

officesettings.factory('OfficeSettingsServ', ['$resource',
    function ($resource) {
        "use strict";
        return $resource('api/settings/:settingsId', null, {
            get : {method: 'GET', isArray : true},
            save : {method : 'PUT'}
        });
    }
]);

officesettings.controller('OfficeSettingsCtrl', ['$scope', '$http', 'growl', 'OfficeSettingsServ',
    function($scope, $http, growl, OfficeSettingsServ){
        "use strict";

        OfficeSettingsServ.get(function(settings){
          $scope.officesettings = settings[0];
          if (!$scope.officesettings)
          {
            $scope.officesettings = {'id' : 1,};
          }
        });

        $scope.updateSettings = function(settings) {
          OfficeSettingsServ.save({settingsId : $scope.officesettings.id }, settings).
            $promise.then( function(settings){
              $scope.officesettings = settings;
              // Display info that it is updated
              var e = document.getElementById('update-info');
              var text = angular.element(e).text();
              growl.addSuccessMessage(text);
              });
        };
}]);