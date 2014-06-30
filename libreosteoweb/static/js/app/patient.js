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

patient.controller('PatientCtrl', ['$scope', '$routeParams', 'PatientServ', function($scope, $routeParams, PatientServ) {
        "use strict";
        $scope.patient = PatientServ.get({patientId : $routeParams.patientId});

        $scope.savePatient = function () {
            console.log('Patient = '+angular.toJson($scope.patient));
            return PatientServ.save({patientId:$scope.patient.id}, $scope.patient);
        };
}]);