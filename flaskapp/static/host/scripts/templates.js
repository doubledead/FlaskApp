angular.module('templates', []).run(['$templateCache', function($templateCache) {$templateCache.put('events/event.html','<!-- Items -->\n<div ng-repeat="item in event.items_data">\n  <item-row ng-if="item.active === true" item="item"></item-row>\n</div>\n<div class="row">\n  <div class="col-xs-12 col-sm-12 col-md-12">&nbsp;</div>\n</div>\n<div class="row">\n  <div class="col-xs-12 col-sm-12 col-md-12">\n    <h4><strong>Removed Items</strong></h4>\n  </div>\n</div>\n<div ng-repeat="item in event.items_data">\n  <item-row ng-if="item.active === false" item="item"></item-row>\n</div>\n<!-- End Items -->\n');
$templateCache.put('form/row.html','<div class="form-group">\n  <label for="tb-title">Title:</label>\n  <input type="text" class="form-control" id="tb-title" ng-model="params.title">\n</div>\n<div class="form-group">\n  <label for="tb-post-date">Post Date:</label>\n  <input type="text" class="form-control" id="tb-post-date" ng-model="params.post_date">\n</div>\n<div class="form-group">\n  <label for="tb-body">Body:</label>\n  <input type="text" class="form-control" id="tb-body" ng-model="params.body">\n</div>\n');
$templateCache.put('events/items/item.html','<div ng-class="{\'item-removed\': item.active === false}">\n  <div class="row">\n    <div class="col-xs-2 col-sm-2 col-md-3"><strong>Name:</strong> {{ item.name }}</div>\n    <div class="col-xs-2 col-sm-2 col-md-2">Quantity: {{ item.quantity }}</div>\n    <div class="col-xs-2 col-sm-2 col-md-2">Claimed: {{ item.quantity_claimed }}</div>\n    <div class="col-xs-2 col-sm-2 col-md-2">\n      <button type="button" class="btn btn-danger btn-xs" ng-click="$parent.removeItem(item.id)">\n        <span ng-if="item.active===true">Remove Item</span>\n        <span ng-if="item.active===false">Reactivate Item</span>\n      </button>\n    </div>\n  </div>\n  <div class="row">\n    <div class="col-xs-12 col-sm-12 col-md-12">&nbsp;</div>\n  </div>\n  <div class="row">\n    <div class="col-xs-12 col-sm-12 col-md-12">&nbsp;</div>\n  </div>\n  <div class="row">\n    <div class="col-xs-12 col-sm-12 col-md-12"><strong>You\'ve Claimed:</strong></div>\n  </div>\n  <!-- Subitems -->\n  <div ng-repeat="subitem in item.subitems">\n    <subitem-row subitem="subitem"></subitem-row>\n  </div>\n  <!--End Subitems -->\n  <div class="row">\n    <hr >\n  </div>\n  <div class="row">\n    <div class="col-xs-12 col-sm-12 col-md-12">&nbsp;</div>\n  </div>\n</div>\n');
$templateCache.put('events/subitems/subitem.html','<div class="row">\n  <!--<div class="col-sx-2 col-sm-2 col-md-2">User: {{ subitem.user_id }}</div>-->\n  <div class="col-xs-2 col-sm-2 col-md-1">\n    <div class="form-group">\n      <label for="{{\'tb-subitem-quantity-\' + subitem.id}}">&nbsp;</label>\n      <input type="text"\n             id="{{\'tb-subitem-quantity-\' + subitem.id}}"\n             class="form-control"\n             ng-model="subitem.quantity">\n    </div>\n  </div>\n</div>\n');}]);