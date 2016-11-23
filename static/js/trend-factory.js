'use strict';

lvlup
.factory('TrendFactory', function() {
    var trendFactory = {};

    trendFactory.tallyCompletionsByDate = function(completions) {
        var frequencies = {};

        for (var i = 0; i < completions.length; i++) {
            var timestamp = moment(completions[i].timestamp);
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

        for (var i = 0; i <= 31; i++) {
            var nextDay = moment().year(year).month(monthString).date(1 + i);
            if (nextDay.month() !== moment().month(monthString).month()) {
                break;
            }
            completeMonth.push(nextDay);
        }

        return completeMonth;
    };

    return trendFactory;
});
