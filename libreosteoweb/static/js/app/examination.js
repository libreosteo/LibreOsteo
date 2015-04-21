var examination = angular.module('loExamination', ['ngResource']);


examination.factory('ExaminationServ', ['$resource',
    function ($resource) {
        "use strict";
        return $resource('api/examinations/:examinationId', null, {
            query: {method: 'GET', isArray : true},
            get : {method: 'GET', params : {examinationId : 'examination'} },
            save : {method : 'PUT'},
            add : {method : 'POST'},
            close : {
                method : 'POST',
                params : {examinationId : 'examinationId'},
                url : 'api/examinations/:examinationId/close'
            },
        });
    }
]);

examination.factory('ExaminationCommentServ', ['$resource',
    function ($resource) {
        return $resource('api/examinations/:examinationId/comments', null, {
            query : { method : 'GET', isArray : true},
        });
    }
    ]);

examination.factory('CommentServ', ['$resource', 
    function($resource) {
        return $resource('api/comments', null)
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
            close : '&',
            newExamination: '=',
        },
      compile: function(element, attrs){
          if (!attrs.newExamination) {attrs.newExamination = false};

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

            $scope.$watch('model.status', function(newValue, oldValue){
                if (newValue){
                    $scope.readOnly = newValue != 0; 
                }
            });
        },
        templateUrl: 'web-view/partials/examination'
    }
});