
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
var dashboard = angular.module('loDashboard', ['ngResource', 'loOfficeEvent']);

dashboard.factory('DashboardServ', ['$resource',
    function ($resource) {
        "use strict";
        return $resource('api/statistics', null, {
            query: {method: 'GET', isArray : true}
        });
    }
]);

dashboard.controller('DashboardCtrl', ['$scope', '$filter', 'growl', 'DashboardServ', 'OfficeEventServ', 'TherapeutSettingsServ',
    function($scope, $filter, growl, DashboardServ, OfficeEventServ, TherapeutSettingsServ) {
        "use strict";
        $scope.selector = 'week';
        $scope.statistics = null;
        $scope.officeEventLoader = null;

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

        TherapeutSettingsServ.get_by_user().$promise.then(function(therapeutSettings) {

            if (therapeutSettings.stats_enabled) {
                $scope.statistics = DashboardServ.get(function(data){
                    $scope.statistics = data;
                    $scope.show($scope.selector);
                });
            }


            if (therapeutSettings.last_events_enabled) {
                $scope.officeEventLoader = new OfficeEventServ();
            }

        });
    }
]);
