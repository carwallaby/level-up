'use strict';

lvlup
.controller('HomeController', function($scope, currentUser, habits) {
    $scope.currentUser = currentUser;
    $scope.habits = habits;
    var userLocation = $scope.currentUser.location;
    $scope.location = userLocation.split(', ')[0];

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

.directive('lvlClock', function($interval) {
    return {
        restrict: 'E',
        templateUrl: 'static/partials/clock.html',
        scope: {
            startTime: '='
        },
        link: function(scope, element, attr) {
            scope.time = moment(scope.startTime);
            $interval(function() {
                scope.time.add(1, 'seconds');
            }, 1000)
        }
    }
})

.controller('NewHabitController', function($scope) {
    $scope.optionsShown = false;

    $scope.showGoalOptions = function() {
        $scope.optionsShown = true;
    };
})

.controller('AccountController', function($scope, currentUser) {
    $scope.currentUser = currentUser;
})

.controller('HabitViewController', function($scope, currentUser, habitInfo, $state) {
    $scope.currentUser = currentUser;
    $scope.habit = habitInfo.habit;
    $scope.completions = habitInfo.completions;
    $state.transitionTo('habit.calendar', {id: $scope.habit.habit_id});

    $scope.days = 7;
    $scope.changeDays = function(numDays) {
        if (numDays !== $scope.days) {
            $scope.days = numDays;
        }
    };
});
