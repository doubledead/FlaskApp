angular.module('create.directives', [])
.directive('itemRow', function () {
  return {
    restrict: 'E',
    templateUrl: 'items/row.html',
    link: function (scope, element, attrs) {

    }
  };
});
