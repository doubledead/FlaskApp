'use strict';

angular.module('events.directives', [])
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
      scope.hostSubitemsFlag = false;

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

      scope.$watch('item.quantity_claimed', function () {
        if (scope.item.quantity_claimed === 0) {
          console.log('No items claimed!');
          if (!scope.subitemsFlag) {
            scope.subitemsFlag = true;
          }
          console.log(scope.subitemsFlag);

        } else if (scope.item.subitems.length <= 0) {
          console.log('No items claimed!');
          if (!scope.subitemsFlag) {
            scope.subitemsFlag = true;
          }
          console.log(scope.subitemsFlag);
        }
      });

      // This needs work.
      scope.$watch('item.subitems', function () {
        for (var i = 0; i < scope.item.subitems.length; i++) {
          var subitem = scope.item.subitems[i];
          if (subitem.user_id === scope.hostId) {
            console.log('Test1!');
          } else {
            if (subitem.user_id != scope.hostId
              && (!scope.hostSubitemsFlag)) {
              // scope.hostSubitemsFlag = true;
            }
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

      scope.updateItem = function () {
        ItemService
          .updateItem(scope.item)
          .then(function (response) {
            if (response.data && response.data.status === 'OK') {
              console.log('updateitem: OK!');
            } else if (response.data && response.data.status === 'Error') {
              console.log('removeItem: Error!');
            }
          });
      };
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
      hostSubitemsFlag: '=',
      subitemsFlag: '='
    },
    link: function (scope, element, attrs) {

    }
  };
});
