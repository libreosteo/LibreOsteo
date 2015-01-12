var officeEvent = angular.module('loOfficeEvent', ['ngResource', 'loPatient']);

officeEvent.factory('OfficeEventServ', ['$resource',
    function ($resource) {
        "use strict";
        return $resource('api/events', null, {
            query: {method: 'GET', isArray : true}
        });
    }
]);

officeEvent.controller('OfficeEventCtrl', ['$scope', 'growl', 'OfficeEventServ',
    function($scope, growl, OfficeEventServ) {
        "use strict";
        $scope.events = OfficeEventServ.query();
        
    }
]);


officeEvent.directive('officeevent', ['PatientServ', 'ExaminationServ', function(PatientServ, ExaminationServ){
    return {
    restrict: 'E',
    //transclude : true,
    scope: {
        officeevents : '=',
    },
    controller: function($scope)
    {
        "use strict";
        
        $scope.getPatientName = function(officeevent){
            var patient = {};
            if(officeevent.clazz === 'Patient'){
                //patient = PatientServ.get({patientId : officeevent.reference }, function(p){
                //    console.log(angular.tojson(p));
                //});
                console.log(angular.toJson(patient));
            } else if( officeevent.clazz === 'Examination'){
                //var examination = ExaminationServ.get({examinationId : officeevent.reference});
                //patient = PatientServ.get({patientId : examination.patient})
                patient.familyname = "TEST";
                patient.firstname = "Test";
            }
            return patient.familyname + " "+patient.firstname;
        };
        
        
    },

    templateUrl: 'web-view/partials/officeevent'
  }
}
]);