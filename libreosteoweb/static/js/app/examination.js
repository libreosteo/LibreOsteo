/**
    This file is part of LibreOsteo.

    LibreOsteo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    LibreOsteo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with LibreOsteo.  If not, see <http://www.gnu.org/licenses/>.
    */
var examination = angular.module('loExamination', ['ngResource', 'loInvoice']);


examination.factory('ExaminationServ', ['$resource',
  function($resource) {
    "use strict";
    var serv = $resource('api/examinations/:examinationId', null, {
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
    serv.SPHERES_LIST = [
      'orl', 'visceral', 'pulmo', 'uro_gyneco', 'periphery', 'generalState'
    ];
    return serv;
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


function isEmpty(str) {
  return (!str || 0 === str.length);
}

function loadExamination(data) {
  var examination = angular.copy(data);
  examination.date = new Date(data.date);
  return examination;
}


examination.directive('examination', ['ExaminationServ', 'PatientServ', 'TherapeutSettingsServ', 'OfficeSettingsServ', function(ExaminationServ, PatientServ, TherapeutSettingsServ, OfficeSettingsServ) {
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
      patient: '=?',
      externalPatientSave: '&',
      reloadExaminations: '&'
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

      TherapeutSettingsServ.get_by_user().$promise.then(function(therapeutSettings) {
        /* Display spheres if the examination has notes about spheres,
         *  even if spheres display is disabled in settings (to avoid
         *  hiding information).
         */
        var filled = ExaminationServ.SPHERES_LIST.map(function(sphere) {
          return !isEmpty($scope.model[sphere]);
        }).reduce(function(enabled, atLeastOne) {
          return atLeastOne || enabled;
        });

        if (therapeutSettings.spheres_enabled || filled) {
          // Initialize UI
          $scope.examinationSettings = initWithKeys(
            ExaminationServ.SPHERES_LIST,
            false
          );
          $scope.accordionOpenState = initWithKeys(
            ExaminationServ.SPHERES_LIST,
            true
          );

          angular.forEach(ExaminationServ.SPHERES_LIST, function(sphere, _) {
            $scope.$watch('model.' + sphere, function(newValue, oldValue) {
              $scope.examinationSettings[sphere] = !isEmpty(newValue) || $scope.newExamination;
            });
          });
        }
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
          OfficeSettingsServ.get(function(settings) {
            var officesettings = settings.find(x => x.selected);
            if (officesettings.cancel_invoice_credit_note) {
              // Credit note on canceling mode
              InvoiceService.cancel({
                invoiceId: invoice.id
              }, null, function(result) {
                $scope.model.last_invoice = null;
                $scope.model.invoice_number = null;
                $scope.model.invoices_list.unshift(result.canceled);
                $scope.model.invoices_list.unshift(result.credit_note);
              });
            } else {
              // Corrective invoice in this case
              $scope.closeHandle()($scope.model, function(examination, invoicing) {
                InvoiceService.cancel({invoiceId: invoice.id}, { examination: examination, corrective_invoice: invoicing },
                  function(result) {
                    $scope.model.last_invoice = result.corrective_invoice;
                    $scope.model.invoice_number = result.corrective_invoice.number;
                    $scope.model.invoices_list.unshift(result.canceled);
                    if (invoicing.paiment_mode == "notpaid"){
                      $scope.model.status = 1;
                    } else {
                      $scope.model.status = 2;
                    }
                  });
              }, true, true);
            }
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
          }, invoicing, function(resultOk) {
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

      // $visible means this form is in edit mode
      $scope.$watch('examinationForm.$visible', function(newValue, oldValue) {
        if (oldValue === false && newValue === true) {
          $scope.triggerEditForm.edit = false;
          $scope.triggerEditForm.save = true;
        } else if (oldValue === true && newValue === false) {
          $scope.triggerEditForm.edit = true;
          $scope.triggerEditForm.save = false;
        }
      });

      $scope.edit = function() {
        $scope.form.partialPatientForm.$show();
        $timeout(function() {
          $scope.examinationForm.$show();
        });
      };

      $scope.save = function() {
        $scope.examinationForm.$submit();
        $scope.form.partialPatientForm.$submit();
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
      $scope.$on('uiTabChange', function(event) {
        // Hackish : we have to wait that the tab has finished rendering
        // to trigger edit, otherwise, the form is considered inactive
        // by edit-form-manager, and « save » button is not shown.
        if ($scope.newExamination) {
          $scope.edit();
        }
      });
      // Patient
      $scope.lateralities = PatientServ.lateralities;

      // No need to handle buttons with partialPatientForm ; examinationForm
      // controls it.
      $scope.triggerEditFormPatient = initWithKeys(
        ['save', 'edit', 'cancel', 'delete'],
        false
      );

      // max date for examination
      $scope.maxExaminationDate = function() {
        if ($scope.model && $scope.model.last_invoice) {
          return moment($scope.model.last_invoice.date).toISOString();
        }
        return moment().endOf("day").toISOString();
      };

      $scope.maxExaminationDateAngular = function() {
        return moment($scope.maxExaminationDate()).toDate();
      }

      $scope.updateExaminationDateValidatorClass = function() {
        var original_input = jQuery('input[class~="examinationdate"][ng-model]');
        if (original_input.hasClass('ng-invalid-add')) {
          jQuery('input[class~="examinationdate"][class*="ws-"]').addClass('ng-invalid');
        } else {
          jQuery('input[class~="examinationdate"][class*="ws-"]').removeClass('ng-invalid');
        }
      };

      $scope.validateExaminationDate = function(data) {
        if (data === undefined || moment(data).isAfter(moment($scope.maxExaminationDate()))) {
          return "La date est invalide";
        } else {
          $scope.frozenExaminationDate = null;
        }
      };

      // Freeze the examination date from the model to be able to support an "undo" or "cancel"
      // edition on the date
      $scope.freezeExaminationDate = function() {
        if(!$scope.frozenExaminationDate) {
          $scope.frozenExaminationDate = moment($scope.model.date).format("DD/MM/YYYY");
        }
        return $scope.frozenExaminationDate;
      }
    }],

    templateUrl: 'web-view/partials/examination'
  };
}]);
