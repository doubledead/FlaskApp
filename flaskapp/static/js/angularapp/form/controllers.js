angular.module('form.controllers', [])
.controller('formCtrl', ['$scope', function ($scope) {

	$scope.submitForm = function () {
		var timeStamp = new Date();

		console.log('Test: ' + timeStamp);
	};


}]);