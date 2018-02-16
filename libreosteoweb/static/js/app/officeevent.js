
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
var officeEvent = angular.module('loOfficeEvent', ['loPatient']);

officeEvent.factory('OfficeEventServ', ['$http', '$filter', function ($http, $filter){
    var OfficeEventLoader = function() {
        this.items = [];
        this.busy = false;
        this.after = '';
        this.itemsByDay = [];
        this.hasFinish = false;
    };
    OfficeEventLoader.prototype.loadEvents = function() {
        if (this.busy) return;
        this.busy = true;

        var url = "/api/events?limit=10&offset=" + this.after ;
        $http.get(url).success(function(data) {
            var items = data.results;
            for (var i = 0; i < items.length; i++) {
                this.items.push(items[i]);
            }
            this.after = "" + this.items.length;
            if (items.length == 0){
                this.hasFinish = true;
                this.busy = false;
                return;
            }

            // Build the list ordonned by Day to prepare the list to display.
            angular.forEach(this.items, function(officeevent, index){
                var date = new Date(officeevent.date);
                var key = $filter('date')(
                    new Date(date.getFullYear(), date.getMonth(), date.getDate()),
                    'yyyy-MM-dd');
                var obj = {
                    day : null,
                    list : []
                };
                angular.forEach(this, function(myobj, idx){
                    if(myobj.day == key){
                        obj = myobj;
                    }
                });
                if (obj.day == null) {
                    obj.day = key;
                    this.push(obj);
                }
                var found = false;
                angular.forEach(obj.list, function(item, idx){
                    if (item.id == officeevent.id)
                        found = true;
                });
                if (!found)
                    obj.list.push(officeevent);

                }, this.itemsByDay);

            this.busy = false;
        }.bind(this));
    };

    return OfficeEventLoader;
}]);

officeEvent.controller('OfficeEventCtrl', ['$scope', 'growl', 'OfficeEventServ',
    function($scope, growl, OfficeEventServ) {
        "use strict";
    }
]);


officeEvent.directive('officeevent', ['$location', 'PatientServ', 'ExaminationServ', function($location, PatientServ, ExaminationServ){
    return {
    restrict: 'E',
    //transclude : true,
    scope: {
        officeevents : '=',
        officeeventsByDay : '=',
        busy : '=',
        officeEventLoader : '='
    },
    controller: function($scope, $location)
    {
        "use strict";
        $scope.selector = 'day';

        $scope.loadOfficeevent = function(officeevent)
        {
            if (officeevent.clazz === 'Patient'){
                $location.path('/patient/'+officeevent.reference);
            } else if(officeevent.clazz === 'Examination')
            {
                ExaminationServ.get({examinationId : officeevent.reference}, function(data){
                  $location.path('/patient/'+data.patient+'/examination/'+officeevent.reference);
                });
            }
        };
        $scope.show = function(selector) {
            $scope.selector = selector;
        };
        console.log($scope.officeEventLoader);
    },

    templateUrl: 'web-view/partials/officeevent'
  }
}
]);
