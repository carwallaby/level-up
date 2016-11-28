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
            // get rid of ISO timezone so time is parsed as naive
            var naive = scope.localDate.split('+');
            scope.localNow = moment(naive[0]);
            scope.frequencies = TrendFactory.tallyCompletionsByDate(scope.completions);
            scope.daysOfWeek = moment.weekdaysShort();

            function loadNewMonth() {
                scope.monthString = moment().month(scope.currentMonth).format('MMMM');
                scope.dates = TrendFactory.getDatesByMonthAndYear(scope.monthString, scope.currentYear);
                scope.onCurrentMonth = (scope.currentMonth === scope.localNow.month() && scope.currentYear === scope.localNow.year());
            }

            scope.loadCurrentMonth = function() {
                scope.currentMonth = scope.localNow.month();
                scope.currentYear = scope.localNow.year();
                loadNewMonth();
            };

            scope.changeMonth = function(numMonths) {
                var newMoment = moment().year(scope.currentYear).month(scope.currentMonth + numMonths);
                scope.currentMonth = newMoment.month();
                scope.currentYear = newMoment.year();
                loadNewMonth();
            };

            scope.isToday = function(date) {
                return date.format('YYYY-MM-DD') === scope.localNow.format('YYYY-MM-DD');
            };

            scope.loadCurrentMonth();
        }
    }
});
