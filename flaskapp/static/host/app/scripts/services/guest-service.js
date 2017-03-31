'use strict';

angular.module('guest-service', [])
  .factory('GuestService', function($http){

    return {
      updateGuest: function(item) {
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
      addGuest: function(payload) {
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


