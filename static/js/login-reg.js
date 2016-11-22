'use strict';

lvlup
.controller('LoginRegController', function($scope, $http) {
    $scope.validatedLocation = false;
    $scope.searching = false;
    $scope.locationResults = [];

    $scope.findLocations = function(location) {
        // clear pre-existing location results
        $scope.locationResults = [];
        $scope.searching = true;

        var reqUrl = '/json/validate-location?location=' + location;
        $http.get(reqUrl).then(function(res) {
            $scope.searching = false;
            if ('error' in res.data) {
                $scope.locationResults.push({
                    name: res.data.error,
                    timezone: null
                });
            } else {
                $scope.locationResults = res.data;
                if ($scope.locationResults.length === 1) {
                    $scope.selectLocation($scope.locationResults[0]);
                }
            }
        });
    };

    $scope.selectLocation = function(locationObj) {
        if (locationObj.timezone === null) {
            $scope.clearLocations();
        } else {
            $scope.validatedLocation = true;
            $scope.location = locationObj.name;
            $scope.timezone = locationObj.timezone;
            $scope.locationResults = [];
        }
    };

    $scope.clearLocations = function() {
        $scope.validatedLocation = false;
        $scope.location = '';
        $scope.timezone = '';
        $scope.locationResults = [];
    };
});
