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
var examination = angular.module('loExamination', ['ngResource', 'loInvoice']);


examination.factory('ExaminationServ', ['$resource',
  function($resource) {
    "use strict";
    return $resource('api/examinations/:examinationId', null, {
      query: {
        method: 'GET',
        isArray: true
      },
      get: {
        method: 'GET',
        params: {
          examinationId: 'examination'
        }
      },
      save: {
        method: 'PUT'
      },
      add: {
        method: 'POST'
      },
      close: {
        method: 'POST',
        params: {
          examinationId: 'examinationId'
        },
        url: 'api/examinations/:examinationId/close'
      },
      invoice: {
        method: 'POST',
        params: {
          examinationId: 'examinationId'
        },
        url: 'api/examinations/:examinationId/invoice'
      },
      delete: {
        method: 'DELETE',
        params: {
          examinationId: 'examinationId'
        }
      },
      update_paiement: {
        method: 'POST',
        url: 'api/examinations/:examinationId/update_paiement',

      }
    });
  }
]);

examination.factory('ExaminationCommentServ', ['$resource',
  function($resource) {
    return $resource('api/examinations/:examinationId/comments', null, {
      query: {
        method: 'GET',
        isArray: true
      },
    });
  }
]);

examination.factory('CommentServ', ['$resource',
  function($resource) {
    return $resource('api/comments', null)
  }
]);

examination.controller('ExaminationCtrl', ['$scope', '$routeParams', 'ExaminationServ', function($scope, $routeParams, ExaminationServ) {
  "use strict";
  $scope.examination = ExaminationServ.get({
    examinationId: $routeParams.examinationId
  });
}]);

function isEmpty(str) {
  return (!str || 0 === str.length);
}


examination.directive('examination', ['ExaminationServ', function(ExaminationServ) {
  "use strict";
  return {
    restrict: 'E',
    scope: {
      model: '=',
      saveModel: '&',
      close: '&',
      closeHandle: '&',
      newExamination: '=',
      onDelete: '&',
      reloadExaminations : '&'
    },
    compile: function(element, attrs) {
      if (!attrs.newExamination) {
        attrs.newExamination = false
      }

    },
    controller: ['$scope', '$filter', '$window', 'growl', '$q', '$timeout', 'InvoiceService', '$uibModal', function($scope, $filter, $window, growl, $q, $timeout, InvoiceService, $uibModal) {
      $scope.types = [{
          value: 1,
          text: gettext('Normal examination')
        },
        {
          value: 2,
          text: gettext('Continuing examination')
        },
        {
          value: 3,
          text: gettext('Return')
        },
        {
          value: 4,
          text: gettext('Emergency')
        },
      ];
      $scope.showTypes = function() {
        if ($scope.model) {
          var selected = $filter('filter')($scope.types, {
            value: $scope.model.type
          });
          return ($scope.model && $scope.model.type && selected.length) ? selected[0].text : gettext('not documented');
        } else {
          return gettext('not documented');
        }
      };

      $scope.examinationSettings = {
        orl: false,
        visceral: false,
        pulmo: false,
        uro_gyneco: false,
        periphery: false,
        general_state: false,
      }

      $scope.accordionOpenState = {
        orl: true,
        visceral: true,
        pulmo: true,
        uro_gyneco: true,
        periphery: true,
        general_state: true
      }

      $scope.$watch('model.orl', function(newValue, oldValue) {
        $scope.examinationSettings.orl = !isEmpty(newValue) || $scope.newExamination;
      });
      $scope.$watch('model.visceral', function(newValue, oldValue) {
        $scope.examinationSettings.visceral = !isEmpty(newValue) || $scope.newExamination;
      });
      $scope.$watch('model.pulmo', function(newValue, oldValue) {
        $scope.examinationSettings.pulmo = !isEmpty(newValue) || $scope.newExamination;
      });
      $scope.$watch('model.uro_gyneco', function(newValue, oldValue) {
        $scope.examinationSettings.uro_gyneco = !isEmpty(newValue) || $scope.newExamination;
      });
      $scope.$watch('model.periphery', function(newValue, oldValue) {
        $scope.examinationSettings.periphery = !isEmpty(newValue) || $scope.newExamination;
      });
      $scope.$watch('model.general_state', function(newValue, oldValue) {
        $scope.examinationSettings.general_state = !isEmpty(newValue) || $scope.newExamination;
      });

      $scope.$watch('model.status', function(newValue, oldValue) {
        $scope.updateDeleteTrigger();
      });

      $scope.$watch('model.id', function(newValue, oldValue) {
        $scope.updateDeleteTrigger();
      });

      $scope.updateDeleteTrigger = function() {
        if ($scope.model == null) {
          $scope.triggerEditForm.delete = false;
          return;
        }
        if ($scope.model.status != 0) {
          $scope.triggerEditForm.delete = false;
        } else {
          if ($scope.model.id) {
            $scope.triggerEditForm.delete = true;
          } else {
            $scope.triggerEditForm.delete = false;
          }
        }
      };

      $scope.printInvoice = function(invoice) {
        var invoiceTab = $window.open('invoice/' + invoice.id, '_blank');

        setTimeout(function() {
          invoiceTab.print();
        }, 750);
      };

      $scope.cancelInvoice = function(invoice) {
        var modalInstance = $uibModal.open({
          templateUrl: 'web-view/partials/confirmation-modal',
          controller: ConfirmationCtrl,
          resolve: {
            message: function() {
              return "<p>" + gettext("Are you sure to cancel this invoice ?") + "</p>";
            },
            defaultIsOk: function() {
              return true;
            }
          }
        });
        modalInstance.result.then(function() {
          InvoiceService.cancel({
            invoiceId: invoice.id
          }, null, function(result) {
            $scope.model.last_invoice = null;
            $scope.model.invoice_number = null;
            $scope.model.invoices_list.unshift(result.canceled);
            $scope.model.invoices_list.unshift(result.credit_note);
          });
        });
      };

      $scope.invoiceExamination = function(examination) {
        $scope.close(examination);
      };


      $scope.finishPaiement = function(examination) {
        $scope.closeHandle()(examination, function(examination, invoicing) {
          ExaminationServ.update_paiement({
            examinationId: examination.id
          },invoicing , function(resultOk) {
            $scope.reloadExaminations()(examination);
          }, function(resultNok) {
            console.log(resultNok);
            growl.addErrorMessage("This operation is not available")
          });
        });
      };

      $scope.delete = function() {
        if ($scope.model.id) {
          ExaminationServ.delete({
            examinationId: $scope.model.id
          }, function(resultOk) {
            if ($scope.onDelete) {
              $scope.onDelete();
            }
          }, function(resultNok) {
            console.log(resultNok);
            growl.addErrorMessage("This operation is not available");
          });
        }

      };

      $scope.$watch('newExamination', function(newValue, oldValue) {
        if (newValue) {
          $scope.edit();
        }
      });
      $scope.$watch('editableForm.$visible', function(newValue, oldValue) {
        if (oldValue === false && newValue === true) {
          $scope.triggerEditForm.edit = false;
          $scope.triggerEditForm.save = true;
        } else if (oldValue === true && newValue === false) {
          $scope.triggerEditForm.edit = true;
          $scope.triggerEditForm.save = false;
        }
      });

      $scope.edit = function() {
        $scope.editableForm.$show();
      };

      $scope.save = function() {
        $scope.editableForm.$save();
      };

      $scope.saveAndClose = function() {
        $scope.close($scope.model);
      };

      $scope.triggerEditForm = {
        save: false,
        edit: true,
        cancel: null,
        delete: false,
      };
      $timeout(function() {
        //DOM has finished rendering
        if ($scope.newExamination) {
          $scope.editableForm.$show();
        }
      });
    }],
    templateUrl: 'web-view/partials/examination'
  }
}]);
