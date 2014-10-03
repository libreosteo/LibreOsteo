var patient = angular.module('loPatient', ['ngResource', 'loDoctor', 'loExamination']);


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

patient.controller('PatientCtrl', ['$scope', '$routeParams', '$filter', '$modal', '$http', 'PatientServ', 'DoctorServ',
    'PatientExaminationsServ', 'ExaminationServ',
    function($scope, $routeParams, $filter, $modal, $http, PatientServ, DoctorServ, PatientExaminationsServ, ExaminationServ) {
        "use strict";
        $scope.patient = PatientServ.get({patientId : $routeParams.patientId}, function (p) {
            p.doctor_detail(function (detail) {$scope.doctor = detail; });
        });

        // Display the formated age
        $scope.get_age = function () {
            var birthDate = $scope.patient.birth_date;
            if(birthDate)
            {
               var todate= new Date();
               var fromdate= new Date(birthDate),
                y= [todate.getFullYear(), fromdate.getFullYear()],
                ydiff= y[0]-y[1],
                m= [todate.getMonth(), fromdate.getMonth()],
                mdiff= m[0]-m[1],
                d= [todate.getDate(), fromdate.getDate()],
                ddiff= d[0]-d[1];

                if(mdiff < 0 || (mdiff=== 0 && ddiff<0))--ydiff;
                if(mdiff<0) mdiff+= 12;
                if(ddiff<0){
                fromdate.setMonth(m[1]+1, 0);
                ddiff= fromdate.getDate()-d[1]+d[0];
                --mdiff;
                }
                return { year : ydiff, month : mdiff, day: ddiff};
            }
            return { };
        };
        $scope.age = $scope.get_age();

        $scope.$watch('patient.birth_date', function (newValue, oldValue) {
           $scope.age = $scope.get_age();
        });

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
            return PatientServ.save({patientId:$scope.patient.id}, $scope.patient);
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

       $scope.examinations = $scope.getOrderedExaminations($routeParams.patientId);
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
        $scope.saveExamination = function () {
            //$scope.examination.date = $filter('date')($scope.examination.date, 'yyyy-MM-dd');
            var localExamination;
            if( !$scope.newExamination.id ) {
                localExamination = ExaminationServ.add($scope.newExamination, function()
                {
                   $scope.examinations = $scope.getOrderedExaminations($routeParams.patientId);
                });
            } else {
                localExamination = ExaminationServ.save({examinationId: $scope.newExamination.id}, $scope.newExamination);
            }
            $scope.newExamination = localExamination;
            return localExamination;
        };

        // Handle the invoice function
        $scope.invoice = function(examination)
        {
            // Hide the new examination function
            $scope.newExamination = {};
            $scope.newExaminationDisplay = false;
            $scope.newExaminationActive = false;
            $scope.examinationsListActive = true;
        };


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


patient.controller('AddPatientCtrl', ['$scope', '$location', 'growl', 'PatientServ', 'DoctorServ',
    function($scope, $location, growl, PatientServ, DoctorServ ) {
        "use strict";

        $scope.initPatient = function(patient) {
            PatientServ.add(patient, function(data)
            {
                $location.path('/patient/'+data.id);
            },
            function(data)
            {
                // Should display the error
                console.log(angular.toJson(data));
                growl.addErrorMessage(data.data.detail);
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