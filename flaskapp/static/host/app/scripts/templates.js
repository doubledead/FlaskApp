angular.module('templates', []).run(['$templateCache', function($templateCache) {$templateCache.put('events/event.html','<!-- Items -->\n<div ng-repeat="item in event.items_data">\n  <item-row ng-if="item.active === true" item="item"></item-row>\n</div>\n<div class="row">\n  <div class="col-xs-12 col-sm-12 col-md-12">&nbsp;</div>\n</div>\n<div class="row">\n  <div class="col-xs-12 col-sm-12 col-md-12">\n    <h4><strong>Removed Items</strong></h4>\n  </div>\n</div>\n<div ng-repeat="item in event.items_data">\n  <item-row ng-if="item.active === false" item="item"></item-row>\n</div>\n<!-- End Items -->\n');
$templateCache.put('events/guests/guest.html','<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <title>Title</title>\n</head>\n<body>\n\n</body>\n</html>\n');
$templateCache.put('events/items/item.html','<div ng-class="{\'item-removed\': item.active === false}">\n  <div class="row">\n    <div class="col-xs-2 col-sm-2 col-md-3"><strong>Name:</strong> {{ item.name }}</div>\n    <div class="col-xs-2 col-sm-2 col-md-2">Quantity: {{ item.quantity }}</div>\n    <div class="col-xs-2 col-sm-2 col-md-2">Claimed: {{ item.quantity_claimed }}</div>\n    <div class="col-xs-2 col-sm-2 col-md-2">\n      <button type="button" class="btn btn-danger btn-xs" ng-click="$parent.removeItem(item.id)">\n        <span ng-if="item.active===true">Remove Item</span>\n        <span ng-if="item.active===false">Reactivate Item</span>\n      </button>\n    </div>\n  </div>\n  <!--\n  <div class="row">\n    <div class="col-xs-12 col-sm-12 col-md-12">&nbsp;</div>\n  </div>\n  <div class="row">\n    <div class="col-xs-12 col-sm-12 col-md-12">&nbsp;</div>\n  </div>\n  <host-subitem\n    subitem="item.host_subitem"\n    host-id="hostId"\n    item-id="item.id">\n\n  </host-subitem>\n  -->\n  <div class="row">\n    <div class="col-xs-12 col-sm-12 col-md-12">&nbsp;</div>\n  </div>\n  <div class="row">\n    <div class="col-xs-12 col-sm-12 col-md-12"><strong>Claimed:</strong></div>\n  </div>\n  <!-- Subitems -->\n  <div ng-repeat="subitem in item.subitems">\n    <subitem-row subitem="subitem" host-id="hostId" item-id="item.id"></subitem-row>\n  </div>\n  <!--End Subitems -->\n  <div class="row" ng-if="subitemsFlag">\n    <div class="col-sx-12 col-sm-12 col-md-12">No items claimed.</div>\n  </div>\n  <div class="row">\n    <div class="col-xs-12 col-sm-12 col-md-12">&nbsp;</div>\n  </div>\n  <div class="row" ng-show="subitemsFlag || hostSubitemsFlag">\n    <div class="col-sx-2 col-sm-2 col-md-2">You\'ve claimed:</div>\n    <div class="col-xs-2 col-sm-2 col-md-1">\n      <div class="form-group">\n        <label for="{{\'tb-subitem-quantity-\' + hostId}}">&nbsp;</label>\n        <input type="text"\n               id="{{\'tb-subitem-quantity-\' + hostId}}"\n               class="form-control"\n               ng-model="subitem.quantity">\n      </div>\n    </div>\n    <div class="col-xs-2 col-sm-2 col-md-2">\n      <!--Four inception layers up to the controller-->\n      <button type="button"\n              class="btn btn-primary btn-sm"\n              ng-click="$parent.$parent.addSubitem(subitem, item.id)">\n        Add\n      </button>\n    </div>\n  </div>\n  <div class="row">\n    <div class="col-xs-12 col-sm-12 col-md-12">&nbsp;</div>\n  </div>\n  <div class="row">\n    <hr >\n  </div>\n  <div class="row">\n    <div class="col-xs-12 col-sm-12 col-md-12">&nbsp;</div>\n  </div>\n</div>\n');
$templateCache.put('events/subitems/host-subitem.html','<div class="row">\n  <div class="col-sx-2 col-sm-2 col-md-2">You\'ve claimed:</div>\n  <div class="col-xs-2 col-sm-2 col-md-1">\n    <div class="form-group">\n      <label for="{{\'tb-subitem-quantity-\' + hostId}}">&nbsp;</label>\n      <input type="text"\n             id="{{\'tb-subitem-quantity-\' + hostId}}"\n             class="form-control"\n             ng-model="subitem.quantity">\n    </div>\n  </div>\n  <div class="col-xs-2 col-sm-2 col-md-2" ng-show="subitem.id">\n    <!--Four inception layers up to the controller-->\n    <button type="button"\n            class="btn btn-primary btn-sm"\n            ng-click="$parent.$parent.$parent.$parent.updateSubitem(subitem, itemId, hostId)">\n      Update\n    </button>\n  </div>\n  <div class="col-xs-2 col-sm-2 col-md-2" ng-show="!subitem.id">\n    <!--Four inception layers up to the controller-->\n    <button type="button"\n            class="btn btn-primary btn-sm"\n            ng-click="$parent.$parent.$parent.$parent.addSubitem(subitem, itemId, hostId)">\n      Add\n    </button>\n  </div>\n</div>\n<div class="row">\n  <div class="col-xs-12 col-sm-12 col-md-12">&nbsp;</div>\n</div>\n');
$templateCache.put('events/subitems/subitem.html','<div class="row" ng-show="subitem.user_id != hostId">\n  <!-- Need to add more user information here so Host can view user info. -->\n  <div class="col-sx-2 col-sm-2 col-md-2">User: {{ subitem.user_id }}</div>\n  <div class="col-sx-2 col-sm-2 col-md-2">Quantity: {{ subitem.quantity }}</div>\n</div>\n<div class="row">\n  <div class="col-xs-12 col-sm-12 col-md-12">&nbsp;</div>\n</div>\n<div class="row" ng-show="subitem.user_id === hostId">\n  <div class="col-sx-2 col-sm-2 col-md-2">You\'ve claimed:</div>\n  <div class="col-xs-2 col-sm-2 col-md-1">\n    <div class="form-group">\n      <label for="{{\'tb-subitem-quantity-\' + hostId}}">&nbsp;</label>\n      <input type="text"\n             id="{{\'tb-subitem-quantity-\' + hostId}}"\n             class="form-control"\n             ng-model="subitem.quantity">\n    </div>\n  </div>\n  <div class="col-xs-2 col-sm-2 col-md-2" ng-show="subitem.id">\n    <!--Four inception layers up to the controller-->\n    <button type="button"\n            class="btn btn-primary btn-sm"\n            ng-click="$parent.$parent.$parent.updateSubitem(subitem, itemId, hostId)">\n      Update\n    </button>\n  </div>\n</div>\n');}]);