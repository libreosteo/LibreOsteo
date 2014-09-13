var timeline = angular.module('loTimeline', []);

// Define the directive
timeline.directive('timeline', function()
{
    "use strict";
    return {
        restrict: 'E',
        transclude: true,
        scope: {
            examinations: '=',
        },

        templateUrl: 'web-view/partials/examinations-timeline'
    }
});
