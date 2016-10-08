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

