'use strict';

angular.module('guest-service', [])
  .factory('GuestService', function($http){

    return {
      updateGuest: function(item) {
        var data = JSON.stringify(item);

        return $http({
          method: 'POST',
          url: '/events/update_guest',
          data: data
        }).then(function successCallback(response) {
          return response;
        }, function errorCallback(response) {
          console.log(response);
        });
      },
      removeGuest: function(payload) {
        // var data = JSON.stringify(payload);

        return $http({
          method: 'POST',
          url: '/events/remove_guest',
          // data: data
          data: JSON.stringify(payload)
        }).then(function successCallback(response) {
          return response;
        }, function errorCallback(response) {
          console.log(response);
        });
      }
    }
  });


