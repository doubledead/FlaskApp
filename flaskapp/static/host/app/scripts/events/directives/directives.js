'use strict';

angular.module('events.directives', [])
.directive('itemRow', function () {
  return {
    restrict: 'E',
    templateUrl: 'events/items/item.html',
    scope: {
      item: '=',
      hostId: '='
    },
    link: function (scope, element, attrs) {
      scope.subitemId = 0;

      /*
      scope.$watch('item.quantity_claimed', function () {
        if (scope.item.quantity_claimed === 0) {
          scope.subitemId++;
          var subitemRow = {
            row_id: scope.subitemId,
            quantity: 0,
            user_id: 0
          };
          scope.item.subitems.push(subitemRow);
        } else if (scope.item.subitems.length <= 0) {
          scope.subitemId++;
          var subitemRow = {
            row_id: scope.subitemId,
            quantity: 0,
            user_id: 0
          };

          scope.item.subitems.push(subitemRow);
        }
      });
      */

      scope.$watch('item.subitems', function () {
        for (var i = 0; i < scope.item.subitems.length; i++) {
          var subitem = scope.item.subitems[i];
          if (scope.item.subitems[i].user_id === scope.hostId) {
            console.log('Test1!');
          }
        }
      });

      scope.addSubitemRow = function () {
        scope.subitemId++;

        var subItemRow = {
          row_id: scope.subitemId,
          quantity: 0,
          user_id: 0
        };
        scope.item.subitems.push(subItemRow);
      };
    }
  };
})
.directive('subitemRow', ['SubitemService'], function (SubitemService) {
  return {
    restrict: 'E',
    templateUrl: 'events/subitems/subitem.html',
    scope: {
      subitem: '=',
      hostId: '='
    },
    link: function (scope, element, attrs) {
      scope.updateSubitem = function (subitem) {

      };

    }
  };
})
.directive('subitemView', function () {
  return {
    restrict: 'E',
    templateUrl: 'events/subitems/subitem-view.html',
    scope: {
      subitem: '=',
      hostId: '='
    },
    link: function (scope, element, attrs) {

    }
  };
});
