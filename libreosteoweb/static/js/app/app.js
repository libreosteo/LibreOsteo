
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
var libreosteoApp = angular.module('libreosteo', [
    'ngRoute',
    'ngCookies',
    'xeditable',
    'ui.bootstrap',
    'loPatient',
    'loTimeline',
    'loDashboard',
    'loOfficeEvent',
    'loInvoice',
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
    'loRebuildIndex',
    'ngFileUpload',
    'loFileManager',
    'angular-bind-html-compile'
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
            state('rebuild-index',
                {
                    url : '/office/rebuild-index',
                    templateUrl : 'web-view/partials/rebuild-index',
                    controller : 'RebuildIndexCtrl'
                }).
            state('invoice-list',
            {
                url : '/invoices',
                templateUrl : 'web-view/partials/invoice-list',
                controller : 'InvoiceListCtrl'
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

libreosteoApp.filter('htmlToPlaintext', function() {
    return function(text) {
      return  text ? String(text).replace(/<br[^>]*>/gm, ' ').replace(/<[^>]+>/gm, '') : '';
    };
  }
);

libreosteoApp.filter('mimeTypeToClass', function() {
    return function(text) {
        if (text) {
            if (text.includes('application/pdf')){
                return 'fa-file-pdf-o';
            } else if (text.includes('image/')) {
                return 'fa-file-image-o';
            }
        } 
        return 'fa-file-text-o';
    }
});
