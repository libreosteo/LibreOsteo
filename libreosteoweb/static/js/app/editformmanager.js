
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

/** A generic modal form controller
 *
 * Modal because two modes : read/write, togglable with a button.
 * Toggling to read mode make the save action to be called.
 *
 * Appart the mode toggle, buttons are also offered for acting on visible
 * controlled forms models: reset and delete.
 */
editFormManager.factory('loEditFormManager', function() {
  var forms = [];
  var actions = ['edit', 'cancel', 'save', 'delete'];
  var callback_form = [];
  var triggers_form = [];
  return {
    add: function(form, action_list, trigger) {
      if (forms.indexOf(form) === -1) {
        forms.push(form);
      }
      angular.forEach(action_list, function(action, key) {
        if (action && actions.indexOf(action.name) != -1) {
          var idx_form = forms.indexOf(form);
          var should_add = true;
          var callbacks = null;
          angular.forEach(callback_form, function(value, key) {
            if (value.id == idx_form) {
              should_add = false;
              callbacks = value.callbacks;
            }
          });
          if (should_add) {
            callback_form.push({
              id: forms.indexOf(form),
              callbacks: [action]
            });
          } else {
            callbacks.push(action);
          }
        }
      });
      var idx_form = forms.indexOf(form);
      if (trigger)
        triggers_form[idx_form] = trigger;
    },

    /** Should we show the modal-related buttons
     */
    isAvailable: function() {
      this.available = this._visibleCtrls().length > 0;
      return this.available;
    },
    available: false,
    action_available: function(name_action) {
      return this.action_callbacks(name_action).length > 0 && this.action_trigger(name_action);
    },

    /** Returns a list of callbacks for a given action name

     Each form may or may not expose a callback; callback will be returned if
     the form is currently visible.

     * @param{string} name_action - edit/save/delete/cancel
     * @return{CallBack[]}
     */
    action_callbacks: function(name_action) {
      var form_idx_list = this._visibleCtrls().map(function(el) {
        return forms.indexOf(el);
      });

      var visible_forms = callback_form.filter(function(form) {
        return form_idx_list.includes(form.id);
      });

      return visible_forms.map(function(form) {
        return form.callbacks.find(function(callback) {return callback.name == name_action});
      }).filter(function(i) {return i !== undefined});
    },

    /** Run the named action for all visible forms
     */
    action_trigger: function(name_action) {
      var idx_form = forms.indexOf(this._visibleCtrls());
      var triggers = null;
      var trigger = true;
      angular.forEach(triggers_form, function(value, key) {
        if (key == idx_form) {
          triggers = value;
        }
      });
      if (triggers != null) {
        angular.forEach(triggers, function(value, key) {
          if (key == name_action) {
            if (value != null)
              trigger = value;
          }
        });
      }
      return trigger;
    },
    call_action: function(name) {
      angular.forEach(this.action_callbacks(name), function(callback) {
        callback.callback();
      });
    },
    _visibleCtrls: function() {
      /** Return the visible forms
       */
      return forms.filter(function(el) {
        return $(el).is(':visible');
      });
    }
  };
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
        if ($element.hasClass('ng-dirty')) {
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
        if ($element.hasClass('ng-dirty')) {
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
