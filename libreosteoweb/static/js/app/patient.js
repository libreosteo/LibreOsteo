var patientController = angular.module('loPatientController', []);

patientController.controller('PatientCtrl', ['$scope', '$routeParams',
    function($scope, $routeParams) {
        "use strict";
        $scope.patientId = $routeParams.patientId;
    }
    ]);