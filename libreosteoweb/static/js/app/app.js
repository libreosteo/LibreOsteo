var libreosteoApp = angular.module('libreosteo', [
    'ngRoute',
    'ngCookies',
    'xeditable',
    'ui.bootstrap',
    'loPatient',
    'loInlineEdit',
    'loTimeline',
    'loDashboard',
    'yaru22.angular-timeago',
    'ngAnimate',
     'duScroll',
    'loSearch',
    'loUser',
    'angular-growl',
    'angular-loading-bar',
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

libreosteoApp.config(['growlProvider', function(growlProvider) {
    growlProvider.globalTimeToLive(5000);
    growlProvider.onlyUniqueMessages(false);
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
            when('/search/:query',
            {
                templateUrl : function(params) {
                    return 'web-view/partials/search-result?q='+params.query ;
                },
                controller : 'SearchResultCtrl'
            }).
            when('/search/:query/:page',
            {
                templateUrl : function(params) {
                    page = '';
                    if(params.page)
                    {  page="&page="+params.page  }
                    return 'web-view/partials/search-result?q='+params.query+page ;
                },
                controller : 'SearchResultCtrl'
            }).
            when('/accounts/user-profile',
            {
               templateUrl : 'web-view/partials/user-profile',
                controller : 'UserProfileCtrl'
            }).
            when('/',
            {
                templateUrl : 'web-view/partials/dashboard',
                controller : 'DashboardCtrl'
            }).
            otherwise({
               redirectTo : '/'
            });
    }
]);

// WEBShim configuration
webshim.polyfill('forms forms-ext');

libreosteoApp.controller('MainController', ['$scope', function($scope) {
	$scope.$on('$viewContentLoaded', function() {
                $('body').updatePolyfill();
            });
}]);
