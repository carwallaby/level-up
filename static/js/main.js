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
        template: '{{ time.format(\'h:mm a\') }} on {{ time.format(\'MMMM Do\') }}',
        scope: {
            startTime: '='
        },
        link: function(scope, element, attr) {
            // get rid of ISO timezone so time is parsed as naive
            var naive = scope.startTime.slice(0, -6);
            scope.time = moment(naive);
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

.controller('AccountController', function($scope, currentUser, $http, $state) {
    $scope.currentUser = currentUser;

    $scope.nameFormShown = false;
    $scope.toggleNameForm = function() {
        $scope.nameFormShown = !$scope.nameFormShown;
    };
    $scope.updateName = function(name) {
        var reqUrl = '/api/update-name';
        $http.post(reqUrl, {name: name}).then(function(res) {
            $state.reload();
        });
    };

    $scope.smsFormShown = false;
    $scope.toggleSmsForm = function() {
        $scope.smsFormShown = !$scope.smsFormShown;
    };
})

.controller('HabitViewController', function($scope, currentUser, habitInfo, $state, $http) {
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

    $scope.deleteHabit = function(habitId) {
        var confirmation = confirm('Are you sure? All habit and completion data will be deleted permanently.');

        if (confirmation) {
            return $http.get('/api/delete-habit?habit-id=' + habitId).then(function() {
                $state.go('home');
            });
        }
    };
})

.controller('EditHabitController', function($scope, habit) {
    $scope.habit = habit;
});
