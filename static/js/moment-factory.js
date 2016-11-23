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

    return momentFactory;
});
