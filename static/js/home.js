'use strict';

lvlup
.controller('HomeController', function($scope, currentUser, habits) {
    $scope.currentUser = currentUser;
    $scope.habits = habits;

    $scope.getSortedHabits = function() {
        var toDo = [];
        var completed = [];

        for (var i = 0; i < $scope.habits.length; i++) {
            if ($scope.habits[i].done_today) {
                completed.push($scope.habits[i]);
            } else {
                toDo.push($scope.habits[i]);
            }
        }

        return toDo.concat(completed);
    };
})

.controller('NewHabitController', function($scope) {
    $scope.optionsShown = false;

    $scope.showGoalOptions = function() {
        $scope.optionsShown = true;
    };
});
