var examination = angular.module('loExamination', ['ngResource']);


examination.factory('ExaminationServ', ['$resource',
    function ($resource) {
        "use strict";
        return $resource('api/examinations/:examinationId', null, {
            query: {method: 'GET', isArray : true},
            get : {method: 'GET', params : {examinationId : 'examination'} },
            save : {method : 'PUT'},
            add : {method : 'POST'}
        });
    }
]);

examination.controller('ExaminationCtrl', ['$scope', '$routeParams', 'ExaminationServ', function ($scope, $routeParams, DoctorServ) {
        "use strict";
        $scope.examination = ExaminationServ.get({examinationId : $routeParams.examinationId});
    }
]);


examination.directive('examination', function(){
    "use strict";
    return {
        restrict: 'E',
        scope: {
            model: '=',
            saveModel : '&',
            invoice : '&',
            readOnly : '@',
        },
        templateUrl: 'web-view/partials/examination'
    }
});