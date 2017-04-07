angular.module('guest', [])
.directive('guestRow', ['$http', 'GuestService', function ($http, GuestService) {
  return {
    restrict: 'E',
    templateUrl: 'events/guests/guest.html',
    scope: {
      guest: '=',
      toggleEdit: '=',
      toggleRemove: '='
    },
    link: function (scope, element, attrs) {
      scope.toggleEdit = false;
      scope.toggleRemove = false;

      scope.removeGuest = function () {

      };

    }
  };
}]);
