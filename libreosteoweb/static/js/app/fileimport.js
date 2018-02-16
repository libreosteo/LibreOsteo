
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
var fileimport = angular.module('loFileImport', ['ngResource','ngFileUpload']);

fileimport.controller('ImportFileCtrl', ['$scope', 'Upload', '$http', '$window', function($scope, Upload, $http, $window)
{
    $scope.forms = {};
    $scope.files = {};
    $scope.result_analyze = null;
    $scope.import_result = null;
    $scope.import_error = null;
    $scope.import_fatal = null;
    $scope.analyze = function() {
      if ($scope.forms.form.$valid && $scope.files.patientFile) {
        $scope.upload($scope.files);
      }
    };

// upload on file select or drop
    $scope.upload = function (files) {
        Upload.upload({
            url: 'api/file-import',
            data: {file_patient: files.patientFile, file_examination: files.examinationFile}
        }).then(function (resp) {
            console.log('Success ' + resp.config.data.file_patient.name + ' uploaded. ');
            $scope.result_analyze = resp.data;
            //console.log(angular.toJson($scope.result_analyze));
            $scope.forms.form.patientFile = null;
            $scope.forms.form.examinationFile = null;
        }, function (resp) {
            console.log('Error status: ' + resp.status);
        }, function (evt) {
            var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
            //console.log('progress: ' + progressPercentage + '% ' + evt.config.data.file_patient.name);
        });
    };

    $scope.import = function() {
        if($scope.result_analyze.status == 1)
        {
            $http( {
                method: 'POST',
                url : 'api/file-import/'+$scope.result_analyze.id+'/integrate'
            }).then( function success(response)
            {
                if(response.data.patient != 0)
                {
                    $scope.import_result = response.data;
                }
                if(response.data.patient.errors.length != 0 || response.data.examination.errors.length != 0)
                {
                    $scope.import_error = response.data;
                }
                $('#import-result').animatescroll();
            }, function error(response) {
                $scope.import_fatal = response.data;
                $('#import-result').animatescroll();
            });
        }
    }
}]);
