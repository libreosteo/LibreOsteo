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
            currentExamination : '=',
            currentExaminationManager : '&',
        },
        controller : function($scope, ExaminationServ) {
          $scope.loadExamination = function(examinationId) {
            if ($scope.currentExamination.id == null)
            {
              ExaminationServ.get({examinationId : examinationId}, function(data){
                  $scope.archiveExamination.data = data;
              });
            } else if ($scope.currentExamination.id == examinationId) {
              // callback the currentExamination manager
              $scope.currentExaminationManager();
            } else {
              ExaminationServ.get({examinationId : examinationId}, function(data){
                  $scope.archiveExamination.data = data;
                });
            }
          }  ;
        },
        templateUrl: 'web-view/partials/examinations-timeline'
    }
});
