
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
var editFormManager = angular.module('loEditFormManager', []);


function Callback(name, callback) {
  this.name = name;
  this.callback = callback;
}

/** Describes an action on one form
 *
 * includes triggers, element (form) and callbacks.
 *
 * @param form: the DOM element (with edit-form-control attr)
 * @param name: the action name (among: edit, save, delete, cancel)
 * @param callbackFunction: the function to be called when the coresponding
 * button is clicked.
 *
 */
function FormAction(form, name, callbackFunction, trigger) {
  this.form = form;
  this.name = name;
  this.callbackFunction = callbackFunction;
  this.trigger = trigger;
}
FormAction.prototype.isAvailable = function() {
  return this.form.is(':visible') && this.trigger[this.name];
};

FormAction.prototype.run = function() {
  this.callbackFunction();
}

/** A generic modal form controller
 *
 * Modal because two modes : read/write, togglable with a button.
 * Toggling to read mode make the save action to be called.
 *
 * Appart the mode toggle, buttons are also offered for acting on visible
 * controlled forms models: reset and delete.
 */
editFormManager.factory('loEditFormManager', function() {
  // This var is global to all loEditFormManager instances
  let formActions =  [];

  return {
    /**
        @param form the DOM element (with edit-form-control attr)
        @param action_list Callback[]
        @param trigger trigger object (ex: {save: true, edit: false, delete: false, cancel: false})
     */
    add: function(form, action_list, trigger) {
      if (formActions.find(x => x.form == form)) {
        console.error('Trying to register already registered form, that is not normal');
        return;
      }
      action_list.forEach(
        x => formActions.push(new FormAction(form, x.name, x.callback, trigger))
      );
      console.warn(`FIXME: Memory leak ; now storing ${formActions.length} actions`);
    },
    action_available: function(name_action) {
      let matchingAction = formActions.find(
        x => x.name === name_action && x.isAvailable()
      );
      return matchingAction != undefined;
    },
    call_action: function(name) {
      let actionsToRun = formActions.filter(
        x => x.name == name && x.isAvailable()
      );
      actionsToRun.forEach(x => x.run());
    }
  }
});

editFormManager.directive('editFormControl', ['$timeout', function($timeout) {
  return {
    restrict: 'A',
    scope: {
      save: "=save",
      trigger: "=trigger",
      edit: "=edit",
      cancel: "=cancel",
      delete: "=delete",
      saveOnLostFocus: "=saveOnLostFocus"
    },
    compile: function(element, attr) {
      if (!attr.save) {
        attr.save = null;
      }
      if (!attr.edit) {
        attr.edit = null;
      }
      if (!attr.cancel) {
        attr.cancel = null;
      }
      if (!attr.delete) {
        attr.delete = null;
      }
      if(!attr.saveOnLostFocus){
        attr.saveOnLostFocus = false;
      }
    },
    controller: ['$scope', '$routeParams', 'loEditFormManager', '$element', function($scope, $routeParams, loEditFormManager, $element) {
      var actions = [];
      if ($scope.save != null) {
        actions.push(new Callback('save', $scope.save));
      }
      if ($scope.edit != null) {
        actions.push(new Callback('edit', $scope.edit));
      }
      if ($scope.cancel != null) {
        actions.push(new Callback('cancel', $scope.cancel));
      }
      if ($scope.delete != null) {
        actions.push(new Callback('delete', $scope.delete));
      }
      $timeout(function() {
        loEditFormManager.add($element, actions, $scope.trigger);
      });

      /**
       * Handle a user attempt to leave a view containing unsaved data
       *
       * May autosave, or prompt user, or let leave.
       *
       * @param {event} event - The event of leaving the view (cancel-able)
       * @param{boolean} askUser - Wether we ask if he really wants to leave
       */
      var quitConfirmationMsg = gettext(
        'There are unsaved changes. Do you really want to leave this page ?'
      );

      function handleUnsavedForm(event, askUser) {
        if ($element.find('.ng-dirty').length > 0) {
          if ($scope.saveOnLostFocus) {
            $scope.save();
            $scope.trigger.save = false;

          } else if (askUser) {
            var quitAnyway = confirm(quitConfirmationMsg);
            if (!quitAnyway) {
              event.preventDefault(); // prevent view change
            }
          }
        }
      }

      // tab change
      $scope.$on('uiTabChange', function(event) {
        // :visible is a hack to figure out if we are current tab.
        if ($element.is(':visible')) {
          handleUnsavedForm(event, false);
        }
      });
      // router view change
      $scope.$on('$locationChangeStart', function(event, newUrl, oldUrl, newState, oldState) {
        if ($element.is(':visible') &&
            // Avoid handling both $locationChangestart and uiTabChange on same click.
            ! (oldUrl.includes('#/patient/') && newUrl.includes('#/patient/'))) {
          handleUnsavedForm(event, true);
        }
      });

      // Window/tab quit or real link click
      //
      // beforeunload is an uncommon event:
      // - on most browsers, confirm() calls within its body will be ignored
      // - on some browsers, you can issue a custom message, but on others
      //   won't accept it (in favor of built-in message)
      // - it is hard to get sure an AJAX call is made (for autosave)
      // - API depend on browser
      //
      // https://developer.mozilla.org/en-US/docs/Web/Events/beforeunload
      //
      // So, best-effort: we ask for confirmation, optionaly with custom
      // message.
      function onQuit(event) {
        if ($element.find('.ng-dirty').length > 0) {
          event.returnValue = quitConfirmationMsg;
          return quitConfirmationMsg;
        }
      };
      window.addEventListener('beforeunload', onQuit);
      $scope.$on('$destroy', function() {
        window.removeEventListener('beforeunload', onQuit);
      });
    }],
  }
}]);

editFormManager.directive('disableEnter', ['$compile', function($compile) {
  return {
    restrict: 'A',
    replace : false,
    terminal : true,
    priority: 1001,
    compile: function compile(element, attrs) {
      element.removeAttr('disable-enter');
      element.attr('ng-keypress', 'disableEnter($event)');
      return {
        pre : function preLink(scope, iElement, iAttrs, controller) { },
        post : function postLink(scope, iElement, iAttrs, controller) {
          $compile(iElement)(scope);
        }
      };
    },
    controller: ["$scope", function($scope, $element) {
      $scope.disableEnter = function(event) {
        if (event.target.contentEditable != "true" && (event.charCode || event.keyCode) == 13) {
          event.preventDefault();
        };
      };
    }],
  }
}]);


var getStackTrace = function() {
  var obj = {};
  Error.captureStackTrace(obj, getStackTrace);
  return obj.stack;
};
