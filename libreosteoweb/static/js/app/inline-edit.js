var inlineEdit = angular.module('loInlineEdit', []);
// Define the directive
inlineEdit.directive('inlineedit', function() {
  return {
    restrict: 'E',
    transclude : true,
    scope: {
        model : '=',
        property: '@',
        onSave : '&',
        placeholder : '@',
        editclass : '@',
        width: '@'
	},
    controller: function($scope)
    {
        "use strict";
        $scope.displayButton = false;
    },
	link:function(scope,elem,attrs){

        scope.saveModel = function() {
            "use strict";
          scope.onSave();
        };
	 },
      compile: function(element, attrs){
       if (!attrs.width) { attrs.width = '100%'; }
    },

    templateUrl: 'static/js/app/templates/inline-edit.html'
  }
});

inlineEdit.directive('inlinetel', function() {
  return {
    restrict: 'E',
    transclude : true,
    scope: {
        model : '=',
        property: '@',
        onSave : '&',
        placeholder : '@',
        editclass : '@',
        width: '@',
        icon : '@'
	},
    controller: function($scope)
    {
        "use strict";
        $scope.displayButton = false;
    },
	link:function(scope,elem,attrs){
        scope.saveModel = function() {
            "use strict";
          scope.onSave();
        };

	 },
    compile: function(element, attrs){
       if (!attrs.width) { attrs.width = '100%'; }
    },

    templateUrl: 'static/js/app/templates/inline-tel.html'
  }
});



inlineEdit.directive('inlinetextarea', function() {
  return {
    restrict: 'E',
    transclude : true,
    scope: {
        model : '=',
        property: '@',
        onSave : '&',
        placeholder : '@',
        editclass : '@',
        width: '@',
        row : '@',
        col : '@'
	},
    controller: function($scope)
    {
        "use strict";
        $scope.displayButton = false;
    },
	link:function(scope,elem,attrs){
        scope.saveModel = function() {
            "use strict";
          scope.onSave();
        };

	 },
    compile: function(element, attrs){
       if (!attrs.width) { attrs.width = '100%'; }
    },

    templateUrl: 'static/js/app/templates/inline-textarea.html'
  }
});