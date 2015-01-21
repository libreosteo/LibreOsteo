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
        $scope.statistics = DashboardServ.get();
        $scope.selector = 'week';
        $scope.show = function(selector) {
            $scope.selector = selector;
          if(selector == 'week'){
                $scope.nb_new_patient = $scope.statistics.week.nb_new_patient;
                $scope.nb_examination = $scope.statistics.week.nb_examination;
                $scope.nb_urgent_return = $scope.statistics.week.nb_urgent_return;
          } else if (selector == 'month') {
                $scope.nb_new_patient = $scope.statistics.month.nb_new_patient;
                $scope.nb_examination = $scope.statistics.month.nb_examination;
                $scope.nb_urgent_return = $scope.statistics.month.nb_urgent_return;
          } else if (selector == 'year') {
                $scope.nb_new_patient = $scope.statistics.year.nb_new_patient;
                $scope.nb_examination = $scope.statistics.year.nb_examination;
                $scope.nb_urgent_return = $scope.statistics.year.nb_urgent_return;
          }
        };

        $scope.statistics = DashboardServ.get(function(data){
           $scope.statistics = data;
            $scope.show($scope.selector);
        });

        $scope.eventsByDay = {};
        $scope.events = OfficeEventServ.query(function(data){
            angular.forEach($scope.events, function(officeevent, index){
                var date = new Date(officeevent.date);
                var key = $filter('date')(
                    new Date(date.getFullYear(), date.getMonth(), date.getDate()),
                    'yyyy-MM-dd');
                if (!this[key]) {
                    this[key] = [ officeevent, ];
                } else {
                    this[key].push(officeevent);
                }

            }, $scope.eventsByDay);
        });
    }
]);
