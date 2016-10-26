angular.module('events.services', [])
  .factory('EventService', function($http){

      return {
        getEvent: function() {
          var url = location.pathname;
          var paramId = url.split("/events/", 2)[1];

          var data = {
            paramId: paramId
          };

          // console.log(url.split("/events/", 2)[1]);

          return $http({
            method: 'POST',
            url: '/events/getitems',
            data: JSON.stringify(data)
          }).then(function successCallback(response) {
            // console.log(response)
            return response;
            // return response;
          }, function errorCallback(response) {
            console.log(response);
          });
        }
      }
    });
