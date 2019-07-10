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
