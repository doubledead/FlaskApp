angular.module('events.controllers', [])
.controller('formCtrl', ['$scope', '$http', '$timeout', function ($scope, $http, $timeout) {
  $scope.params = [];
  $scope.formValid = false;
  $scope.rowId = 0;

  var url = location.pathname;
  var deferred = $.Deferred();

  // function ajaxCall($scope) {
  //   $.ajax({
  //     cache: false,
  //     contentType: 'application/json; charset=utf-8',
  //     accepts: 'application/json',
  //     url: url,
  //     method: 'POST'
  //   }).success(function(response) {
  //     deferred.resolve(response);
  //     // console.log(response);
  //     console.log("Success");
  //     responseParams = JSON.parse(response);
  //     $scope.$apply(function () {
  //       $scope.params = responseParams;
  //     });
  //
  //   }).fail(function(response) {
  //     deferred.reject(response)
  //     console.log(response);
  //     console.log("Fail");
  //   }).done(function(response) {
  //
  //   });
  // }

  // ajaxCall($scope);

  $http({
    method: 'POST',
    url: url
  }).then(function successCallback(response) {
    if (response && response.data) {
      console.log(response.data)
      $scope.params = JSON.stringify(response.data);
    } else {
      if (response && response.data) {
        console.log(response)
      }
    }
  }, function errorCallback(response) {
    console.log(response);
  });

  $scope.testParams = function () {
    console.log($scope.params);
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
