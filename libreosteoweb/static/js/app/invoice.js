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
var invoices = angular.module('loInvoice', ['ngResource', 'daterangepicker']);

invoices.factory('InvoiceService', ['$resource', function ($resource) {
    "use strict";
    return $resource('api/invoices/:InvoiceId', null, {
        query: {method: 'GET' , isArray: true},
        get : {method: 'GET', params: {InvoiceId: 'invoiceId'}},
        save : {method : 'PUT', params : {InvoiceId : 'InvoiceId'}},
        add : {method : 'POST'},
        delete : { method : 'DELETE', params : {InvoiceId : 'InvoiceId'}},
    });
}]);


invoices.controller('InvoiceListCtrl', ['$scope','InvoiceService',
    function($scope, InvoiceService) {
        "use strict";

        function getInvoices() {
            var params = {};
            InvoiceService.query(
                {
                    date__lte: $scope.filters.dateRange.endDate.toISOString(),
                    date__gte: $scope.filters.dateRange.startDate.toISOString(),
                },
                function(result) {
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


        $scope.invoices = [];

        // Daterangepicker configuration
        // http://www.daterangepicker.com/#options
        $scope.daterangePickerOptions = {
            opens: 'center',
            ranges: makeMomentRanges(),
            autoApply: true,
        }

        $scope.filters = {
            dateRange: {
                startDate: moment().startOf('month'),
                endDate: moment().endOf('month')
            },
        };

        // Initial API call
        getInvoices();
        // Refresh & filter from API on new date selection
        $scope.$watch('filters.dateRange', getInvoices);

        $scope.openCalendar = function(){
            // This is a hack to open the calendar programatically
            angular.element('input#billing-period').triggerHandler('click');
        }

    }
]);
