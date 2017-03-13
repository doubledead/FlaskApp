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
          if (!scope.subitemsFlag) {
            scope.subitemsFlag = true;
          }
          if (!scope.hostSubitemsFlag) {
            scope.hostSubitemsFlag = true;
          } else {
            scope.hostSubitemsFlag = false;
          }
        } else if (scope.item.subitems.length <= 0) {
          if (!scope.subitemsFlag) {
            scope.subitemsFlag = true;
          }
          if (!scope.hostSubitemsFlag) {
            scope.hostSubitemsFlag = true;
          } else {
            scope.hostSubitemsFlag = false;
          }
        }
      });

      // This needs work.
      scope.$watch('item.subitems', function () {
        for (var i = 0; i < scope.item.subitems.length; i++) {
          var subitem = scope.item.subitems[i];
          if (subitem.user_id === scope.hostId) {

          }
          if (subitem.user_id != scope.hostId) {
            if (!scope.hostSubitemsFlag) {
              scope.hostSubitemsFlag = true;
            }
          } else {
            scope.hostSubitemsFlag = false;
          }
        }

        // if ((scope.hostSubitemsList.length <= 0)
        //   && (!scope.hostSubitemsFlag)) {
        //   scope.hostSubitemsFlag = true;
        // }
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

      /*
      scope.addNewHostSubitem = function (quantity) {
        var newHostSubitemRow = {
          row_id: 0,
          quantity: quantity,
          user_id: 0
        };

        scope.item.subitems = [];

        scope.item.subitems.push(newHostSubitemRow);

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
      */
    }
  };
}])
.directive('subitemRow', function () {
  return {
    restrict: 'E',
    templateUrl: 'events/subitems/subitem.html',
    scope: {
      subitem: '=',
      hostId: '='
    },
    link: function (scope, element, attrs) {

    }
  };
});
