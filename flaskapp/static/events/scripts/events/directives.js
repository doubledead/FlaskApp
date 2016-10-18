angular.module('events.directives', [])
.directive('itemRow', function () {
  return {
    restrict: 'E',
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
    templateUrl: 'events/row.html',
    link: function (scope, element, attrs) {

    }
  };
});
