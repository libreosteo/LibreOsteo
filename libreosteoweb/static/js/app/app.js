var libreosteoApp = angular.module('libreosteo', [
    'ngRoute',
    'ngCookies',
    'xeditable',
    'ui.bootstrap',
    'loPatient',
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
    'loOfficeSettings',
    'ui.grid',
    'infinite-scroll',
    'loEditFormManager',
    'loHalloEditor',
    'loFileImport',
    'ngFileUpload'
]);

libreosteoApp.config(function ($interpolateProvider) {
  $interpolateProvider.startSymbol('{$');
  $interpolateProvider.endSymbol('$}');
});

libreosteoApp.run(function (editableOptions) {
  editableOptions.theme = 'bs3'; // bootstrap3 theme. Can be also 'bs2', 'default'
});

libreosteoApp.run(['$http', '$cookies', function ($http, $cookies) {
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
    $http.defaults.xsrfCookieName = 'csrftoken';
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
                    var url = 'web-view/partials/search-result?q='+params.query;
                    return url ;
                },
                controller : 'SearchResultCtrl'
            }).
            state('searchPaginated', 
            {
                url : '/search/:query/:page',
                templateUrl : function(params) {
                    var page = '';
                    if(params.page)
                    {  page="&page="+params.page  }
                    var url = 'web-view/partials/search-result?q='+params.query+page;
                    return  url ;
                },
                controller : 'SearchResultCtrl'
            }).
            state('user-profile', 
            {
                url : '/accounts/user-profile',
               templateUrl : 'web-view/partials/user-profile',
                controller : 'UserProfileCtrl'
            }).
            state('office-settings',
            {
                url : '/office/settings',
                templateUrl : 'web-view/partials/office-settings',
                controller : 'OfficeSettingsCtrl'
            }).
            state('import-file',
                {
                    url : '/office/import-file',
                    templateUrl : 'web-view/partials/import-file',
                    controller : 'ImportFileCtrl'
                }).

            state('dashboard',
            {
                url : '/',
                templateUrl : 'web-view/partials/dashboard',
                controller : 'DashboardCtrl'
            });
    }
]);

webshim.setOptions('forms-ext', {
    replaceUI: 'auto',
    types: 'date',
    date: {nopicker: false}
});

// WEBShim configuration
webshim.polyfill('forms-ext');

libreosteoApp.controller('MainController', ['$scope', 'loEditFormManager', function($scope, loEditFormManager) {
	$scope.$on('$viewContentLoaded', function() {
                $('[type="date"].birthdate').prop('max', function(){
                    return new Date().toJSON().split('T')[0];
                });
                $('body').updatePolyfill();
            });

    $scope.editFormManager = loEditFormManager;
}]);
