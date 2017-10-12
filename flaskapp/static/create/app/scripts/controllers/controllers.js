angular.module('controllers', [])
.controller('formCtrl', ['$scope', '$http', '$timeout', 'CreateService', function ($scope, $http, $timeout, CreateService) {
  $scope.params = {};
  $scope.stage = '';
  //$scope.direction = 0;
  $scope.longStage = 0;
  $scope.formValid = false;
  $scope.rowId = 0;
  $scope.itemId = 0;
  $scope.toggleEventObjView = false;

  $scope.params = {
    address: '',
    address_line_two: '',
    category_id: 100,
    city: '',
    country: '',
    description: '',
    end_date: '',
    guestEmail: '',
    guests: [],
    items: [],
    itemName: '',
    itemQuantity: '',
    name: '',
    start_date: '',
    state: '',
    zip_code: ''
  };

  // Navigation functions
  $scope.next = function (stage) {
    $scope.direction = 1;
    $scope.stage = stage;
    if (stage=='stage5') {
      $scope.longStage = 1;
    }
  };

  $scope.back = function (stage) {
    $scope.direction = 0;
    $scope.stage = stage;
  };

  // Form submission functions
  $scope.submitForm = function () {
    $scope.direction = 1;
    $scope.stage = "loading";

    var
      deferred = $.Deferred(),
      data = JSON.stringify($scope.params);

    if ($scope.baseForm.$valid) {}

    // jQuery Ajax is used to reach Flask endpoints
    // because AngularJS routes are not used.
    // $.ajax({
    //   cache: false,
    //   contentType: 'application/json; charset=utf-8',
    //   accepts: 'application/json',
    //   url: '/events/create',
    //   data: data,
    //   dataType: 'json',
    //   type: 'POST'
    // }).success(function(response) {
    //   deferred.resolve(response);
    //   console.log(response);
    //   $scope.$apply(reset());
    // }).fail(function(response) {
    //
    // }).done(function(response) {
    //
    // });
    // return deferred.promise();
    CreateService
      .createEvent(data)
      .then(function (response) {
        if (response.data
          && (response.data.status === 'OK')) {
          $scope.direction = 1;
          $scope.stage = 'success';
          $scope.reset();
        } else if (response.data
          && (response.data.status === 'Error')) {
          $scope.direction = 1;
          $scope.stage = 'error';
          console.log('Create Event: Error!');
        }
      });
  };

  function changeRoute() {
    var returnRoute = location.origin + '/events/';
    location.assign(returnRoute);
  }

  $scope.reset = function () {
    // Clean up scope before destroying
    $scope.params = {};

    // Send the app back to a Flask route
    // This method is kind of experimental at the moment.
    $timeout(changeRoute, 1000);
  };

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

  $scope.addItemRow = function () {
    $scope.itemId++;

    var itemRow = {
      row_id: $scope.itemId,
      category_id: 0,
      name: "",
      quantity: 0
    };

    $scope.params.items.push(itemRow);
  };
  /* Add one default Item row */
  $scope.addItemRow();

  $scope.addItem = function () {
    $scope.itemId++;
    var itemName = $scope.params.itemName;
    var itemQuantity = $scope.params.itemQuantity;

    var item = {
      itemId: $scope.itemId,
      category_id: 100,
      name: itemName,
      quantity: itemQuantity
    };

    $scope.params.items.push(item);

    $scope.params.itemName = '';
    $scope.params.itemQuantity = '';
  };

  $scope.removeItem = function (row_id) {
    for (var i = 0; i < $scope.params.items.length; i++) {
      if ($scope.params.items[i].row_id === row_id) {
        $scope.params.items.splice(i, 1);
        break;
      }
    }
  };

  // AngularJS Datetimepicker
  $scope.endDateBeforeRender = endDateBeforeRender;
  $scope.endDateOnSetTime = endDateOnSetTime;
  $scope.startDateBeforeRender = startDateBeforeRender;
  $scope.startDateOnSetTime = startDateOnSetTime;

  function startDateOnSetTime () {
    $scope.$broadcast('start-date-changed');
  }

  function endDateOnSetTime () {
    $scope.$broadcast('end-date-changed');
  }

  function startDateBeforeRender ($dates) {
    if ($scope.params.end_date) {
      var activeDate = moment($scope.params.end_date);

      $dates.filter(function (date) {
        return date.localDateValue() >= activeDate.valueOf()
      }).forEach(function (date) {
        date.selectable = false;
      })
    }
  }

  function endDateBeforeRender ($view, $dates) {
    if ($scope.params.start_date) {
      var activeDate = moment($scope.params.start_date).subtract(1, $view).add(1, 'minute');

      $dates.filter(function (date) {
        return date.localDateValue() <= activeDate.valueOf()
      }).forEach(function (date) {
        date.selectable = false;
      })
    }
  }

}]);
