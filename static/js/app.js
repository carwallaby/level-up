'use strict';

var lvlup = angular.module('LevelUp', ['ui.router']);

lvlup
.config(function($stateProvider, $locationProvider) {
    $locationProvider.html5Mode({
        enabled: true,
        requireBase: false
    });

    $stateProvider.state('register', {
        url: '/register',
        templateUrl: 'static/partials/register.html',
        controller: 'LoginRegController'
    })
    .state('login', {
        url: '/login',
        templateUrl: 'static/partials/login.html',
        controller: 'LoginRegController'
    })
    .state('home', {
        url: '/home',
        templateUrl: 'static/partials/home.html',
        controller: 'HomeController',
        resolve: {
            currentUser: function($http) {
                return $http.get('/json/get-current-user').then(function(res) {
                    return res.data;
                });
            },

            habits: function($http) {
                return $http.get('/json/get-user-habits').then(function(res) {
                    return res.data;
                });
            }
        }
    })
    .state('new-habit', {
        url: '/new-habit',
        templateUrl: 'static/partials/new_habit.html',
        controller: 'NewHabitController'
    });
})
.run(function($rootScope, $state, $timeout) {
    $rootScope.$on('$stateChangeSuccess', function() {
        var flashContainer = document.getElementById('flash-container');
        $timeout(function() {
            while (flashContainer.firstChild) {
                flashContainer.removeChild(flashContainer.firstChild);
            }
        }, 2500);
    });
});
