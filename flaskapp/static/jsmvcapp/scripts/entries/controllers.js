angular.module('entries.controllers', [])
.controller('entriesCtrl', ['$scope', '$http', '$timeout', function ($scope, $http, $timeout) {
  $scope.params = {};
  $scope.stage = "";
  //$scope.direction = 0;
  $scope.longStage = 0;
  $scope.formValid = false;

  $scope.params = {
    title: "",
    post_date: "",
    tags: [],
    body: ""
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

    if ($scope.entriesForm.$valid) {}

      // jQuery Ajax is used to reach Flask endpoints
      // because AngularJS routes are not used.
      $.ajax({
        cache: false,
        contentType: 'application/json; charset=utf-8',
        accepts: 'application/json',
        url: '/entries/createjs',
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
    location.assign("http://127.0.0.1:5000/entries/");
  }

  function reset() {
    // Clean up scope before destorying
    $scope.params = {};
    $scope.stage = "";

    // Send the app back to a Flask route
    // This method is kind of experimental at the moment.
    $timeout(changeRoute, 1000);
  }

  $scope.addTag = function () {
    var tag = {
      // id: _.uniqueId(),
      description: $scope.tag
    };

    $scope.params.tags.push(tag);

    $scope.tag = "";
  };

}]);
