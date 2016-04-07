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
});