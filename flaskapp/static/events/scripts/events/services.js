angular.module('events.services', [])
  .factory('EventService', function($http){

      return {
        getEvent: function() {
          var url = location.pathname;
          // Split event ID out of URL
          var paramId = url.split('/events/', 2)[1];

          var data = {
            paramId: paramId
          };

          return $http({
            method: 'POST',
            url: '/events/getitems',
            data: JSON.stringify(data)
          }).then(function successCallback(response) {
            return response;
          }, function errorCallback(response) {
            console.log(response);
          });
        }
      }
    });
