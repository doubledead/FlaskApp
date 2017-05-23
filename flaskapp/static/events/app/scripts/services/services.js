angular.module('services', [])
  .factory('EventService', function($http){

      return {
        getItems: function() {
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
