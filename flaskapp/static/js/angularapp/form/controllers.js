angular.module('form.controllers', [])
.controller('formCtrl', ['$scope', '$http', '$timeout', function ($scope, $http, $timeout) {

    $scope.params = {};

	$scope.submitForm = function () {
        var 
            deferred = $.Deferred(),
            data = JSON.stringify($scope.params);

        // jQuery Ajax is used to reach Flask endpoints
        // because AngularJS routes are not used.
        $.ajax({
            cache: false,
            contentType: 'application/json; charset=utf-8',
            accepts: 'application/json',
            url: '/main/create',
            data: data,
            dataType: 'json',
            type: 'POST'
        }).success(function(response) {
            deferred.resolve(response);
            console.log(response);
            $scope.$apply(reset());
        }).fail(function(response) {

        }).done(function(response) {

        });
        return deferred.promise();
    };

    function changeRoute() {
        location.assign("http://127.0.0.1:5000/main/");
    }

    function reset() {
        // Clean up scope before destorying
        $scope.params = {};

        // Send the app back to a Flask route
        //$timeout((location.assign("http://127.0.0.1:5000/main/")), 4000);
        $timeout(changeRoute, 3000);
    }
}]);