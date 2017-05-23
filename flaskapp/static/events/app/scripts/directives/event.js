angular.module('event', [])
  .directive('eventRow', ['$http', function ($http) {
    return {
      restrict: 'E',
      templateUrl: 'events/event.html',
      scope: {
        event: '='
      },
      link: function (scope, element, attrs) {
        scope.subitemId = 0;

        scope.$watch('event', function () {

        });

        scope.claimItems = function () {
          var items = JSON.stringify(scope.event.items_data);

          $http({
            method: 'POST',
            url: '/events/updateitems',
            data: items
          }).then(function successCallback(response) {
            if (response.data && response.data.status === 'OK') {
              console.log('Success.')
              // reset();
            } else if (response.data && response.data.status === 'code:3') {
              console.log('Quantity being claimed exceeds max. Value will remain unchanged.')
            }
            // console.log(response)
          }, function errorCallback(response) {
            if (response.data && response.data.status === 'Error') {
              console.log('Error.')
              // reset();
            }
            console.log(response);
          });
        };


      }
    };
  }]);
