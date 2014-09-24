var inlineEdit = angular.module('loInlineEdit', []);
// Define the directive
inlineEdit.directive('inlineedit', function() {
  return {
    restrict: 'E',
    //transclude : true,
    scope: {
        model : '=',
        property: '@',
        onSave : '&',
        placeholder : '@',
        editclass : '@',
        width: '@',
        readOnly : '=',
	},
    controller: function($scope)
    {
        "use strict";
        $scope.displayButton = false;

        $scope.saveModel = function() {
          $scope.onSave();
        };
    },
      compile: function(element, attrs){
          if (!attrs.width) { attrs.width = '100%'; }
          if (!attrs.readOnly) { attrs.readOnly = false; }

    },

    templateUrl: 'static/js/app/templates/inline-edit.html'
  }
});

inlineEdit.directive('inlinetel', function() {
  return {
    restrict: 'E',
    //transclude : true,
    scope: {
        model : '=',
        property: '@',
        onSave : '&',
        placeholder : '@',
        editclass : '@',
        width: '@',
        icon : '@',
        readOnly : '=',
	},
    controller: function($scope)
    {
        "use strict";
        $scope.displayButton = false;

        $scope.saveModel = function() {
          $scope.onSave();
        };
    },
    compile: function(element, attrs){
       if (!attrs.width) { attrs.width = '100%'; }
       if (!attrs.readOnly) { attrs.readOnly = false; }
    },

    templateUrl: 'static/js/app/templates/inline-tel.html'
  }
});



inlineEdit.directive('inlinetextarea', function() {
  return {
    restrict: 'E',
    //transclude : true,
    scope: {
        model : '=',
        property: '@',
        onSave : '&',
        placeholder : '@',
        editclass : '@',
        width: '@',
        row : '@',
        col : '@',
        readOnly : '=',
	},
    controller: function($scope)
    {
        "use strict";
        $scope.displayButton = false;

        $scope.saveModel = function() {
          $scope.onSave();
        };
    },
    compile: function(element, attrs){
       if (!attrs.width) { attrs.width = '100%'; }
       if (!attrs.readOnly) { attrs.readOnly = false; }
    },

    templateUrl: 'static/js/app/templates/inline-textarea.html'
  }
});