'use strict';

angular.module('directives', [])
.directive('itemRow', ['ItemService', function (ItemService) {
  return {
    restrict: 'E',
    templateUrl: 'events/items/item.html',
    scope: {
      item: '=',
      hostId: '='
    },
    link: function (scope, element, attrs) {
      scope.subitemId = 0;
      scope.subitemsFlag = false;
      scope.hostSubitemsFlag = true;

      scope.$watch('item.quantity_claimed', function () {
        if (scope.item.quantity_claimed === 0) {
          if (!scope.subitemsFlag) {
            scope.subitemsFlag = true;
          }
        } else if (scope.item.subitems.length <= 0) {
          if (!scope.subitemsFlag) {
            scope.subitemsFlag = true;
          }
        }
      });

      scope.$watch('item.subitems', function () {
        for (var i = 0; i < scope.item.subitems.length; i++) {
          var subitem = scope.item.subitems[i];
          if (subitem.user_id === scope.hostId) {
            scope.hostSubitemsFlag = false;
            break
          }
        }
      });
    }
  };
}])
.directive('subitemRow', function () {
  return {
    restrict: 'E',
    templateUrl: 'events/subitems/subitem.html',
    scope: {
      subitem: '=',
      hostId: '=',
      itemId: '='
    },
    link: function (scope, element, attrs) {

    }
  };
});
