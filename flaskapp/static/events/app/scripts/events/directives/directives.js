angular.module('events.directives', [])
.directive('itemRow', function () {
  return {
    restrict: 'E',
    templateUrl: 'events/items/item.html',
    scope: {
      item: '='
    },
    link: function (scope, element, attrs) {
      scope.subitemId = 0;

      // Insert blank Subitem row as placeholder if conditions
      scope.$watch('item.quantity_claimed', function () {
        if (scope.item.quantity_claimed === 0) {
          // console.log("Test");
          // Do some logic here to add and subtract
          // the quantity_claimed from something like
          // called remaining. Watch for changes in the
          // input and add and subtract difference accordingly.

          scope.addSubitemRow = function () {
            scope.subitemId++;

            var subitemRow = {
              row_id: scope.subitemId,
              quantity: 0,
              user_id: 0
            };

            scope.item.subitems.push(subitemRow);
          };
          scope.addSubitemRow();
        } else if (scope.item.subitems.length <= 0) {
          scope.addSubitemRow = function () {
            scope.subitemId++;

            var subitemRow = {
              row_id: scope.subitemId,
              quantity: 0,
              user_id: 0
            };

            scope.item.subitems.push(subitemRow);
          };
          scope.addSubitemRow();
        }
      });


    }
  };
})
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
});
