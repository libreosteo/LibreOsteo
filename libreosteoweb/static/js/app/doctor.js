
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
var doctor = angular.module('loDoctor', ['ngResource']);


doctor.factory('DoctorServ', ['$resource',
    function ($resource) {
        "use strict";
        return $resource('api/doctors/:doctorId', null, {
            query: {method: 'GET', isArray : true},
            get : {method: 'GET', params: {doctorId: 'doctor'}},
            save : {method : 'PUT'},
            add : {method : 'POST'}
        });
    }
]);


doctor.controller('DoctorCtrl', ['$scope', '$routeParams', 'DoctorServ', function ($scope, $routeParams, DoctorServ) {
    "use strict";
    $scope.doctorDetails = DoctorServ.get({doctorId : $routeParams.doctorId});
}]);

var DoctorAddFormCtrl = function($scope, $uibModalInstance) {
    "use strict";
    $scope.doctor = {
        family_name : null,
        first_name : null,
        phone : null,
        city : null

    };
    $scope.ok = function () {
      $uibModalInstance.close($scope.doctor);
    };

    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
};


/** A Directive to select a doctor among existing ones or create a new one
 *
 * It will fill a field on an existing data structure with the selected doctor ID.
 * It uses a two-modes widget (editable-select) from angular-xeditable.
 */
doctor.directive('doctorSelector', ['DoctorServ', function(DoctorServ) {
    "use strict";
    return {
        restrict: 'E',
        scope: {
            // object receiving the selected doctor ID in one of its properties
            doctorHolder: '=',
            // Name of the docterHolder property receividing the selected doctor ID
            doctorHolderProperty: '=?',
        },
        templateUrl: 'web-view/partials/doctor-selector',
        controller: function($scope, $uibModal, DoctorServ) {
            if (angular.isUndefined($scope.doctorHolderProperty)) {
                $scope.doctorHolderProperty = 'id'; // default
            }
            $scope.doctors = [];
            $scope.addDoctorButtonVisible = false;

            $scope.onSwitchToEdit = function() {
                $scope.addDoctorButtonVisible = true;
                return DoctorServ.query(function(result){
                    $scope.doctors = result;
                });
            };

            $scope.onSwitchToView = function() {
                $scope.addDoctorButtonVisible = false;
            };

            // Fetch doctor details (on initial load or after doctor add)
            $scope.$watch('doctorHolder.'+ $scope.doctorHolderProperty, function(newValue, oldValue){
                if (newValue){
                    DoctorServ.get({doctorId: newValue}).
                        $promise.then(function(result) {
                            $scope.doctorDetails = result;
                        });
                }
            });

            // Prepare and define the modal function to add doctor.
            $scope.formAddDoctor = function($event) {
                var modalInstance = $uibModal.open({
                    templateUrl: 'web-view/partials/doctor-modal',
                    controller : DoctorAddFormCtrl
                });
                modalInstance.result.then(function (newDoctor){
                    DoctorServ.add(newDoctor).$promise.then(
                        function(savedDoctor) {
                            $scope.doctors.push(savedDoctor);
                            $scope.doctorHolder[$scope.doctorHolderProperty] = savedDoctor.id;
                        }
                    );
                });
            };
        },
    };
}]);
