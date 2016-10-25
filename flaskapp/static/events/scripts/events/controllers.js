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
    $scope.params = {};
    $scope.formValid = false;
    $scope.rowId = 0;

    var url = location.pathname;

    // $http({
    //   method: 'POST',
    //   url: url
    // }).then(function successCallback(response) {
    //   if (response && response.data) {
    //     console.log(response.data)
    //     $scope.params = response.data;
    //   } else {
    //     if (response && response.data) {
    //       console.log(response)
    //     }
    //   }
    // }, function errorCallback(response) {
    //   console.log(response);
    // });

    $scope.params = EventService.getEvent();
    console.log($scope.params);


    $scope.testParams = function () {
      // console.log($scope.params);
      // for (var i = 0; i < $scope.params.length; i++) {
      //   console.log($scope.params[i].name);
      // }
      var
        deferred = $.Deferred(),
        url = location.pathname;

      var paramId = url.split("/events/", 2)[1];

      var data = {
        id: paramId
      };

      // console.log(url.split("/events/", 2)[1]);

      $http({
        method: 'POST',
        url: '/events/gettest',
        data: JSON.stringify(data)
      }).then(function successCallback(response) {
        if (response && response.data) {
          // console.log(response.data)
          console.log(response)
        }
      }, function errorCallback(response) {
        console.log(response);
      });

      // $.ajax({
      //   cache: false,
      //   contentType: 'application/json; charset=utf-8',
      //   accepts: 'application/json',
      //   url: '/events/gettest',
      //   data: JSON.stringify(data),
      //   method: 'POST'
      // }).success(function(response) {
      //   deferred.resolve(response);
      //   console.log(response);
      //   console.log("Success");
      //
      // }).fail(function(response) {
      //   console.log(response);
      //   console.log("Fail");
      // }).done(function(response) {
      //
      // });

    };

    function changeRoute() {
      var returnRoute = location.origin + "/events/";
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
