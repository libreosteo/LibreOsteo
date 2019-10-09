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
var invoices = angular.module('loInvoice', ['ngResource', 'daterangepicker', 'loUser', 'loOfficeSettings']);

invoices.factory('InvoiceService', ['$resource', function ($resource) {
    "use strict";
    return $resource('api/invoices/:invoiceId', null, {
        query: {method: 'GET' , isArray: true},
        get : {method: 'GET', params: {invoiceId: 'invoiceId'}},
        cancel : {
          method: 'POST',
          params:{invoiceId: 'invoiceId'},
          url : 'api/invoices/:invoiceId/cancel'
        }
    });
}]);


/** Localize daterangepicker using django built-in mechanisms
 */
function localizeDaterangePicker() {
    return {
            customRangeLabel: django.gettext("Custom range"),
            daysOfWeek: [
                django.gettext("Su"),
                django.gettext("Mo"),
                django.gettext("Tu"),
                django.gettext("We"),
                django.gettext("Th"),
                django.gettext("Fr"),
                django.gettext("Sa")
            ],
            monthNames: [
                django.gettext("January"),
                django.gettext("February"),
                django.gettext("March"),
                django.gettext("April"),
                django.gettext("May"),
                django.gettext("June"),
                django.gettext("July"),
                django.gettext("August"),
                django.gettext("September"),
                django.gettext("October"),
                django.gettext("November"),
                django.gettext("December")
            ],
            firstDay: django.get_format('FIRST_DAY_OF_WEEK'),
    };
}

invoices.controller('InvoiceListCtrl', ['$scope','InvoiceService', 'MyUserIdServ', 'OfficeUsersServ','$uibModal',
    function($scope, InvoiceService, MyUserIdServ, OfficeUsersServ, $uibModal) {
        "use strict";

        function buildAPIFilter() {
            return {
                date__lte: $scope.filters.dateRange.endDate.toISOString(),
                date__gte: $scope.filters.dateRange.startDate.toISOString(),
		            therapeut_id : $scope.filters.therapeut_id,
            };
        }

        function getInvoices() {
            InvoiceService.query(buildAPIFilter(), function(result) {
                $scope.invoices = result;
            });
        }

        /** Prepare pre-defined ranges for daterangepicker
         *
         *  http://www.daterangepicker.com/#ex4
         */
        function makeMomentRanges() {
            var ranges = {}
            ranges[moment().format('MMMM YYYY')] = [
                moment().startOf('month'),
                moment().endOf('month')
            ];
            ranges[moment().format('YYYY')] = [
                moment().startOf('year'),
                moment().endOf('year')
            ]
            ranges[moment().subtract(1, 'year').format('YYYY')] = [
                moment().subtract(1, 'year').startOf('year'),
                moment().subtract(1, 'year').endOf('year')
            ];
            return ranges;
        }

	      $scope.user = MyUserIdServ.then(function(result) {
          $scope.user = result;
          if ($scope.filters)
          {
            $scope.filters.therapeut_id = $scope.user.id;
            getInvoices();
          }
        });
	      $scope.users = OfficeUsersServ.query();

        $scope.invoices = [];

        // Daterangepicker configuration
        // http://www.daterangepicker.com/#options
        $scope.daterangePickerOptions = {
            opens: 'center',
            ranges: makeMomentRanges(),
            autoApply: true,
            locale: localizeDaterangePicker()
        }

        $scope.filters = {
            dateRange: {
                startDate: moment().startOf('month'),
                endDate: moment().endOf('month')
            },
		        therapeut_id : $scope.user.id
        };

        // Refresh & filter from API on new date selection
        $scope.$watch('filters.dateRange', getInvoices);

        $scope.openCalendar = function(){
            // This is a hack to open the calendar programatically
            angular.element('input#billing-period').triggerHandler('click');
        }

        $scope.buildCsvUrl = function(fields) {
            var queryDict = buildAPIFilter();
            var url = '/api/invoices.csv?';

            if (fields) {
                queryDict.fields = fields
            }

            for (var key in queryDict) {
                url += key + '=' + queryDict[key]+'&'
            }
            return url.slice(0, -1)
        }
      $scope.changeTherapeut = function(user) {
        $scope.user = user;
        $scope.filters.therapeut_id = user.id;
        getInvoices();
      };

      $scope.cancelInvoice = function(invoice) {
        var modalInstance = $uibModal.open({
          templateUrl: 'web-view/partials/confirmation-modal',
          controller : ConfirmationCtrl,
          resolve : {
            message : function() {
              return "<p>"+gettext("Are you sure to cancel this invoice ?")+"</p>";
            },
            defaultIsOk : function() {
              return true;
            }
          }
        });
        modalInstance.result.then(function (){
          InvoiceService.cancel({invoiceId : invoice.id },null, function (result) {
            getInvoices();
          });
        });
      };
    }
]);

var ConfirmationCtrl = function($scope, $uibModalInstance, message, defaultIsOk) {
    $scope.message = message;
    $scope.ok = function () {
      $uibModalInstance.close();
    };

    $scope.isOk = defaultIsOk;

    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
}

