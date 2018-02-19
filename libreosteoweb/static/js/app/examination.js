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
            delete : { method : 'DELETE', params : {examinationId : 'examinationId'}},
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


examination.directive('examination', ['ExaminationServ', function(ExaminationServ){
    "use strict";
    return {
        restrict: 'E',
        scope: {
            model: '=',
            saveModel : '&',
            close : '&',
            newExamination: '=',
            onDelete : '&',
        },
      compile: function(element, attrs){
          if (!attrs.newExamination) {attrs.newExamination = false};

        },
        controller : [ '$scope', '$filter', '$window', 'growl', '$q', function($scope, $filter, $window, growl, $q)
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

            $scope.$watch('model.status', function(newValue, oldValue){
               $scope.updateDeleteTrigger(); 
            });

            $scope.$watch('model.id', function(newValue, oldValue)
            {
                $scope.updateDeleteTrigger();
            });

            $scope.updateDeleteTrigger = function() {
                if ($scope.newExamination) {
                    $scope.editableForm.$show();
                }

                if($scope.model == null)
                {
                    $scope.triggerEditForm.delete = false;
                    return;
                }
                if( $scope.model.status != 0){
                    $scope.triggerEditForm.delete = false;
                } else {
                    if($scope.model.id){
                        $scope.triggerEditForm.delete = true;            
                    } else {
                        $scope.triggerEditForm.delete = false;
                    }
                }
            };

            $scope.printInvoice = function(examination)
            {
                var invoiceTab = $window.open('invoice/' + examination.invoice , '_blank');

                setTimeout(function() {
                    invoiceTab.print();
                }, 750);
            };

            $scope.delete = function()
            {
                if($scope.model.id)
                {
                    ExaminationServ.delete({examinationId : $scope.model.id}, function(resultOk)
                        {
                            if ($scope.onDelete)
                            {
                                $scope.onDelete();
                            }   
                        }, function(resultNok)
                        {
                            console.log(resultNok);
                            growl.addErrorMessage("This operation is not available");
                        });
                }
                
            };

            $scope.$watch('editableForm.$visible', function(newValue, oldValue)
            {
                if(oldValue === false && newValue === true)
                {
                    $scope.triggerEditForm.edit = false;
                    $scope.triggerEditForm.save = true;
                } else if(oldValue === true && newValue === false )
                {
                    $scope.triggerEditForm.edit = true;
                    $scope.triggerEditForm.save = false;
                }
            });

            $scope.edit = function() {
                $scope.editableForm.$show();
            };

            $scope.save = function()
            {
                $scope.editableForm.$save();
            };

            $scope.saveAndClose = function()
            {
                $scope.close($scope.model);
            };
            
            $scope.triggerEditForm = {
                save: false,
                edit: true,
                cancel: null,
                delete: false,
            };
            
        }],
        templateUrl: 'web-view/partials/examination'
    }
}]);