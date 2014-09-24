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
            archiveExamination : '=',
        },
        controller : function($scope, ExaminationServ) {
          $scope.loadExamination = function(examinationId) {
              ExaminationServ.get({examinationId : examinationId}, function(data){
                  $scope.archiveExamination.data = data;
              });
          }  ;
        },
        templateUrl: 'web-view/partials/examinations-timeline'
    }
});
