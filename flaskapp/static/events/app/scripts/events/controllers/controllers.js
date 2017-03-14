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
    $scope.carbon = [];
    $scope.formValid = false;
    $scope.rowId = 0;
    $scope.stage = 0;
    $scope.toggleEventObjView = false;

    // This method of calling the service initializes the response
    // as an object in the controller on load.
    // $scope.params = EventService.getEvent();
    // console.log($scope.params);

    // This method initializes the object after everything else loads
    // and makes the object available to routes/views. ng-repeat, etc.
    EventService
      .getItems()
      .then(function (response) {
        $scope.params = response.data;
        // $scope.carbon = response.data;
      });


    $scope.claimItem = function (id) {
      var item;

      // Iterate through params.event_data to find Item object
      for (var i = 0; i < $scope.params.items_data.length; i++) {
        if ($scope.params.items_data[i].id === id) {
          item = $scope.params.items_data[i];
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

    $scope.claimItems = function () {
      // Validation
      // Maybe make a copy and validate on client side before
      // even hitting the DB to save a service call.

      // Maybe store copy in local storage and dump it on
      // change/submit.

      EventService
        .updateItems($scope.params.items_data)
        .then(function (response) {
          if (response.data && response.data.status === "OK") {
            console.log("updateitems: OK!");
            $scope.reset();
          } else if (response.data && response.data.status === "Error") {
            $scope.direction = 1;
            $scope.stage = "error";
            console.log("removeItem: Error!");
          }
        });
    };

    function changeRoute() {
      var returnRoute = location.origin + '/events/';
      location.assign(location.href);
    }

    $scope.reset = function () {
      // Clean up scope before destroying
      $scope.params = {};
      // $scope.carbon = {};
      EventService
        .getItems()
        .then(function (response) {
          $scope.params = response.data;
          // $scope.carbon = response.data;
        });
    }

}]);
