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
    // console.log($scope.params);


    $scope.testParams = function () {
      // console.log($scope.params);
      // for (var i = 0; i < $scope.params.length; i++) {
      //   console.log($scope.params[i].name);
      // }
      var url = location.pathname;

      var paramId = url.split("/events/", 2)[1];

      var data = {
        id: paramId
      };

      // console.log(url.split("/events/", 2)[1]);

      $http({
        method: 'POST',
        url: url,
        data: JSON.stringify(data)
      }).then(function successCallback(response) {
        if (response && response.data) {
          // console.log(response.data)
          console.log(response)
        }
      }, function errorCallback(response) {
        console.log(response);
      });

    };

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
        }
        console.log(response)
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
