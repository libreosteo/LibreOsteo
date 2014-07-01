var patient = angular.module('loPatient', ['ngResource']);


patient.factory('PatientServ', ['$resource',
    function ($resource) {
        "use strict";
        return $resource('api/patients/:patientId', null, {
            query: {method: 'GET', params: {patientId: 'patient'}, isArray: true},
            get : {method: 'GET', params: {patientId: 'patient'}},
            save : {method : 'PUT'}
        });
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

patient.controller('PatientCtrl', ['$scope', '$routeParams', '$filter', 'PatientServ', function($scope, $routeParams, $filter, PatientServ) {
        "use strict";
        $scope.patient = PatientServ.get({patientId : $routeParams.patientId});
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

        $scope.savePatient = function () {
            $scope.patient.birth_date = $filter('date')($scope.patient.birth_date, 'yyyy-MM-dd');
            return PatientServ.save({patientId:$scope.patient.id}, $scope.patient);
        };
}]);