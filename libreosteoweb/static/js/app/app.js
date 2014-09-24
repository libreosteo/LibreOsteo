var libreosteoApp = angular.module('libreosteo', [
    'ngRoute',
    'ngCookies',
    'xeditable',
    'ui.bootstrap',
    'loTypeAhead',
    'loPatient',
    'loInlineEdit',
    'loTimeline',
    'yaru22.angular-timeago',
    'ngAnimate',
     'duScroll',
]);

libreosteoApp.config(function ($interpolateProvider) {
  $interpolateProvider.startSymbol('{$');
  $interpolateProvider.endSymbol('$}');
});

libreosteoApp.run(function (editableOptions) {
  editableOptions.theme = 'bs3'; // bootstrap3 theme. Can be also 'bs2', 'default'
});

libreosteoApp.run(['$http', '$cookies', function ($http, $cookies) {
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.headers.put['X-CSRFToken'] = $cookies.csrftoken;
    //$http.defaults.headers.delete['X-CSRFToken'] = $cookies.csrftoken;
}]);

libreosteoApp.config(['$routeProvider',
    function ($routeProvider) {
        $routeProvider.
            when('/patient/:patientId',
            {
                templateUrl : 'web-view/partials/patient-detail',
                controller : 'PatientCtrl'
            }).
            when('/addPatient',
            {
                templateUrl : 'web-view/partials/add-patient',
                controller : 'AddPatientCtrl'
            }
            ).
            otherwise({
               redirectTo : '/'
            });
    }
]);