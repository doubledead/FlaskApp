angular.module('form.controllers', [])
.controller('formCtrl', ['$scope', '$http', '$timeout', function ($scope, $http, $timeout) {
  $scope.params = {};
  $scope.stage = '';
  //$scope.direction = 0;
  $scope.longStage = 0;
  $scope.formValid = false;
  $scope.rowId = 0;

  $scope.params = {
    address: '',
    address_line_two: '',
    category: 'event',
    city: '',
    country: '',
    end_date: '',
    guestEmail: '',
    guests: [],
    items: [],
    itemName: '',
    itemQuantity: '',
    name: '',
    start_date: '',
    state: '',
    zip_code: '',
  };

  // Navigation functions
  $scope.next = function (stage) {
    $scope.direction = 1;
    $scope.stage = stage;
    if (stage=='stage6') {
      $scope.longStage = 1;
    }
  };

  $scope.back = function (stage) {
    $scope.direction = 0;
    $scope.stage = stage;
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

  // Guest item functions
  $scope.addGuestEmail = function () {
    $scope.rowId++;
    var guestEmail = $scope.params.guestEmail;

    var guest = {
      email: guestEmail,
      row_id: $scope.rowId
    };

    $scope.params.guests.push(guest);

    $scope.params.guestEmail = '';
  };

  $scope.removeGuestEmail = function (row_id) {
    for (var i = 0; i < $scope.params.guests.length; i++) {
      if ($scope.params.guests[i].row_id === row_id) {
        $scope.params.guests.splice(i, 1);
        break;
      }
    }
  };

  // Item functions
  $scope.addItem = function () {
    $scope.itemId++;
    var itemName = $scope.params.itemName;
    var itemQuantity = $scope.params.itemQuantity;

    var item = {
      itemId: $scope.itemId,
      category: 100,
      name: itemName,
      quantity: itemQuantity
    };

    $scope.params.items.push(item);

    $scope.params.itemName = '';
    $scope.params.itemQuantity = '';
  };

  $scope.removeItem = function (itemId) {
    for (var i = 0; i < $scope.params.items.length; i++) {
      if ($scope.params.items[i].itemId === itemId) {
        $scope.params.items.splice(i, 1);
        break;
      }
    }
  };

}]);
