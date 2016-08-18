angular.module('form.controllers', [])
.controller('formCtrl', ['$scope', '$http', '$timeout', function ($scope, $http, $timeout) {
  $scope.params = {};
  $scope.stage = "";
  //$scope.direction = 0;
  $scope.longStage = 0;
  $scope.formValid = false;

  $scope.params = {
    title: "",
    address: "",
    city: "",
    state: "",
    zip_code: "",
    country: "",
    start_date: "",
    end_date: ""
  };

  $scope.next = function (stage) {
    $scope.direction = 1;
    $scope.stage = stage;
    if (stage=="stage4") {
      $scope.longStage = 1;
    }
  };

  $scope.back = function (stage) {
    $scope.direction = 0;
    $scope.stage = stage;
  };


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
    // location.assign("http://127.0.0.1:5000/events/");
    var returnRoute = location.origin + "/events/";
    location.assign(returnRoute);
  }

  function reset() {
    // Clean up scope before destorying
    $scope.params = {};
    $scope.stage = "";

    // Send the app back to a Flask route
    // This method is kind of experimental at the moment.
    $timeout(changeRoute, 1000);
  }
}]);
