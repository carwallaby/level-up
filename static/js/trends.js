'use strict';

lvlup
.directive('lvlLineChart', function(TrendFactory) {
    function fillInMissingDates(dates, frequenciesByDate) {
        var points = [];

        for (var i = 0; i < dates.length; i++) {
            if (dates[i] in frequenciesByDate) {
                points.push(frequenciesByDate[dates[i]]);
            } else {
                points.push(0);
            }
        }

        return points;
    }

    function drawChart(chart, completions, numDays) {
        var frequencies = TrendFactory.tallyCompletionsByDate(completions);
        var dates = TrendFactory.getPastDates(numDays);
        var formattedDates = TrendFactory.massFormatMoments(dates, 'MMM D YYYY');
        var labels = TrendFactory.massFormatMoments(dates, 'MMM D');
        var points = fillInMissingDates(formattedDates, frequencies);

        var data = {
            labels: labels,
            datasets: [{
                label: 'Completions',
                data: points,
                fill: false,
                borderColor: '#4fc3f7',
                borderWidth: 1
            }]
        };

        var options = {
            legend: {
                display: false
            },
            scales: {
                yAxes: [{
                    ticks: {
                        min: 0,
                        stepSize: 1
                    }
                }]
            }
        };

        var trendChart = new Chart(chart, {
            type: 'line',
            data: data,
            options: options
        });
    }

    return {
        restrict: 'A',
        scope: {
            completions: '=',
            days: '@'
        },
        link: function(scope, element, attrs) {
            var chart = angular.element(element);

            attrs.$observe('days', function(days) {
                scope.days = days;
                drawChart(chart, scope.completions, scope.days);
            });
        }
    }
});
