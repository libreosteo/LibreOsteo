
/**
    This file is part of Libreosteo.

    Libreosteo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Libreosteo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Libreosteo.  If not, see <http://www.gnu.org/licenses/>.
*/
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
        controller : function($scope, ExaminationServ, ExaminationCommentServ, CommentServ, loEditFormManager) {
          $scope.loadExamination = function(examinationId) {
            if ($scope.currentExamination.id == null)
            {
              ExaminationServ.get({examinationId : examinationId}, function(data){
                  $scope.archiveExamination.data = data;
                  loEditFormManager.available = true;

              });
            } else if ($scope.currentExamination.id == examinationId) {
              // callback the currentExamination manager
              $scope.currentExaminationManager();
            } else {
              ExaminationServ.get({examinationId : examinationId}, function(data){
                  $scope.archiveExamination.data = data;
                  loEditFormManager.available = true;
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
              var examination = $scope.examinations.find(function(element, index, array)
              {
                return element.id == examinationId;
              });
              examination.comments_list.unshift(result);
              examination.comments = examination.comments_list.length;
           });
          }
        },
        templateUrl: 'web-view/partials/examinations-timeline'
    }
});
