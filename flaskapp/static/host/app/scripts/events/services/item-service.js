'use strict';

angular.module('events.item-service', [])
  .factory('ItemService', function($http){

    return {
      updateItem: function(item) {
        var data = JSON.stringify(item);

        return $http({
          method: 'POST',
          url: '/events/updatehostitem',
          data: data
        }).then(function successCallback(response) {
          return response;
        }, function errorCallback(response) {
          console.log(response);
        });
      },
      updateSubitem: function(payload) {
        var data = JSON.stringify(payload);

        return $http({
          method: 'POST',
          url: '/events/updatesubitem',
          data: data
        }).then(function successCallback(response) {
          return response;
        }, function errorCallback(response) {
          console.log(response);
        });
      },
      addSubitem: function(payload) {
        var data = JSON.stringify(payload);

        return $http({
          method: 'POST',
          url: '/events/addsubitem',
          data: data
        }).then(function successCallback(response) {
          return response;
        }, function errorCallback(response) {
          console.log(response);
        });
      }
    }
  });

