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
            readOnly : '=',
        },
      compile: function(element, attrs){
          if (!attrs.readOnly) { attrs.readOnly = false; }

        },
        controller : function($scope, $filter)
        {
            $scope.types = [
                { value : 1, text : 'Consultation normale' },
                { value : 2, text : 'Retour prévu (Contrôle)' },
                { value : 3, text : 'Retour non prévu' },
                { value : 4, text : 'Urgence' },
            ];
            $scope.showTypes = function() {
                if($scope.model) {
                    var selected = $filter('filter')($scope.types, {value: $scope.model.type});
                    return ($scope.model && $scope.model.type && selected.length) ? selected[0].text : 'Non renseigné';
                } else {
                    return 'Non renseigné';
                }
            };
        },
        templateUrl: 'web-view/partials/examination'
    }
});