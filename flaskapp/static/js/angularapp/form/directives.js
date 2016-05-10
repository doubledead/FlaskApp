angular.module('form.directives', [])
.directive('formRow', function () {
    return {
        restrict: 'E',
        //templateUrl: 'partials/form/row.html',
        template: 
        '<div class="form-group">' +
        '<label for="tb-fname">First Name:</label>' +
        '<input type="text" id="tb-fname" class="form-control" ng-model="fname">' +
        '</div>' +
        '<div class="form-group">' +
        '<label for="tb-lname">Last Name:</label>' +
        '<input type="text" id="tb-lname" class="form-control" ng-model="lname">' +
        '</div>' +
        '<div class="form-group">' +
        '<label for="tb-date-birth">DOB:</label>' +
        '<input type="text" id="tb-date-birth" class="form-control" ng-model="dateOfBirth">' +
        '</div>' +
        '<div class="form-group">' +
        '<label for="tb-email">Email:</label>' +
        '<input type="text" id="tb-email" class="form-control" ng-model="email">' +
        '</div>',
        link: function (scope, element, attrs) {

        }
    };
})
.directive('entryRow', function () {
    return {
        restrict: 'E',
        //templateUrl: 'partials/form/row.html',
        template: 
        '<div class="form-group">' +
        '<label for="tb-title">Title:</label>' +
        '<input type="text" id="tb-title" class="form-control" ng-model="params.title">' +
        '</div>' +
        '<div class="form-group">' +
        '<label for="tb-body">Body:</label>' +
        '<input type="text" id="tb-body" class="form-control" ng-model="params.body">' +
        '</div>',
        link: function (scope, element, attrs) {

        }
    };
});