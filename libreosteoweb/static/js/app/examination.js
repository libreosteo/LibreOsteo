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

function isEmpty(str) {
    return (!str || 0 === str.length);
}


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
                { value : 1, text : gettext('Normal examination') },
                { value : 2, text : gettext('Continuing examination') },
                { value : 3, text : gettext('Return') },
                { value : 4, text : gettext('Emergency') },
            ];
            $scope.showTypes = function() {
                if($scope.model) {
                    var selected = $filter('filter')($scope.types, {value: $scope.model.type});
                    return ($scope.model && $scope.model.type && selected.length) ? selected[0].text : gettext('not documented');
                } else {
                    return gettext('not documented');
                }
            };

            $scope.$watch('model.status', function(newValue, oldValue){
                if (newValue){
                    $scope.readOnly = newValue != 0; 
                }
            });

            $scope.examinationSettings = {
                orl : false,
                visceral : false,
                pulmo : false,
                uro_gyneco : false,
                periphery : false,
                general_state : false,
            }

            $scope.accordionOpenState = {
                orl : true,
                visceral : true,
                pulmo : true,
                uro_gyneco : true,
                periphery : true,
                general_state : true
            }

            $scope.$watch('model.orl', function(newValue, oldValue){
                $scope.examinationSettings.orl = !isEmpty(newValue);
            });
            $scope.$watch('model.visceral', function(newValue, oldValue){
                $scope.examinationSettings.visceral = !isEmpty(newValue);
            });
            $scope.$watch('model.pulmo', function(newValue, oldValue){
                $scope.examinationSettings.pulmo = !isEmpty(newValue);
            });
            $scope.$watch('model.uro_gyneco', function(newValue, oldValue){
                $scope.examinationSettings.uro_gyneco = !isEmpty(newValue);
            });
            $scope.$watch('model.periphery', function(newValue, oldValue){
                $scope.examinationSettings.periphery = !isEmpty(newValue);
            });
            $scope.$watch('model.general_state', function(newValue, oldValue){
                $scope.examinationSettings.general_state = !isEmpty(newValue);
            });
            
        },
        templateUrl: 'web-view/partials/examination'
    }
});