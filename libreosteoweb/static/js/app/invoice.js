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
var invoices = angular.module('loInvoice', ['ngResource']);


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

        $scope.invoices = [];
        InvoiceService.query(function(result) {
            $scope.invoices = result;
        });
    }
]);
