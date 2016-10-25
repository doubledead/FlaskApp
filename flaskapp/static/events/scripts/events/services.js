angular.module('events.services', [])
  .factory('EventService', function($http){

      return {
        getEvent: function() {
          var url = location.pathname;
          var paramId = url.split("/events/", 2)[1];

          var data = {
            id: paramId
          };

          // console.log(url.split("/events/", 2)[1]);

          return $http({
            method: 'POST',
            url: '/events/gettest',
            data: JSON.stringify(data)
          }).then(function successCallback(response) {
            if (response && response.data) {
              // console.log(response.data)
              console.log(response)
              return response.data;
            }
          }, function errorCallback(response) {
            console.log(response);
          });
        }
      }
    });
