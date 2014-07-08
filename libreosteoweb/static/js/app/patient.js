var patient = angular.module('loPatient', ['ngResource', 'loDoctor']);


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

patient.controller('PatientCtrl', ['$scope', '$routeParams', '$filter', '$modal', 'PatientServ', 'DoctorServ',
    function($scope, $routeParams, $filter, $modal, PatientServ, DoctorServ ) {
        "use strict";
        $scope.patient = PatientServ.get({patientId : $routeParams.patientId}, function (p) {
            p.doctor_detail(function (detail) {$scope.doctor = detail; });
        });

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

        $scope.$watch('patient.doctor', function(newValue, oldValue){
            if (newValue){
                $scope.doctor = DoctorServ.get({doctorId : newValue});
            }
        });

        $scope.savePatient = function () {
            $scope.patient.birth_date = $filter('date')($scope.patient.birth_date, 'yyyy-MM-dd');
            return PatientServ.save({patientId:$scope.patient.id}, $scope.patient);
        };

        $scope.doctors = null;
        $scope.loadDoctors = function() {
            $scope.doctors = DoctorServ.query();
        };

       $scope.formAddDoctor = function() {
            var modalInstance = $modal.open({
                templateUrl: 'web-view/partials/doctor-modal',
                controller : DoctorAddFormCtrl
            });
           modalInstance.result.then(function (newDoctor){
              DoctorServ.add(newDoctor);
           });
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