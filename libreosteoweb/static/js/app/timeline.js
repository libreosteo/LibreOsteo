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
        controller : function($scope, ExaminationServ, ExaminationCommentServ, CommentServ) {
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

          $scope.loadComments = function(examinationId, event) {
            if ($scope.currentExamination.id == null || $scope.currentExamination.id != examinationId) {
              var panelComment = $(event.target).parents(".timeline-footer").next(".timeline-panel-footer");

              ExaminationCommentServ.query({examinationId : examinationId}, function(data){  
                panelComment.toggleClass('hidden');
                var examination = $scope.examinations.find(function(element, index, array)
                  {
                    return element.id == examinationId;
                  });
                examination.comments_list = data;
              });
              event.stopPropagation();
            }
          };
          $scope.no_propagate = function(event)
          {
            event.stopPropagation();
          }

          $scope.sendComment = function(examinationId, comment)
          {
           var data = {
            comment : comment,
            examination : examinationId,
           };
           CommentServ.save(data, function(result) {
              console.log(angular.toJson(result));
              var examination = $scope.examinations.find(function(element, index, array)
              {
                return element.id == examinationId;
              });
              if (!result.date.endsWith('Z'))
              {
                result.date += 'Z';
              }
              examination.comments_list.unshift(result);
              examination.comments = examination.comments_list.length;
           });
          }
        },
        templateUrl: 'web-view/partials/examinations-timeline'
    }
});
