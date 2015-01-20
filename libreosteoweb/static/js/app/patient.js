var patient = angular.module('loPatient', ['ngResource', 'loDoctor', 'loExamination', 'ngSanitize']);


patient.factory('PatientServ', ['$resource', 'DoctorServ',
    function ($resource, DoctorServ) {
        "use strict";
        var serv = $resource('api/patients/:patientId', null, {
            query: {method: 'GET' },
            get : {method: 'GET', params: {patientId: 'patient'}},
            save : {method : 'PUT'},
            add : {method : 'POST'}
        });

        serv.prototype.doctor_detail = function (callback) {
            if (this.doctor)
            {
                return DoctorServ.get({doctorId : this.doctor}, callback);
            }
            return;
        };
        return serv;
    }
]);

patient.factory('PatientExaminationsServ', ['$resource',
    function($resource) {
        "use strict";
        return $resource('api/patients/:patient/examinations', null,
            {
                get: {
                    method: 'GET',
                    params: { patient: 'patient'},
                    isArray: true,
                }
            });

}]);

patient.filter('format_age', function () {
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
            if(ans)
            {
                out += ' ';
            }
            out += mois || '';
            if(mois)
            {
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

patient.controller('PatientCtrl', ['$scope', '$state', '$stateParams', '$filter', '$modal', '$http', 'growl', 'PatientServ', 'DoctorServ',
    'PatientExaminationsServ', 'ExaminationServ',
    function($scope, $state, $stateParams, $filter, $modal, $http, growl, PatientServ, DoctorServ, PatientExaminationsServ, ExaminationServ) {
        "use strict";
        $scope.patient = PatientServ.get({patientId : $stateParams.patientId}, function (p) {
            p.doctor_detail(function (detail) {$scope.doctor = detail; });
        });

        // Display the formated age
        $scope.get_age = function () {
            var birthDate = $scope.patient.birth_date;
            if(birthDate) {
                var todate = new Date();
                var fromDate = new Date(birthDate);
                var y = [todate.getFullYear(), fromDate.getFullYear()];
                var m = [todate.getMonth(), fromDate.getMonth()];
                var d = [todate.getDate(), fromDate.getDate()];

                var ydiff = y[0] - y[1];
                var mdiff = m[0] - m[1];
                var ddiff = d[0] - d[1];

                if ((mdiff <= 0) && (ddiff < 0)) {
                    ydiff = ydiff -1;
                    mdiff = mdiff + 12;
                }
                if (ddiff <= 0) {
                    var n_day_by_month = [31,28,31,30,31, 30, 31, 31, 30, 31,30, 31];
                    mdiff = mdiff -1;
                    var d_month ;
                    if ((m[0] == 1) && (y[0]%4 == 0)) {
                         d_month = n_day_by_month[m[0]] + 1;
                    } else {
                        d_month = n_day_by_month[m[0]];
                    }
                    ddiff = ddiff + d_month;
                }
                return {year : ydiff, month : mdiff, day : ddiff};
            }
            return {};
        };
        $scope.age = $scope.get_age();

        $scope.$watch('patient.birth_date', function (newValue, oldValue) {
         $scope.age = $scope.get_age();
     });

        $scope.updateComponentPolyfill = function() {
            // To be compliant with all browser.
            var els = angular.element(".polyfill-updatable");
            for (var i = 0; i < els.length; ++i)
            {
                $(els[i]).updatePolyfill();
            }
        }

        // Handle the doctor of the patient.
        $scope.$watch('patient.doctor', function(newValue, oldValue){
            if (newValue){
                $scope.doctor = DoctorServ.get({doctorId : newValue});
            }
        });

        // Handle the patient object to be saved.
        $scope.savePatient = function () {
            // Be sure that the birth_date has a correct format to be registered.
            $scope.patient.birth_date = $filter('date')($scope.patient.birth_date, 'yyyy-MM-dd');
            return PatientServ.save({patientId:$scope.patient.id}, $scope.patient, null, function(data)
            {
                // Should display the error
                if(data.data.detail) {
                    growl.addErrorMessage(data.data.detail);
                } else {
                    growl.addErrorMessage(formatGrowlError(data.data), {enableHtml:true});
                }
                $scope.patient = PatientServ.get({patientId : $stateParams.patientId}, function (p) {
                     p.doctor_detail(function (detail) {$scope.doctor = detail; });
                });
            });
        };

        // Prepare the doctors function to be selected.
        $scope.doctors = null;
        $scope.loadDoctors = function() {
            $scope.doctors = DoctorServ.query();
        };

        // Prepare and define the modal function to add doctor.
       $scope.formAddDoctor = function() {
            var modalInstance = $modal.open({
                templateUrl: 'web-view/partials/doctor-modal',
                controller : DoctorAddFormCtrl
            });
           modalInstance.result.then(function (newDoctor){
              DoctorServ.add(newDoctor);
           });
        };

        //Handle examinations

        $scope.getOrderedExaminations = function(patientId)
        {
            var examinationsList = PatientExaminationsServ.get( { patient : patientId }, function(data)
                {
                    examinationsList = data;
                    angular.forEach(examinationsList, function(value, index, obj)
                    {
                        value.order = examinationsList.length - index;
                    });
                }
                );
            return examinationsList;

        };

       $scope.examinations = $scope.getOrderedExaminations($stateParams.patientId);
        // The futur examination of the patient, if a new examination is started.
        $scope.newExamination = {};
        // To display examination in the patient file.
       // $scope.archiveExamination = null;

        $scope.newExaminationDisplay = false;
        $scope.newExaminationActive = false;
        $scope.examinationsListActive = false;
        $scope.startExamination = function() {
            $scope.newExaminationDisplay = true;
            $scope.newExaminationActive = true;
            $scope.examinationsListActive = false;

            $scope.newExamination = {
                reason : '',
                reason_description : '',
                medical_examination : '',
                orl : '',
                visceral : '',
                pulmo : '',
                uro_gyneco : '',
                periphery : '',
                general_state : '',
                tests : '',
                diagnosis : '',
                treatments : '',
                conclusion : '',
                status : 0,
                type : 1,
                date : new Date(),
                patient : $scope.patient.id,
                therapeut : '',
            };
        };

        $scope.previousExamination = {
            data : null,
        };

        // Handle the examination object to be saved.
        $scope.saveExamination = function (examinationToSave) {
            //$scope.examination.date = $filter('date')($scope.examination.date, 'yyyy-MM-dd');
            var localExamination;
            if( !examinationToSave.id ) {
                localExamination = ExaminationServ.add(examinationToSave, function()
                {
                   $scope.newExamination = localExamination;
                });
            } else {
                localExamination = ExaminationServ.save({examinationId: examinationToSave.id}, examinationToSave);
            }
            $scope.examinations = $scope.getOrderedExaminations($stateParams.patientId);
            return localExamination;
        };

        // Function which manage the current examination
        $scope.currentExaminationManager = function() {
            $scope.newExaminationDisplay = true;
            $scope.newExaminationActive = true;
        };

        // Handle the invoice function
        $scope.close = function(examination)
        {
            ExaminationServ.close({examinationId : examination.id} , function() {
                if ($scope.newExaminationDisplay){
                    // Hide the in progress examination
                    $scope.newExamination = {};
                    $scope.newExaminationDisplay = false;
                    $scope.newExaminationActive = false;
                    $scope.examinationsListActive = true;
                } else {
                    // Close the view of the examination
                    $scope.previousExamination.data = null;
                }
                // Reload the examinations list
                $scope.examinations = $scope.getOrderedExaminations($stateParams.patientId);
            });
        };


        // Restore the state
        if ($state.includes('patient.examinations')){
            $scope.examinationsListActive = true;
        } else if ($state.includes('patient.examination')){
            $scope.examinationsListActive = true;

            $scope.previousExamination.data = ExaminationServ.get({examinationId : $state.params.examinationId},
                function(data){
                  $scope.previousExamination.data = data;
              });
        }

}]);


var DoctorAddFormCtrl = function($scope, $modalInstance) {
    "use strict";
    $scope.doctor = {
        family_name : null,
        first_name : null,
        phone : null,
        city : null

    };
    $scope.ok = function () {
      $modalInstance.close($scope.doctor);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
};


patient.controller('AddPatientCtrl', ['$scope', '$location', 'growl', '$sce', 'PatientServ', 'DoctorServ',
    function($scope, $location, growl, $sce, PatientServ, DoctorServ ) {
        "use strict";

        $scope.initPatient = function(patient) {
            PatientServ.add(patient, function(data)
            {
                $location.path('/patient/'+data.id);
            },
            function(data)
            {
                // Should display the error
                if(data.data.detail) {
                    growl.addErrorMessage(data.data.detail);
                } else {
                    growl.addErrorMessage(formatGrowlError(data.data), {enableHtml:true});
                }
            });
        };
    }]);


patient.controller('DisplayArchiveExaminationCtrl', ['$scope',
    function($scope) {
        "use strict";
        $scope.previousExamination = {
            data : null,
        };
    }
]);
