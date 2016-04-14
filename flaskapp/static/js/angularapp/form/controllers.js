angular.module('form.controllers', [])
.controller('formCtrl', ['$scope', '$http', function ($scope, $http) {

	$scope.submitForm = function () {
		var timeStamp = new Date();

		console.log('Test: ' + timeStamp);

		/*
    $http.get('/test').then(function(resp) {
			console.log(resp.data);
		});
    */

    var deferred = $.Deferred();

    $.ajax({
        cache: false,
        contentType: 'application/json; charset=utf-8',
        accepts: 'application/json',
        url: '/user/test',
        data: '',
        dataType: 'json',
        type: 'POST'
    }).done( function(response) {

        deferred.resolve(response);
        console.log(response);
        if (response) {
          $scope.$apply($scope.fname = response.fname);
          $scope.$apply($scope.lname = response.lname);
          // These need to be parsed
          //$scope.$apply($scope.dateOfBirth = response.dateOfBirth);
          //$scope.$apply($scope.email = response.email);
        }

    });
    return deferred.promise();
	};


}]);