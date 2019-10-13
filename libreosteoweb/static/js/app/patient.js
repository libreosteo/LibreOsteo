
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
var patient = angular.module('loPatient', ['ngResource', 'loDoctor', 'loExamination', 'ngSanitize', 'loOfficeSettings', 'loFileManager', 'loUtils', 'angular-bind-html-compile']);


patient.factory('PatientServ', ['$resource', 'DoctorServ', 'PatientDocumentServ',
  function($resource, DoctorServ, PatientDocumentServ) {
    "use strict";
    var serv = $resource('api/patients/:patientId', null, {
      query: {
        method: 'GET'
      },
      get: {
        method: 'GET',
        params: {
          patientId: 'patient'
        }
      },
      save: {
        method: 'PUT',
        params: {
          patientId: 'patientId'
        }
      },
      add: {
        method: 'POST'
      },
      delete: {
        method: 'DELETE',
        params: {
          patientId: 'patientId'
        }
      },
      delete_gdpr: {
        method: 'DELETE',
        url: 'api/patients/:patientId?gdpr=True',
        params: {
          patientId: 'patientId'
        }
      }
    });

    serv.prototype.doctor_detail = function(callback) {
      if (this.doctor) {
        return DoctorServ.get({
          doctorId: this.doctor
        }, callback);
      }
      return;
    };

    serv.prototype.medical_reports_doc = function(callback) {
      return PatientDocumentServ.get({
        patient: this.id
      }, callback);
    }
    return serv;
  }
]);

patient.factory('PatientExaminationsServ', ['$resource',
  function($resource) {
    "use strict";
    return $resource('api/patients/:patient/examinations', null, {
      get: {
        method: 'GET',
        params: {
          patient: 'patient'
        },
        isArray: true,
      },
    });

  }
]);

patient.factory('PatientDocumentServ', ['$resource',
  function($resource) {
    "use strict";
    return $resource('api/patients/:patient/documents', null, {
      get: {
        method: 'GET',
        params: {
          patient: 'patient'
        },
        isArray: true,
      }
    });
  }
]);

patient.filter('format_age', function() {
  "use strict";
  return function(input) {
    if (input) {
      var out = '';
      var ans = '';
      var mois = '';
      var jour = '';
      if (input.year) {
        ans = input.year + " ans";
      }
      if (input.month) {
        mois = input.month + " mois";
      }
      if (input.day) {
        jour = input.day + " jours";
      }
      out = ans || '';
      if (ans) {
        out += ' ';
      }
      out += mois || '';
      if (mois) {
        out += ' ';
      }
      if (ans == '') {
        out += ' ' + jour || '';
      }
      return out;
    } else {
      return '';
    }
  };
});

patient.controller('PatientCtrl', ['$scope', '$state', '$stateParams', '$filter', '$uibModal', '$http', '$sce', 'growl', 'PatientServ', 'DoctorServ', '$timeout',
  'PatientExaminationsServ', 'ExaminationServ', 'OfficeSettingsServ', 'loEditFormManager', 'loFileManager', 'FileServ', 'OfficePaimentMeansServ',
  function($scope, $state, $stateParams, $filter, $uibModal, $http, $sce, growl, PatientServ, DoctorServ, $timeout, PatientExaminationsServ, ExaminationServ, OfficeSettingsServ,
    loEditFormManager, loFileManager, FileServ, OfficePaimentMeansServ) {
    "use strict";

    var updateMedicalDocumentReports = function(docs) {
      var medicalReportsDoc = [];
      angular.forEach(docs, function(value, key) {
        if (value.attachment_type == 5) { // Medical reports
          this.push(value.document);
          value.document.expand = false;
          value.document.edit = false;
          if (value.document.title == 'null')
            value.document.title = null;
          if (value.document.notes == 'null')
            value.document.notes = null;
          var d = value.document.document_date;
          if (d)
            value.document.document_date = convertUTCDateToLocalDate(new Date(d));
        }
      }, medicalReportsDoc);
      $scope.patient.medicalReportsDoc = medicalReportsDoc;
    };

    $scope.patient = PatientServ.get({
      patientId: $stateParams.patientId
    }, function(p) {
      p.doctor_detail(function(detail) {
        $scope.doctor = detail;
      });
      p.birth_date = convertUTCDateToLocalDate(new Date(p.birth_date));
      p.medical_reports_doc(updateMedicalDocumentReports);
    });

    $scope.form = {};

    // Display the formated age
    $scope.get_age = function() {
      var birthDate = $scope.patient.birth_date;
      if (birthDate) {
        var todate = new Date();
        var fromDate = new Date(birthDate);
        var y = [todate.getFullYear(), fromDate.getFullYear()];
        var m = [todate.getMonth(), fromDate.getMonth()];
        var d = [todate.getDate(), fromDate.getDate()];

        var ydiff = y[0] - y[1];
        var mdiff = m[0] - m[1];
        var ddiff = d[0] - d[1];

        if (mdiff < 0) {
          ydiff = ydiff - 1;
          mdiff = mdiff + 12;
        }

        if (mdiff == 0 && ddiff < 0) {
          ydiff = ydiff - 1;
          mdiff = mdiff + 12;
        } else if (ddiff < 0) {
          var n_day_by_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
          mdiff = mdiff - 1;
          var d_month;
          if ((m[0] == 1) && (y[0] % 4 == 0)) {
            d_month = n_day_by_month[m[0]] + 1;
          } else {
            d_month = n_day_by_month[m[0]];
          }
          ddiff = ddiff + d_month;
        }
        return {
          year: ydiff,
          month: mdiff,
          day: ddiff
        };
      }
      return {};
    };
    $scope.age = $scope.get_age();

    $scope.$watch('patient.birth_date', function(newValue, oldValue) {
      $scope.age = $scope.get_age();
    });

    $scope.updateComponentPolyfill = function() {
      // To be compliant with all browser.
      var els = angular.element(".polyfill-updatable");
      angular.forEach(els, function(el) {
        var jqEl = $(el);
        if (jqEl.is(':visible')) {
          jqEl.updatePolyfill();
        }
      });
    }

    // Handle the doctor of the patient.
    $scope.$watch('patient.doctor', function(newValue, oldValue) {
      if (newValue) {
        $scope.doctor = DoctorServ.get({
          doctorId: newValue
        });
      }
    });

    // Handle the patient object to be saved.
    $scope.savePatient = function() {
      // Be sure that the birth_date has a correct format to be registered.
      var model = angular.copy($scope.patient);
      model.birth_date = $filter('date')($scope.patient.birth_date, 'yyyy-MM-dd');
      return PatientServ.save({
        patientId: $scope.patient.id
      }, model, function(data) {
        // Should reload the patient
        $scope.patient = data;
        $scope.patient.birth_date = convertUTCDateToLocalDate(new Date(data.birth_date));
        $scope.patient.doctor_detail(function(detail) {
          $scope.doctor = detail;
        });
        $scope.patient.medical_reports_doc(updateMedicalDocumentReports);
      }, function(data) {
        // Should display the error
        if (data.data.detail) {
          growl.addErrorMessage(data.data.detail);
        } else {
          growl.addErrorMessage(formatGrowlError(data.data), {
            enableHtml: true
          });
        }
        $scope.patient = PatientServ.get({
          patientId: $stateParams.patientId
        }, function(p) {
          p.doctor_detail(function(detail) {
            $scope.doctor = detail;
          });
          $scope.patient.birth_date = convertUTCDateToLocalDate(new Date(p.birth_date));
          $scope.patient.medical_reports_doc(updateMedicalDocumentReports);
        });
      });
    };

    // Prepare the doctors function to be selected.
    $scope.doctors = null;
    $scope.loadDoctors = function() {
      return DoctorServ.query(function(result) {
        $scope.doctors = result;
      });
    };

    // Prepare and define the modal function to add doctor.
    $scope.formAddDoctor = function() {
      var modalInstance = $uibModal.open({
        templateUrl: 'web-view/partials/doctor-modal',
        controller: DoctorAddFormCtrl
      });
      modalInstance.result.then(function(newDoctor) {
        DoctorServ.add(newDoctor);
      });
    };

    //Handle examinations

    $scope.getOrderedExaminations = function(patientId) {
      var examinationsList = PatientExaminationsServ.get({
        patient: patientId
      }, function(data) {
        examinationsList = data;
        angular.forEach(examinationsList, function(value, index, obj) {
          value.order = examinationsList.length - index;
        });
      });
      return examinationsList;

    };

    $scope.examinations = $scope.getOrderedExaminations($stateParams.patientId);
    // The futur examination of the patient, if a new examination is started.
    $scope.newExamination = {};
    // To display examination in the patient file.
    // $scope.archiveExamination = null;

    $scope.examinationsTab = {
      //Is the tab for new examination is displayed ?
      newExaminationDisplayTab: false,
    };

    $scope.$watch('patient.id', function(newValue, oldValue) {
      $scope.updateDeleteTrigger();
      loEditFormManager.available = true;
    });

    $scope.updateDeleteTrigger = function() {
      if ($scope.patient == null) {
        $scope.triggerEditFormPatient.delete = false;
        return;
      }

      if ($scope.patient.id != null) {
        $scope.triggerEditFormPatient.delete = true;
      } else {
        $scope.triggerEditFormPatient.delete = false;
      }
    };

    $scope.startExamination = function() {
      $scope.currentExaminationManager();

      $scope.newExamination = {
        reason: '',
        reason_description: '',
        medical_examination: '',
        orl: '',
        visceral: '',
        pulmo: '',
        uro_gyneco: '',
        periphery: '',
        general_state: '',
        tests: '',
        diagnosis: '',
        treatments: '',
        conclusion: '',
        status: 0,
        type: 1,
        date: new Date(),
        patient: $scope.patient.id,
        therapeut: '',
      };
    };

    $scope.previousExamination = {
      data: null,
    };

    // Handle the examination object to be saved.
    $scope.saveExamination = function(examinationToSave) {
      //$scope.examination.date = $filter('date')($scope.examination.date, 'yyyy-MM-dd');
      if (!examinationToSave) {
        examinationToSave = $scope.newExamination;
      }
      var localExamination;
      if (!examinationToSave.id) {
        localExamination = ExaminationServ.add(examinationToSave, function(value) {
          Object.keys(value).forEach(function(key) {
            $scope.newExamination[key] = value[key];
          });
          $scope.examinations = $scope.getOrderedExaminations($stateParams.patientId);
        });
      } else {
        localExamination = ExaminationServ.save({
          examinationId: examinationToSave.id
        }, examinationToSave, function(value) {
          $scope.examinations = $scope.getOrderedExaminations($stateParams.patientId);
        });
      }
      $scope.updateDeleteTrigger();
      return localExamination;
    };

    // Function which manage the current examination
    $scope.currentExaminationManager = function() {
      $scope.examinationsTab.newExaminationDisplay = true;
      $scope.indexTab = 6;
    };

    // Handle the invoice function

    $scope.invoiceExamination = function(examination, handleClose) {
      var modalInstance = $uibModal.open({
        templateUrl: 'web-view/partials/invoice-modal',
        controller: InvoiceFormCtrl,
        resolve: {
          examination: function() {
            return examination;
          }
        }
      });

      modalInstance.result.then(function(invoicing) {
        handleClose(examination, invoicing);
      });
    };

    $scope.reloadExaminations = function(examination) {
      // Reload the examinations list
      $scope.examinations = $scope.getOrderedExaminations($stateParams.patientId);
      $scope.previousExamination.data = ExaminationServ.get({
          examinationId: examination.id
        },
        function(data) {
          $scope.previousExamination.data = data;
        });
    };

    $scope.close = function(examination, invoicing) {

      ExaminationServ.close({
        examinationId: examination.id
      }, invoicing, function() {
        if ($scope.examinationsTab.newExaminationDisplay) {
          // Hide the in progress examination
          $scope.newExamination = {};
          $scope.examinationsTab.newExaminationDisplay = false;
          $scope.indexTab = 5;
        }
        $scope.reloadExaminations(examination);
      }, function(reason) {
        if (reason.data.detail) {
          growl.addErrorMessage(reason.data.detail);
        } else {
          growl.addErrorMessage(formatGrowlError(reason.data), {
            enableHtml: true
          });
        }
      });
    };

    $scope.examinationDeleted = function(examination) {
      if (examination.id) {
        growl.addSuccessMessage(gettext("Examination deleted"));
        $scope.examinations = $scope.examinations.filter(function(el) {
          return el.id !== examination.id;
        });

      }
      if ($scope.examinationsTab.newExaminationDisplay) {
        // Hide the in progress examination
        Object.keys($scope.newExamination).forEach(function(key) {
          delete $scope.newExamination[key];
        });
        $scope.examinationsTab.newExaminationDisplay = false;
        $scope.indexTab = 5;
      }
      if ($scope.examinationsTab.examinationsListActive) {
        $scope.previousExamination.data = null;
        $state.go('patient.examinations');
      }
      $scope.updateDeleteTrigger();
    }

    // Restore the state
    if ($state.includes('patient.examinations')) {
      $scope.indexTab = 5;
    } else if ($state.includes('patient.examination')) {
      $scope.indexTab = 5;

      $scope.previousExamination.data = ExaminationServ.get({
          examinationId: $state.params.examinationId
        },
        function(data) {
          $scope.previousExamination.data = data;
          loEditFormManager.available = true;
        },
        function(error) {
          $scope.previousExamination.data = null;
          $state.go('patient.examinations');
        });
    } else {
      loEditFormManager.available = true;
    }

    // Load the values for the sex
    $scope.sexes = [{
        value: 'M',
        text: gettext('Male')
      },
      {
        value: 'F',
        text: gettext('Female')
      },
    ];

    // display the translated value for the sex
    $scope.showSex = function() {
      if ($scope.patient) {
        var selected = $filter('filter')($scope.sexes, {
          value: $scope.patient.sex
        });
        return ($scope.patient && $scope.patient.sex && selected.length) ? selected[0].text : gettext('not documented');
      } else {
        return gettext('not documented');
      }
    };

    // Load the values for the sex
    $scope.laterality = [{
        value: 'L',
        text: gettext('Left-handed')
      },
      {
        value: 'R',
        text: gettext('Right-handed')
      },
    ];

    // display the translated value for the sex
    $scope.showLaterality = function() {
      if ($scope.patient) {
        var selected = $filter('filter')($scope.laterality, {
          value: $scope.patient.laterality
        });
        return ($scope.patient && $scope.patient.laterality && selected.length) ? selected[0].text : '';
      } else {
        return gettext('not documented');
      }
    };

    $scope.triggerEditFormPatient = {
      save: false,
      edit: true,
      cancel: null,
      delete: true,
    };

    $scope.$watch('form.patientForm.$visible', function(newValue, oldValue) {
      if (newValue === true) {
        $scope.triggerEditFormPatient.edit = false;
        $scope.triggerEditFormPatient.save = true;
        loEditFormManager.available = true;
        $scope.originalNameInput.$show();
      } else if (newValue === false) {
        $scope.triggerEditFormPatient.edit = true;
        $scope.triggerEditFormPatient.save = false;
      }
    });

    $scope.editPatient = function() {

      $scope.form.patientForm.$show();
    };

    $scope.saveEditPatient = function() {
      $scope.form.patientForm.$save();
    };

    $scope.delete = function() {
      var deleteFunction = function(isGdpr) {
        var delete_impl = PatientServ.delete;
        if (isGdpr) {
          delete_impl = PatientServ.delete_gdpr;
        }
        delete_impl({
          patientId: $scope.patient.id
        }, function(resultOk) {
          $state.go('dashboard');
        }, function(resultNok) {
          console.log(resultNok);
          growl.addErrorMessage("This operation is not available");
        });
      };

      if ($scope.patient.id) {
        var examinationsList = PatientExaminationsServ.get({
          patient: $scope.patient.id
        }, function(data) {
          if (data.length != 0) {
            var modalInstance = $uibModal.open({
              templateUrl: 'web-view/partials/confirmation-modal',
              controller: ConfirmationCtrl,
              resolve: {
                message: function() {
                  return $sce.trustAsHtml("<p>" +
                    gettext("For GDPR conformity, patient can ask to delete all information. This function delete all information without trace except invoices. You can find invoices into Accounting function. Are you agree with that ?") +
                    "</p>" +
                    "<div><input type=\"checkbox\" id=\"agreeGdpr\" name=\"agreeGdpr\" ng-model=\"isOk\"><label for=\"agreeGdpr\">" +
                    gettext("I understand that it means") +
                    "</label></div>");
                },
                defaultIsOk: function() {
                  return false;
                }
              }
            });
            modalInstance.result.then(function() {
              deleteFunction(true);
            });
          } else {
            deleteFunction();
          }
        });
      }
    }

    $scope.triggerEditFormHistory = {
      save: false,
      edit: true,
      cancel: null,
      delete: false,
    };

    $scope.$watch('form.historyForm.$visible', function(newValue, oldValue) {
      if (oldValue === false && newValue === true) {
        $scope.triggerEditFormHistory.edit = false;
        $scope.triggerEditFormHistory.save = true;
      } else if (oldValue === true && newValue === false) {
        $scope.triggerEditFormHistory.edit = true;
        $scope.triggerEditFormHistory.save = false;
      }
    });

    $scope.editHistory = function() {

      $scope.form.historyForm.$show();
    };

    $scope.saveHistory = function() {
      $scope.form.historyForm.$save();
    };

    $scope.triggerEditFormMedical = {
      save: false,
      edit: true,
      cancel: null,
      delete: false,
    };

    $scope.$watch('form.medicalForm.$visible', function(newValue, oldValue) {
      if (oldValue === false && newValue === true) {
        $scope.triggerEditFormMedical.edit = false;
        $scope.triggerEditFormMedical.save = true;
      } else if (oldValue === true && newValue === false) {
        $scope.triggerEditFormMedical.edit = true;
        $scope.triggerEditFormMedical.save = false;
      }
    });

    $scope.editMedical = function() {

      $scope.form.medicalForm.$show();
    };

    $scope.saveMedical = function() {
      $scope.form.medicalForm.$save();
    };

    $scope.fillInfoFiles = function(files) {
      if (files && files.length) {
        $scope.fileContext.files(files);
        $scope.fileContext.patient($scope.patient);
      }
    };

    $scope.fileContext = loFileManager.createFileContext();

    $scope.fileContext.setDocumentAddedCb(function() {
      console.log("Call callback");
      $scope.patient.medical_reports_doc(updateMedicalDocumentReports);
    });

    $scope.expand = function(document_view, flag) {
      document_view.expand = flag;
    };

    $scope.edit_doc = function(document_view, flag) {
      document_view.edit = flag;
      document_view.expand = false;
      if (!flag)
        $scope.patient.medical_reports_doc(updateMedicalDocumentReports);
    };

    $scope.save_doc = function(document_view) {
      document_view.edit = false;
      var date_tostr = $filter('date')(document_view.document_date, 'yyyy-MM-dd');
      var document_tosave = {
        'id': document_view.id,
        'title': document_view.title,
        'notes': document_view.notes,
        'document_date': date_tostr,
      };
      FileServ.save({
        patientDocId: document_view.id
      }, document_tosave, function(value) {
        growl.addSuccessMessage(gettext("Update success"));
      });
    };

    $scope.delete_doc = function(document_view) {
      var modalInstance = $uibModal.open({
        templateUrl: 'web-view/partials/confirmation-modal',
        controller: ConfirmationCtrl,
        resolve: {
          message: function() {
            return "<p>" + gettext("Are you sure to delete this document ?") + "</p>";
          },
          defaultIsOk: function() {
            return true;
          }
        }
      });
      modalInstance.result.then(function() {
        FileServ.delete({
          patientDocId: document_view.id
        }, function(value) {
          $scope.patient.medicalReportsDoc = $scope.patient.medicalReportsDoc.filter(function(el) {
            return el.id !== document_view.id;
          });
        });
      });
    };
  }
]);


var DoctorAddFormCtrl = function($scope, $uibModalInstance) {
  "use strict";
  $scope.doctor = {
    family_name: null,
    first_name: null,
    phone: null,
    city: null

  };
  $scope.ok = function() {
    $uibModalInstance.close($scope.doctor);
  };

  $scope.cancel = function() {
    $uibModalInstance.dismiss('cancel');
  };
};

var ConfirmationCtrl = function($scope, $uibModalInstance, message, defaultIsOk) {
  $scope.message = message;
  $scope.ok = function() {
    $uibModalInstance.close();
  };

  $scope.isOk = defaultIsOk;

  $scope.cancel = function() {
    $uibModalInstance.dismiss('cancel');
  };
}

var InvoiceFormCtrl = function($scope, $uibModalInstance, OfficeSettingsServ, OfficePaimentMeansServ, examination) {
  "use strict";
  $scope.invoicing = {
    status: null,
    reason: null,
    amount: null,
    paiment_mode: null,
    check: {
      bank: null,
      payer: null,
      number: null,
    },
  };
  $scope.examinationToInvoice = examination;

  if ($scope.examinationToInvoice != null && $scope.examinationToInvoice.last_invoice != null) {
    $scope.invoicing.status = 'invoiced';
    $scope.invoicing.amount = $scope.examinationToInvoice.last_invoice.amount;
  } else {
    OfficeSettingsServ.get(function(settings) {
      $scope.officesettings = settings[0];
      $scope.invoicing.amount = $scope.officesettings.amount;
    });
  }

  OfficePaimentMeansServ.query(function(paimentmeans) {
    var enabledPm = [];
    angular.forEach(paimentmeans, function(value, key) {
      if (value.enable) {
        enabledPm.push(value);
      }
    }, enabledPm);
    $scope.paimentmeans = enabledPm;
  });

  $scope.ok = function() {
    $uibModalInstance.close($scope.invoicing);
  };

  $scope.cancel = function() {
    $uibModalInstance.dismiss('cancel');
  };

  $scope.validateStatus = function(value) {
    return value != null;
  }

  $scope.validateReason = function(value) {
    if ($scope.invoicing.status == 'notinvoiced') {
      return value != null && value.length != 0;
    }
    return true;
  };

  $scope.validateAmount = function(value) {
    if ($scope.invoicing.status == 'invoiced') {
      return value != null && value > 0;
    }
    return true;
  };

  $scope.validatePaimentMode = function(value) {
    return value != null;
  }

  $scope.validateBank = function(value) {
    /*if($scope.invoicing.status == 'invoiced' && $scope.invoicing.paiment_mode == 'check')
    {
        return value != null && value.length != 0;
    }*/
    return true;
  };

  $scope.validatePayer = function(value) {
    /*if($scope.invoicing.status == 'invoiced' && $scope.invoicing.paiment_mode == 'check')
    {
        return value != null && value.length != 0;
    }*/
    return true;
  };

  $scope.validateNumber = function(value) {
    /*if($scope.invoicing.status == 'invoiced' && $scope.invoicing.paiment_mode == 'check')
    {
        return value != null && value.length != 0;
    }*/
    return true;
  };
};


patient.controller('AddPatientCtrl', ['$scope', '$location', 'growl', '$sce', 'PatientServ', 'DoctorServ', '$filter',
  function($scope, $location, growl, $sce, PatientServ, DoctorServ, $filter) {
    "use strict";

    $scope.initPatient = function(patient) {
      var model = angular.copy(patient);
      model.birth_date = $filter('date')(patient.birth_date, 'yyyy-MM-dd');

      PatientServ.add(model, function(data) {
          $location.path('/patient/' + data.id);
        },
        function(data) {
          // Should display the error
          if (data.data.birth_date && data.data.birth_date.birth_date) {
            growl.addErrorMessage(data.data.birth_date.birth_date);
          } else if (data.data.non_field_errors) {
            growl.addErrorMessage(data.data.non_field_errors);
          } else {
            growl.addErrorMessage(formatGrowlError(data.data), {
              enableHtml: true
            });
          }
        });
    };
  }
]);


patient.controller('DisplayArchiveExaminationCtrl', ['$scope',
  function($scope) {
    "use strict";
    $scope.previousExamination = {
      data: null,
    };
  }
]);
