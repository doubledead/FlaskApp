'use strict';

angular.module('controllers', [])
.controller('eventsCtrl', [
  '$scope',
  '$http',
  '$timeout',
  'EventService',
  'ItemService',
  function (
    $scope,
    $http,
    $timeout,
    EventService,
    ItemService
  ){
    $scope.params = [];
    $scope.carbon = [];
    $scope.formValid = false;
    $scope.rowId = 0;
    $scope.stage = '';
    $scope.longStage = 0;
    $scope.toggleEventObjView = false;

    EventService
      .getItems()
      .then(function (response) {
        $scope.params = response.data;
        // $scope.carbon = response.data;
      });

    $scope.removeItem = function (id) {
      $scope.direction = 1;
      $scope.stage = 'loading';

      EventService
        .removeItem(id)
        .then(function (response) {
          if (response.data
            && (response.data.status === 'OK')) {
            console.log('removeItem: OK!');
            $scope.reset();
          } else if (response.data
            && (response.data.status === 'Error')) {
            $scope.direction = 1;
            $scope.stage = 'error';
            console.log('removeItem: Error!');
          }
        });
    };

    $scope.claimItems = function () {
      var items = JSON.stringify($scope.params.items_data);
      $scope.direction = 1;
      $scope.stage = 'loading';
      $scope.longStage = 1;

      EventService
        .updateItems($scope.params.items_data)
        .then(function (response) {
          if (response.data && response.data.status === 'OK') {
            console.log('claimItems: OK!');
            $scope.reset();
          } else if (response.data && response.data.status === 'Error') {
            $scope.direction = 1;
            $scope.stage = 'error';
            console.log('claimItems: Error!');
          }
        });
    };

    $scope.updateItem = function (item) {
      ItemService
        .updateItem(item)
        .then(function (response) {
          if (response.data && response.data.status === "OK") {
            console.log("updateitem: OK!");
            $scope.reset();
          } else if (response.data && response.data.status === "Error") {
            $scope.direction = 1;
            $scope.stage = "error";
            console.log("removeItem: Error!");
          }
        });
    };

    $scope.updateSubitem = function (subitem, itemId, hostId) {
      $scope.direction = 1;
      $scope.stage = 'loading';
      var payload = {
        'item_id': itemId,
        'host_id': hostId,
        'subitem': subitem
      };

      ItemService
        .updateSubitem(payload)
        .then(function (response) {
          if (response.data
            && (response.data.status === 'OK')) {
            console.log('updateHostItem: OK!');
            $scope.reset();
          } else if (response.data
            && (response.data.status === 'Error')) {
            // $scope.direction = 1;
            // $scope.stage = 'error';
            console.log('updateHostItem: Error!');
          }
        });
    };

    $scope.addSubitem = function (subitem, itemId) {
      $scope.direction = 1;
      $scope.stage = 'loading';
      var payload = {
        'item_id': itemId,
        'subitem': subitem
      };

      ItemService
        .addSubitem(payload)
        .then(function (response) {
          if (response.data
            && (response.data.status === 'OK')) {
            console.log('addSubitem: OK!');
            $scope.reset();
          } else if (response.data
            && (response.data.status === 'Error')) {
            // $scope.direction = 1;
            // $scope.stage = 'error';
            console.log('addSubitem: Error!');
          }
        });
    };

    function changeRoute() {
      var returnRoute = location.origin + '/events/';
      location.assign(location.href);
    }

    $scope.reset = function () {
      // Clean up scope before destroying
      $scope.params = {};
      // $scope.carbon = {};
      EventService
        .getItems()
        .then(function (response) {
          $scope.params = response.data;
          // $scope.carbon = response.data;
        });
      $scope.direction = 1;
      $scope.stage = '';
      $scope.longStage = 0;
    };

}]);
