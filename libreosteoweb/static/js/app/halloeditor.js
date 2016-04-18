var directives = angular.module('loHalloEditor', []);

directives.directive('halloEditor', [ '$sce', function($sce) {
  return {
    restrict: 'A',
    require: '?ngModel',
    scope: {
      isEditable: '=',
      placeholder: '=',
    },
    link: function(scope, element, attrs, ngModel) {
      if (!ngModel) {
        return;
      }

      // Monkey patch hallo.js enable function
      var enableOriginal = $.IKS.hallo.prototype.enable;
      $.IKS.hallo.prototype.enable = function()
      {
        enableOriginal.apply(this);
        this.element.css({'min-height':34});
      };

      ngModel.$render = function() { 
        if(!scope.isEditable){
          if ( ngModel.$viewValue == '') {
            element.empty();
            element.removeClass('inEditMode');
            element.removeClass('inPlaceholderMode');
          } else {
            element.html($sce.getTrustedHtml(ngModel.$viewValue));
            element.removeClass('inPlaceholderMode');
          }
        } else {
          element.html($sce.getTrustedHtml(ngModel.$viewValue || scope.placeholder));
          if(ngModel.$viewValue)
          {
            element.removeClass('inPlaceholderMode');
            element.addClass('inEditMode');
          } else {
            element.addClass('inPlaceholderMode');
            element.removeClass('inEditMode');
          }
        }
      };

      $(element).hallo({
        plugins: {
          'halloformat': {
            "formattings": {
              "bold": true,
              "italic": true,
              "strikethrough": true,
              "underline": true
            }
          },
          'halloheadings': [1, 2, 3],
          'hallojustify': {},
          'hallolists': {
            "lists": {
              "ordered": true,
              "unordered": true
            }
          },
          //'halloreundo': {},
          'halloblock': {},
        },
        toolbar: 'halloToolbarFixed',
        //parentElement : '#toolbarHolder'
        placeholder: scope.placeholder,
      });


      scope.$watch('isEditable', function(newValue, oldValue) {
        $(element).hallo({
          editable: newValue
        });

        if(element.html() === scope.placeholder && !newValue)
        {
          element.empty();
        }

        if(newValue)
        {
          element.addClass('form-control readyForEditMode');
        } else {
          element.removeClass('form-control readyForEditMode');
        }
      });

      function read() {
        console.log("ngModel "+angular.toJson(ngModel));
        var html = element.html();
        if ( html == '<br>' || html == '<br/>' || element == '') {
          element.empty();
        }
        if(html === scope.placeholder){
          element.empty();
        }
        ngModel.$setViewValue(element.html());
      }

      $(element).on('hallodeactivated', read);

    }
  };
}]);