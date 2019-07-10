
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
var installer = angular.module('libreosteoinstaller', [
    'ngRoute',
    'ngCookies',
    'ui.bootstrap',
    'ngAnimate',
    'angular-loading-bar',
    'ui.router',
    'ngFileUpload',
    'installerRestore',
]);

installer.config(function ($interpolateProvider) {
  $interpolateProvider.startSymbol('{$');
  $interpolateProvider.endSymbol('$}');
});

installer.run(['$http', '$cookies', function ($http, $cookies) {
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
    $http.defaults.xsrfCookieName = 'csrftoken';
}]);

installer.config(['$stateProvider', '$urlRouterProvider',
    function ($stateProvider, $urlRouterProvider) {
        $urlRouterProvider.otherwise('/');

        $stateProvider.
            state('restore', 
            {
                url : '/restore',
                templateUrl : '/web-view/partials/restore',
                controller : 'RestoreCtrl'
            }).
            state('register',
            {
                url : '/register',
                templateUrl : '/web-view/partials/register',
                controller : 'RegisterCtrl'
            })
            ;
    }
]);

installer.controller('MainController', ['$scope', '$state', function($scope, $state) {
    $scope.prepare_restore = function()
    {
        $state.go('restore');
    };

    $scope.prepare_register = function()
    {
        $state.go('register');
    };
}]);

