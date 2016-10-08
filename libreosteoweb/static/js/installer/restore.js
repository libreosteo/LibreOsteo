var restore = angular.module('installerRestore', ['ngResource', 'ngFileUpload']);

restore.controller('RestoreCtrl', ['$scope', 'Upload', '$http', '$window', function($scope, Upload, $http, $window)
{
    $scope.in_progress = false;
	$scope.restore = function() {
      if ($scope.forms.form_dump.$valid && $scope.files.archiveFile) {
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
            console.log('Error status : '+resp.status);
            $scope.in_progress = false;
        }, function (evt){
            var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
        });
    };

}]);