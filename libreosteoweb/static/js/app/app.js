var libreosteoApp = angular.module('libreosteo', [
    'ngRoute',
    'ngCookies',
    'xeditable',
    'loTypeAhead',
    'loPatient'
]);

libreosteoApp.config(function ($interpolateProvider) {
  $interpolateProvider.startSymbol('{$');
  $interpolateProvider.endSymbol('$}');
});

libreosteoApp.run(function (editableOptions) {
  editableOptions.theme = 'bs3'; // bootstrap3 theme. Can be also 'bs2', 'default'
});

libreosteoApp.run(['$http','$cookies', function ($http, $cookies) {
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.headers.put['X-CSRFToken'] = $cookies.csrftoken;
    //$http.defaults.headers.delete['X-CSRFToken'] = $cookies.csrftoken;
}]);

libreosteoApp.config(['$routeProvider',
    function ($routeProvider) {
        $routeProvider.
            when('/patient/:patientId',
            {
                templateUrl : 'web-view/partials/patient-detail.html',
                controller : 'PatientCtrl'
            }).
            otherwise({
               redirectTo : '/'
            });
    }
]);