'use strict';

angular.module('events.controllers', [])
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

    $scope.updateHostSubitem = function (subitem, itemId, hostId) {
      var payload = {
        'item_id': itemId,
        'host_id': hostId,
        'subitem': subitem
      };

      ItemService
        .updateHostSubitem(payload)
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

    $scope.addNewHostSubitem = function (itemId, quantity) {
      console.log('Testing!!');
      var item;

      for (var i = 0; i < $scope.params.items_data.length; i++) {
        if ($scope.params.items_data[i].id = itemId) {
          item = $scope.params.items_data[i];
        }
      }

      var newHostSubitemRow = {
        row_id: 0,
        quantity: quantity,
        user_id: 0
      };

      item.subitems = [];

      item.subitems.push(newHostSubitemRow);

      ItemService
        .updateItem(item)
        .then(function (response) {
          if (response.data
            && (response.data.status === 'OK')) {
            console.log('updateitem: OK!');
            $scope.reset();
          } else if (response.data
            && (response.data.status === 'Error')) {
            console.log('removeItem: Error!');
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
