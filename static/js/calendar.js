'use strict';

lvlup
.directive('lvlCalendar', function(TrendFactory) {
    return {
        templateUrl: 'static/partials/calendar.html',
        scope: {
            localDate: '=',
            completions: '='
        },
        link: function(scope, element, attrs) {
            var localNow = moment(scope.localDate);
            scope.frequencies = TrendFactory.tallyCompletionsByDate(scope.completions);

            function loadNewMonth() {
                scope.monthString = moment().month(scope.currentMonth).format('MMMM');
                scope.dates = TrendFactory.getDatesByMonthAndYear(scope.monthString, scope.currentYear);
                scope.onCurrentMonth = (scope.currentMonth === localNow.month() && scope.currentYear === localNow.year());
            }

            scope.loadCurrentMonth = function() {
                scope.currentMonth = localNow.month();
                scope.currentYear = localNow.year();
                loadNewMonth();
            };

            scope.changeMonth = function(numMonths) {
                var newMoment = moment().year(scope.currentYear).month(scope.currentMonth + numMonths);
                scope.currentMonth = newMoment.month();
                scope.currentYear = newMoment.year();
                loadNewMonth();
            };

            scope.isToday = function(date) {
                return date.format('YYYY-MM-DD') === localNow.format('YYYY-MM-DD');
            };

            scope.loadCurrentMonth();
        }
    }
});
