'use strict';

angular.module('guest-service', [])
  .factory('GuestService', function($http){

    return {
      addGuest: function(payload) {

        return $http({
          method: 'POST',
          url: '/events/add_guest',
          data: JSON.stringify(payload)
        }).then(function successCallback(response) {
          return response;
        }, function errorCallback(response) {
          console.log(response);
          return response;
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
          return response;
        });
      }
    }
  });


