'use strict';

angular.module('services', [])
  .factory('CreateService', function($http){

    return {
      createEvent: function(data) {

        return $http({
          method: 'POST',
          url: '/events/create',
          data: data
        }).then(function successCallback(response) {
          return response;
        }, function errorCallback(response) {
          console.log(response);
        });
      },
      getMetadata: function(data) {

        return $http({
          method: 'POST',
          url: '/events/get_metadata',
          data: data
        }).then(function successCallback(response) {
          return response;
        }, function errorCallback(response) {
          console.log(response);
        });
      }
    }
  });

