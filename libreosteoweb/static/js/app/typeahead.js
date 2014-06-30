var typeAhead = angular.module('loTypeAhead', []);

typeAhead.factory('searchFactory', function($http) {
  return {
    get: function(query) {
      return $http.get("/api/patients/?q=" + query).then(function(resp) {
        return resp.data;
      });
    }
  };
});

// Define the Controller
typeAhead.controller('TypeAheadController', function ($scope, $location, searchFactory) {
    $scope.searchPatients = function () {
        "use strict";
        if ($scope.queryFragment.length >= 3) {
            searchFactory.get($scope.queryFragment).then(function (data) {
                $scope.items = data;
            });
        } else {
            $scope.items = [];
        }
    };
    $scope.$watch('queryFragment', function (newValue, oldValue) {
        "use strict";
        $scope.searchPatients();
    });
    $scope.items = [];
    $scope.queryFragment = "";
    $scope.patient = "";
    $scope.onItemSelected = function () {
        $scope.items = [];
        $scope.queryFragment = "";
        $location.path('/patient/' + $scope.patient.id);
    };
});



// Define the directive
typeAhead.directive('typeahead', function($timeout) {
  return {
    restrict: 'AEC',
    scope: {
        query : '=',
        items : '=',
		onSelect:'&',
        model : '='
	},
	link:function(scope,elem,attrs){
	   scope.handleSelection=function(selectedItem){
		 scope.model=selectedItem;
		 scope.selected=true;
		 $timeout(function(){
			 scope.onSelect();
		  },100);
         scope.current = 0;
	  };

	  scope.current=0;
	  scope.selected=true;
	  scope.isCurrent=function(index){
		 return scope.current==index;
	  };
	  scope.setCurrent=function(index){
		 scope.current=index;
	  };
	},
    templateUrl: 'static/js/app/templates/typeahead-list.html'
  }
});
