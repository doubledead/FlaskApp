'use strict';

angular.module('eventsApp.events', [
	'events.controllers',
  'events.event',
	'events.directives',
  'events.services',
  'events.item-service'
])
.run(['$rootScope', function ($rootScope) {

}]);
