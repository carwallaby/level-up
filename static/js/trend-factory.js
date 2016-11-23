'use strict';

lvlup
.factory('TrendFactory', function() {
    var momentFactory = {};

    momentFactory.tallyCompletionsByDate = function(completions) {
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

    momentFactory.getPastDates = function(numDays) {
        var dates = [];

        for (var i = 0; i < numDays; i++) {
            dates.push(moment().subtract(i, 'days'));
        }

        return dates;
    };

    momentFactory.massFormatMoments = function(momentArray, formatString) {
        var formatted = [];

        for (var i = 0; i < momentArray.length; i++) {
            formatted.push(momentArray[i].format(formatString));
        }

        return formatted;
    };

    return momentFactory;
});
