'use strict';

angular.module('events.directives', [])
.directive('itemRow', ['ItemService', function (ItemService) {
  return {
    restrict: 'E',
    templateUrl: 'events/items/item.html',
    scope: {
      item: '=',
      hostId: '=',
      hostSubitem: '='
    },
    link: function (scope, element, attrs) {
      scope.subitemId = 0;
      scope.subitemsFlag = false;

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

      /*
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
      subitem: '='
    },
    link: function (scope, element, attrs) {

    }
  };
})
.directive('hostSubitem', function () {
  return {
    restrict: 'E',
    templateUrl: 'events/subitems/host-subitem.html',
    scope: {
      subitem: '=',
      hostId: '=',
      itemId: '='
    },
    link: function (scope, element, attrs) {

    }
  };
});
