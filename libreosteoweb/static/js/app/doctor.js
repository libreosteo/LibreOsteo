var doctor = angular.module('loDoctor', ['ngResource']);


doctor.factory('DoctorServ', ['$resource',
    function ($resource) {
        "use strict";
        return $resource('api/doctors/:doctorId', null, {
            query: {method: 'GET', isArray : true},
            get : {method: 'GET', params: {doctorId: 'doctor'}},
            save : {method : 'PUT'},
            add : {method : 'POST'}
        });
    }
]);


doctor.controller('DoctorCtrl', ['$scope', '$routeParams', 'DoctorServ', function ($scope, $routeParams, DoctorServ) {
        "use strict";
        $scope.doctor = DoctorServ.get({doctorId : $routeParams.doctorId});
        }
]);