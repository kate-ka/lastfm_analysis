$(function () {
    function getInputData() {
        $('button').click(function() {
        var username = $('input').val();
        $('#loading').show();
            getTopArtists(username);
            getAllScrobblesByYear(username);
            getTopAlbumsByYears(username);
            getPhotoCollage(username);
    })}
    getInputData();

    function renderChart(data) {
        $('#container').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: 'Top artists'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    }
                }
            }
        },
            series: [{
            name: 'Brands',
            colorByPoint: true,
            data: data
        }]
    });
    }

    function renderScrobblesChart(data, years) {
        $('#container_2').highcharts({
        chart: {
            type: 'bar'
        },
        title: {
            text: 'Scrobbles By Year Chart'
        },
        subtitle: {
            text: 'Source: <a href="https://en.wikipedia.org/wiki/World_population">Wikipedia.org</a>'
        },
        xAxis: {
            categories: years,
            title: {
                text: null
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Scrobbles by Year',
                align: 'high'
            },
            labels: {
                overflow: 'justify'
            }
        },
        tooltip: {
            valueSuffix: ' scrobbles'
        },
        plotOptions: {
            bar: {
                dataLabels: {
                    enabled: true
                }
            }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'top',
            x: -5,
            y: 160,
            floating: true,
            borderWidth: 1,
            backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
            shadow: true
        },
        credits: {
            enabled: false
        },
        series: [{
            data: data,
        }]
    });
    }

    function getTopArtists(username) {
        $.getJSON('/api-v1/users/' + username + '/top-artists', function(data) {

            var chartData = [];
            var artists = data.artists;
            for(var i=0; i < artists.length; i ++) {
                var chartItem = {
                    name: artists[i]['name'],
                    y: parseInt(artists[i]['plays'])
                };
                chartData.push(chartItem)
            }
             $('#loading').hide();
             renderChart(chartData)
        })

    }

    function getAllScrobblesByYear(username) {
        $.getJSON('/api-v1/users/' + username + '/total-by-years', function(data) {
            var scrobbles = data.scrobbles;
            var yearsChart = [];
            var dataChart = [];

            $.each(scrobbles, function() {
                yearsChart.push(this['year']);
                //dataChart.push(this['scrobbles'])
                dataChart.push(this['scrobbles'])

            });


            renderScrobblesChart(dataChart, yearsChart);
        })
    }

    function getTopAlbumsByYears(username) {
        $.getJSON('/api-v1/users/' + username + '/top-albums-by-years', function(data) {
            var pageHtml = $('#top-albums-template').html();
            var template = _.template(pageHtml);
            console.log(data)
            $('#container_3').append(template(data));
        })
    }

    function getPhotoCollage(username) {
        var photoCollageUrl = 'http://127.0.0.1:8000/api-v1/users/' + username + '/photo-collage';
            $('#container_4').append('<img src="' + photoCollageUrl + '">');
    }


});