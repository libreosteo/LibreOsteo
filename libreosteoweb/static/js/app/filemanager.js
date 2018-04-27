
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
var fileManager = angular.module('loFileManager', ['ngFileUpload']);


fileManager.factory('loFileManager', function() {
	return {
		createFileContext : function(){
			var _files = [];
			var _patient = null;
			var _callback = function () {};
			return {
				files : function(files) {
					if(files)
					{
						_files = [];
						angular.forEach(files , function(value, key){
							_files.push({
								file : value,
								status : 0,
								title : null,
								date : null,
								notes : null
							});
						});
					}
					return _files;
				},
				patient : function(patient) {
					if(patient)
					{
						_patient = patient;
					}
					return _patient;
				},
				setDocumentAddedCb : function(callback) {
					_callback = callback;
				},
				callback : function()
				{
					return _callback;
				}
			};
		},
	}
});



fileManager.factory('FileServ', ['$resource',
    function ($resource) {
        "use strict";
        return  $resource('api/documents/:patientDocId', null, {
            query: {method: 'GET' },
            get : {method: 'GET', params: {patientDocId: 'docId'}},
            save : {method : 'PUT', params : {patientDocId : 'docId'}},
            add : {method : 'POST'},
            delete : { method : 'DELETE', params : {patientDocId : 'docId'}},
        });
    }
]);


fileManager.directive('fileManager', [ 'FileServ', 'Upload', '$filter', function(fileService, Upload, $filter)
{
	return {
		restrict : 'E',
		scope: {
	      context: "=context"
	    },
    controller : ['$scope', function($scope) {
    	$scope.validate = function() {
    		console.info("Should send all files to the service");
    	}

    	$scope.send = function(doc)
    	{
    		if(doc.status == 5) {
    			doc.status = 0
    			return;
    		}
    		if(doc.status != 0)
    		{
    			return;
    		}
    		console.info(doc);
    		doc.status = 1;
    		var doc_date = '';
    		if (doc.date) {
    			console.info("date for doc : "+doc.date);
    			doc_date = $filter('date')(doc.date, 'yyyy-MM-dd');
    		}
    		var doc_notes = '';
    		if(doc.notes) {
    			doc_notes = doc.notes;
    		}

    		Upload.upload({
	            url: 'api/patient-documents',
	            data: {	'patient': $scope.context.patient().id,
	            		'document.document_file' : doc.file,
	            		'document.title' : doc.title,
	            		'document.notes' : doc_notes,
	            		'document.document_date' : doc_date,
	            		'attachment_type' : 5
	        	}
	        }).then(function (resp) {
	            console.info('Success ' + resp + ' uploaded. ');
	            $scope.result_analyze = resp.data;
	            doc.status = 2;
	            $scope.context.callback()();
	        }, function (resp) {
	            console.error('Error status: ' + resp.status);
	            doc.status = 5;
	        }, function (evt) {
	            var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
	            //console.log('progress: ' + progressPercentage + '% ' + evt.config.data.file_patient.name);
	        });
    	}

    	$scope.files = [];

    	$scope.$watch(function($scope) {
    		var result = undefined;
    		if($scope.context) {
    			result = $scope.context.files();
    		}
    		$scope.updateComponentPolyfill();
    		return result;
    	}, function(newValue){
    		$scope.files.length = 0;
    		angular.forEach(newValue, function(value) {
    			if(value.status != 2){
    				this.push(value);
    			}
    		}, $scope.files);
    	});

    	$scope.updateComponentPolyfill = function() {
            // To be compliant with all browser.
            var els = angular.element(".polyfill-updatable");
	    angular.forEach(els, function(el) {
		var jqEl = $(el);
		if (jqEl.is(':visible')) {
			jqEl.updatePolyfill();
		}
	    });
        }

    }],
    templateUrl: 'web-view/partials/filemanager'
  }
}]);
