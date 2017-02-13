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
        if (response.data && response.data.status === "OK") {
          $scope.params = response.data;
          $scope.carbon = response.data;
          console.log("getItems: OK!");
        } else if (response.data && response.data.status === "Error") {
          $scope.stage = "Error";
          console.log("Error");
          // Get last data from local storage
          // $scope.params = $scope.carbon;
        }
        // $scope.params = response.data;
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


      var items = JSON.stringify($scope.params.items_data);

      $http({
        method: 'POST',
        url: '/events/updateitems',
        data: items
      }).then(function successCallback(response) {
        if (response.data && response.data.status === 'OK') {
          console.log('Success.');
          reset();
        } else if (response.data && response.data.status === 'Error') {
          console.log("Error");
          $scope.stage = "error"
        }
        // console.log(response)
      }, function errorCallback(response) {
        if (response.data && response.data.status === 'Error') {
          console.log('Error.');
          // reset();
        }
        console.log(response);
      });
    };

    function changeRoute() {
      var returnRoute = location.origin + '/events/';
      location.assign(location.href);
    }

    function reset() {
      // Clean up scope before destroying
      $scope.params = {};
      $scope.carbon = {};
      EventService
        .getItems()
        .then(function (response) {
          $scope.params = response.data;
          $scope.carbon = response.data;
        });
    }

}]);
