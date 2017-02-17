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

    EventService
      .getItems()
      .then(function (response) {
        $scope.params = response.data;
        // $scope.carbon = response.data;
      });

    $scope.removeItem = function (id) {

      EventService
        .removeItem(id)
        .then(function (response) {
          if (response.data && response.data.status === "OK") {
            // $scope.params = response.data;
            console.log("removeItem: OK!");
          } else if (response.data && response.data.status === "Error") {
            // scope.stage = "Error";
            console.log("removeItem: Error!");
          }
        });
    };

    $scope.claimItems = function () {
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
          // $scope.carbon = response.data;
        });
    }

}]);
