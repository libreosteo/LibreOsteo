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


officeEvent.directive('officeevent', ['$location', 'PatientServ', 'ExaminationServ', function($location, PatientServ, ExaminationServ){
    return {
    restrict: 'E',
    //transclude : true,
    scope: {
        officeevents : '=',
    },
    controller: function($scope, $location)
    {
        "use strict";
        $scope.loadOfficeevent = function(officeevent)
        {
            if (officeevent.clazz === 'Patient'){
                $location.path('/patient/'+officeevent.reference);
            } else if(officeevent.clazz === 'Examination')
            {
                ExaminationServ.get({examinationId : officeevent.reference}, function(data){
                  $location.path('/patient/'+data.patient+'/examination/'+officeevent.reference);
                });
            }
        }
    },

    templateUrl: 'web-view/partials/officeevent'
  }
}
]);