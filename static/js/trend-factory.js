'use strict';

lvlup
.factory('TrendFactory', function() {
    var trendFactory = {};

    trendFactory.tallyCompletionsByDate = function(completions) {
        var frequencies = {};

        for (var i = 0; i < completions.length; i++) {
            var naiveTimestamp = completions[i].timestamp.slice(0, -6);
            var timestamp = moment(naiveTimestamp);
            var date = timestamp.format('MMM D YYYY');

            if (date in frequencies) {
                frequencies[date]++;
            } else {
                frequencies[date] = 1;
            }
        }

        return frequencies;
    };

    trendFactory.getPastDates = function(numDays) {
        var dates = [];

        for (var i = 0; i < numDays; i++) {
            dates.push(moment().subtract(i, 'days'));
        }

        return dates;
    };

    trendFactory.massFormatMoments = function(momentArray, formatString) {
        var formatted = [];

        for (var i = 0; i < momentArray.length; i++) {
            formatted.push(momentArray[i].format(formatString));
        }

        return formatted;
    };

    trendFactory.getDatesByMonthAndYear = function(monthString, year) {
        var completeMonth = [];
        var firstWeekDay = moment().year(year).month(monthString).date(1).weekday();

        for (var i = firstWeekDay; i > 0; i--) {
            // start the month on a sunday
            var nextDay = moment().year(year).month(monthString).date(1 - i);
            completeMonth.push(nextDay);
        }

        var lastDayNum;
        for (var i = 0; i <= 31; i++) {
            var nextDay = moment().year(year).month(monthString).date(1 + i);
            if (nextDay.month() !== moment().month(monthString).month()) {
                lastDayNum = i;
                break;
            }
            completeMonth.push(nextDay);
        }

        var lastWeekDay = completeMonth[completeMonth.length - 1].weekday();
        for (var i = lastWeekDay, count = 1; i < 6; i++, count++) {
            // end the month on a saturday
            var nextDay = moment().year(year).month(monthString).date(lastDayNum + count);
            completeMonth.push(nextDay);
        }

        return completeMonth;
    };

    return trendFactory;
});
