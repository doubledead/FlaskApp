angular.module('events.controllers', [])
.controller('eventsCtrl', [
  '$scope',
  '$http',
  '$timeout',
  'EventService',
  function (
    $scope,
    $http,
    $timeout,
    EventService
  ){
    $scope.params = [];
    $scope.formValid = false;
    $scope.rowId = 0;

    var url = location.pathname;

    // This method of calling the service initializes the response
    // as an object in the controller on load.
    // $scope.params = EventService.getEvent();
    // console.log($scope.params);

    // This method initializes the object after everything else loads
    // and makes the object available to routes/views. ng-repeat, etc.
    EventService
      .getEvent()
      .then(function (res) {
        $scope.params = res.data;
        console.log($scope.params);
      });


    $scope.claimItem = function (id) {
      var item;
      for (var i = 0; i < $scope.params.length; i++) {
        if ($scope.params[i].id === id) {
          item = $scope.params[i];
        }
      }

      $http({
        method: 'POST',
        url: '/events/updateitem',
        data: JSON.stringify(item)
      }).then(function successCallback(response) {
        if (response.data && response.data.status === 'OK') {
          console.log('Success.')
        } else if (response.data && response.data.status === 'code:3') {
          console.log('Quantity being claimed exceeds max. Value will remain unchanged.')
        }
        // console.log(response)
      }, function errorCallback(response) {
        console.log(response);
      });
    };

    function changeRoute() {
      var returnRoute = location.origin + '/events/';
      location.assign(returnRoute);
    }

    function reset() {
      // Clean up scope before destorying
      $scope.params = {};
      $scope.stage = '';

      // Send the app back to a Flask route
      // This method is kind of experimental at the moment.
      $timeout(changeRoute, 1000);
    }

}]);
