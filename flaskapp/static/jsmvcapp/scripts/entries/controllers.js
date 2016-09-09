angular.module('entries.controllers', [])
.controller('entriesCtrl', ['$scope', '$http', '$timeout', function ($scope, $http, $timeout) {
  $scope.params = {};
  //$scope.direction = 0;
  $scope.formValid = false;

  $scope.params = {
    title: "",
    post_date: "",
    tags: [],
    body: ""
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
    // location.assign("http://127.0.0.1:5000/entries/");
    var returnRoute = location.origin + "/entries/";
    location.assign(returnRoute);
  }

  function reset() {
    // Clean up scope before destorying
    $scope.params = {};

    // Send the app back to a Flask route
    // This method is kind of experimental at the moment.
    $timeout(changeRoute, 1000);
  }

  $scope.addTag = function () {
    var d = $scope.tag;
    // var id = _.uniqueId();
    var tag = {
      category: "social",
      description: d
    };

    $scope.params.tags.push(tag);

    $scope.tag = "";
  };

}]);
