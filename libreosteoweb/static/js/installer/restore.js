
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
var restore = angular.module('installerRestore', ['ngResource', 'ngFileUpload']);

restore.controller('RestoreCtrl', ['$scope', 'Upload', '$http', '$window', function($scope, Upload, $http, $window)
{
    $scope.in_progress = false;
	$scope.restore = function() {
      if ($scope.forms.form_dump.$valid && $scope.files.archiveFile) {
        $scope.error = null;
        $scope.upload_dump($scope.files);
      }
    };

    $scope.upload_dump = function(dump)
    {
        $scope.in_progress = true;
        Upload.upload({
            url : '/internal/restore',
            data : {file : dump.archiveFile}
        }).then(function (resp)
        {
            console.log('Success ' + resp.config.data.file.name + ' uploaded. ');
            $scope.in_progress = false;
            $scope.result_restore = resp.data;
            $scope.forms.form_dump.archiveFile = null;
            if ($scope.result_restore = 'reloaded')
            {
                // Display a popup which indicates that all base was reloaded and user was reinitialized.
                //  You have to be connected again
                // After reload the page
                $window.location.assign("/");
            }
        }, function(resp) {
            $scope.in_progress = false;
            $scope.error = resp.data;
        }, function (evt){
            var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
        });
    };

}]);
