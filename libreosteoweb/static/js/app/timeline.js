var timeline = angular.module('loTimeline', ['loExamination']);

// Define the directive
timeline.directive('timeline', function()
{
    "use strict";
    return {
        restrict: 'E',
        transclude: true,
        scope: {
            examinations: '=',
            startExamination : '&',
            examinationIsActive : '=',
        },
        controller : function($scope, ExaminationServ) {
          $scope.loadExamination = function(examinationId) {
              $scope.$parent.archiveExamination = ExaminationServ.get({examinationId : examinationId}, function(e)
                {
                    console.log(angular.toJson($scope.$parent.archiveExamination));
                });
          }  ;
        },
        templateUrl: 'web-view/partials/examinations-timeline'
    }
});
