var dashboard = angular.module('loDashboard', ['ngResource', 'loOfficeEvent']);

dashboard.factory('DashboardServ', ['$resource',
    function ($resource) {
        "use strict";
        return $resource('api/statistics', null, {
            query: {method: 'GET', isArray : true}
        });
    }
]);

dashboard.controller('DashboardCtrl', ['$scope', '$filter', 'growl', 'DashboardServ', 'OfficeEventServ',
    function($scope, $filter, growl, DashboardServ, OfficeEventServ) {
        "use strict";
        $scope.selector = 'week';

        var describe_map = function(range_array){
            var map = {};
            for(var i = 0; i < range_array.length; i++)
            {
                map[i] = range_array[i];
            }
            return map;
        };

        var showObjSparklines = function(obj) {
            $('.inlinesparkline-newpatient').sparkline(obj.nb_new_patient[1],{
                type: 'line',
                tooltipFormat: '{{x:labels}} - {{y}}',
                tooltipValueLookups: {
                    labels: $.range_map(describe_map(obj.nb_new_patient[0]))
                }
            });

            $('.inlinesparkline-nbexamination').sparkline(obj.nb_examination[1],{
                type: 'line',
                tooltipFormat: '{{x:labels}} - {{y}}',
                tooltipValueLookups: {
                    labels: $.range_map(describe_map(obj.nb_examination[0]))
                }
            });
            $('.inlinesparkline-urgentreturn').sparkline(obj.nb_urgent_return[1], {
                type: 'line',
                tooltipFormat: '{{x:labels}} - {{y}}',
                tooltipValueLookups: {
                    labels: $.range_map(describe_map(obj.nb_urgent_return[0]))
                }
            });
        };

        var showStatistics = function(obj)
        {
            $scope.nb_new_patient = obj.nb_new_patient;
            $scope.nb_examination = obj.nb_examination;
            $scope.nb_urgent_return = obj.nb_urgent_return;
        }

        $scope.show = function(selector) {
            $scope.selector = selector;
          if(selector == 'week'){
                showStatistics($scope.statistics.week);
                showObjSparklines($scope.statistics.history.week);
          } else if (selector == 'month') {
                showStatistics($scope.statistics.month);
                showObjSparklines($scope.statistics.history.month);
          } else if (selector == 'year') {
                showStatistics($scope.statistics.year)
                showObjSparklines($scope.statistics.history.year);
          }
        };

        $scope.statistics = DashboardServ.get(function(data){
           $scope.statistics = data;
            $scope.show($scope.selector);
        });

        $scope.officeEventLoader = new OfficeEventServ();

    }
]);
