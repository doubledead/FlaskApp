angular.module('events.services', [])
  .factory('EventService', function($http){

      return {
        getItems: function() {
          var url = location.pathname;
          // Split event ID out of URL
          var paramId = url.split('/events/host/', 2)[1];

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
        reactivateItem: function(itemId) {

          var data = {
            paramId: itemId
          };

          return $http({
            method: 'POST',
            url: '/events/reactivateitem',
            data: JSON.stringify(data)
          }).then(function successCallback(response) {
            return response;
          }, function errorCallback(response) {
            console.log(response);
          });
        }
      }
    });
