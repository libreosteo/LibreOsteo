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

    $scope.restore = function() {
      if ($scope.forms.form_dump.$valid && $scope.files.archiveFile) {
        $scope.upload_dump($scope.files);
      }
    };

    $scope.upload_dump = function(dump)
    {
        Upload.upload({
            url : 'internal/restore',
            data : {file : dump.archiveFile}
        }).then(function (resp)
        {
            console.log('Success ' + resp.config.data.file.name + ' uploaded. ');
            $scope.result_restore = resp.data;
            $scope.forms.form_dump.archiveFile = null;
            if ($scope.result_restore = 'reloaded')
            {
                // Display a popup which indicates that all base wes reloaded and user was reinitialized. 
                //  You have to be connected again
                // After reload the page
                $window.location.reload();
            }
        }, function(resp) {
            console.log('Error status : '+resp.status);
        }, function (evt){
            var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
        });
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