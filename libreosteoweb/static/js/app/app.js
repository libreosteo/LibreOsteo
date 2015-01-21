var libreosteoApp = angular.module('libreosteo', [
    'ngRoute',
    'ngCookies',
    'xeditable',
    'ui.bootstrap',
    'loPatient',
    'loInlineEdit',
    'loTimeline',
    'loDashboard',
    'loOfficeEvent',
    'yaru22.angular-timeago',
    'ngAnimate',
     'duScroll',
    'loSearch',
    'loUser',
    'angular-growl',
    'angular-loading-bar',
    'ui.router',
    'angular-toArrayFilter',
    'ui.validate',
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

libreosteoApp.config(['$stateProvider', '$urlRouterProvider',
    function ($stateProvider, $urlRouterProvider) {
        $urlRouterProvider.otherwise('/');

        $stateProvider.
            state('patient', 
            {
                url : '/patient/{patientId}',
                templateUrl : 'web-view/partials/patient-detail',
                controller : 'PatientCtrl'
            }).
            state('patient.examinations',
            {
                url : '/examinations',

            }).
            state('patient.examination',
            {
                url : '/examination/{examinationId}',
            }).
            state('addPatient',
            {
                url : '/addPatient',
                templateUrl : 'web-view/partials/add-patient',
                controller : 'AddPatientCtrl'
            }).
            state('search', 
            {
                url : '/search/:query',
                templateUrl : function(params) {
                    return 'web-view/partials/search-result?q='+params.query ;
                },
                controller : 'SearchResultCtrl'
            }).
            state('searchPaginated', 
            {
                url : '/search/:query/:page',
                templateUrl : function(params) {
                    page = '';
                    if(params.page)
                    {  page="&page="+params.page  }
                    return 'web-view/partials/search-result?q='+params.query+page ;
                },
                controller : 'SearchResultCtrl'
            }).
            state('user-profile', 
            {
                url : '/accounts/user-profile',
               templateUrl : 'web-view/partials/user-profile',
                controller : 'UserProfileCtrl'
            }).

            state('dashboard',
            {
                url : '/',
                templateUrl : 'web-view/partials/dashboard',
                controller : 'DashboardCtrl'
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
