angular.module('guest', [])
.directive('guestRow', ['$http', 'GuestService', function ($http, GuestService) {
  return {
    restrict: 'E',
    templateUrl: 'events/guests/guest.html',
    scope: {
      guest: '=',
      hostId: '=',
      toggleEdit: '=',
      toggleRemove: '='
    },
    link: function (scope, element, attrs) {
      scope.toggleEdit = false;
      scope.toggleRemove = false;

      var payload = {
        g_id: scope.guest.id,
        u_id: scope.hostId
      };

      scope.removeGuest = function () {
        GuestService
          .removeGuest(payload)
          .then(function (response) {
            if (response.data && response.data.status === 'OK') {
              console.log('Guest removed!');
            } else {
              console.log('Error removing guest!');
            }
          });
      };

    }
  };
}]);
