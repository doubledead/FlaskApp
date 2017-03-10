'use strict';

angular.module('events.subitem-service', [])
  .factory('SubitemService', function($http){

    return {
      removeItem: function(itemId) {
        var data = {
          paramId: itemId
        };

        return $http({
          method: 'POST',
          url: '/events/removeitem',
          data: JSON.stringify(data)
        }).then(function successCallback(response) {
          return response;
        }, function errorCallback(response) {
          console.log(response);
        });
      },
      updateItems: function(items_data) {
        var data = JSON.stringify(items_data);

        return $http({
          method: 'POST',
          url: '/events/updateitems',
          data: data
        }).then(function successCallback(response) {
          return response;
        }, function errorCallback(response) {
          console.log(response);
        });
      }
    }
  });

