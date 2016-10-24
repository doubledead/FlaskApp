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
      for (var i = 0; i < $scope.params.length; i++) {
        console.log($scope.params[i].name);
      }
    };

    // Form submission functions
    $scope.submitForm = function () {
      var
        deferred = $.Deferred(),
        data = JSON.stringify($scope.params);

      if ($scope.baseForm.$valid) {}

        // jQuery Ajax is used to reach Flask endpoints
        // because AngularJS routes are not used.
        $.ajax({
          cache: false,
          contentType: 'application/json; charset=utf-8',
          accepts: 'application/json',
          url: '/events/create',
          data: data,
          dataType: 'json',
          type: 'POST'
        }).success(function(response) {
          deferred.resolve(response);
          console.log(response);
          $scope.$apply(reset());
        }).fail(function(response) {

        }).done(function(response) {

        });
        return deferred.promise();
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
