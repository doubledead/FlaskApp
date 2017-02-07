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

      scope.$watch('item.quantity_claimed', function () {
        if (scope.item.quantity_claimed === 0) {
          console.log("Test");
          // Do some logic here to add an subtract
          // the quantity_claimed from something like
          // called remaining.

          // Get rid of quantity_claimed_new and make it bind
          // to quantity_claimed. Watch for changes in the input
          // and add and subtract difference accordingly.

          // Maybe add in one Subitem by default and check for that
          // on the back-end after submit.
          scope.addSubitemRow = function () {
            scope.subitemId++;

            var subitemRow = {
              row_id: scope.subitemId,
              quantity: 0
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
