angular.module('events.services', [])
  .factory('EventService', function($http){

      return {
        getEvent: function() {
          var url = location.pathname;

          return $http({
            method: 'POST',
            url: url
          }).then(function successCallback(response) {
            return response.data;
          }, function errorCallback(response) {

          });
        }
      }
    });
