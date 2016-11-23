'use strict';

lvlup
.factory('MomentFactory', function() {
    var momentFactory = {};

    momentFactory.tallyCompletionsByDate = function(completions) {
        var frequencies = {};

        for (var i = 0; i < completions.length; i++) {
            var timestamp = moment(completions[i].timestamp);
            var date = timestamp.format('MMM D YYYY');
            if (date in frequencies) {
                frequencies[date][0]++;
            } else {
                frequencies[date] = [1, timestamp];
            }
        }

        return frequencies;
    };

    momentFactory.getPastNDates = function(numDays) {
        var dates = [];

        for (var i = 0; i < numDays; i++) {
            dates.push(moment().subtract(i, 'days'));
        }

        return dates;
    };

    return momentFactory;
});
