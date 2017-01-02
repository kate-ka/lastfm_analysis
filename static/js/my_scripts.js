$(document).ready(function () {
    $(document).ajaxStart(function () {
        $('#loading').show();
    });
    $(document).ajaxStop(function () {
        $("#loading").hide();
    });



    // Current username from url will be stored there
    // and will be used when user clicks on tab
    var currentUser = null;

    function renderChart(chartData) {
        $('#container').highcharts({
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie'
            },
            title: {
                text: 'Top Artists'
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
                data: chartData
            }]
        });
    }


    function getTopArtists(username) {
        $('#topArtistsBtn').tab('show');

        $.get('/api-v1/users/' + username + '/top-artists/', function (json) {
            $('#top_artists').empty();

            $.each(json.artists, function () {
                var pageHtml = '<div>' + this['name'] + this['plays'] + '</div>';

                $('#top_artists').append(pageHtml);
            });


            // Prepare data for our chart
            var chartData = [];

            // Need to convert {"name": "Iron maiden", "plays": "444"} to {"name": "Iron maiden", "y": 444}
            for (var i = 0; i < json.artists.length; i++) {
                var chartItem = {
                    name: json.artists[i]['name'],
                    y: parseInt(json.artists[i]['plays'])
                };
                chartData.push(chartItem);

            }


            renderChart(chartData);


        });


    }

    function renderScrobblesChart(chartYears, chartScrobbles) {
        $('#container_2').highcharts({
            chart: {
                type: 'bar'
            },
            title: {
                text: 'Lastfm scrobbles by Years'
            },
            subtitle: {
                text: 'Source: <a href="http://www.last.fm">Last.fm</a>'
            },
            xAxis: {
                categories: chartYears,
                title: {
                    text: null
                }
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Number of Scrobbles',
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
                x: -40,
                y: 80,
                floating: true,
                borderWidth: 1,
                backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
                shadow: true
            },
            credits: {
                enabled: false
            },
            series: [{
                data: chartScrobbles
            }]
        });


    }

    function getAllScrobblesByYear(username) {
        // Save current user, for using it when user clicks on tab
        currentUser = username;
        $('#scrobblesByYearBtn').tab('show');

        $.get('/api-v1/users/' + username + '/total-by-years/', function (json) {
            $('#all_scrobbles').empty();

            $.each(json.scrobbles, function () {
                var pageHtml = '<div>' + this['year'] + this['scrobbles'] + '</div>';

                $('#all_scrobbles').append(pageHtml);
            });

            var chartScrobbles = [];
            var chartYears = []
            for (var i = 0; i < json.scrobbles.length; i++) {

                    //data = parseInt(json.scrobbles[i]['scrobbles']);
                 var chartScrobble = json.scrobbles[i]['scrobbles']


                var chartYear =
                    json.scrobbles[i]['year']
                chartYears.push(chartYear);


                chartScrobbles.push(chartScrobble);
            }
            renderScrobblesChart(chartYears, chartScrobbles);


        });


    }

    function getTopAlbumsByYears(username) {
        // Save current user, for using it when user clicks on tab
        currentUser = username;

        $('#topAlbumsByYearBtn').tab('show');
        $.get('/api-v1/users/' + username + '/top-albums-by-years/', function (json) {
            _.templateSettings.variable = 'rc';
            $('#container_3').empty();

            var pageHtml = $('#top-albums-template').html();
            var template = _.template(pageHtml);

            //$.each(json.top_albums, function () {
            //    pageHtml = pageHtml + '<div>' + this['year'] + '</div>'
            //    $.each(this.months, function() {
            //        pageHtml = pageHtml + '<div>' + this['month']+'</div>' + '<div>' + this['album'] + '</div>' + '<div>' + this['artist']+ '</div>' + "<img src= '" + this['img'] + "'>" + '</div>'
            //    })
            //    });
            $('#container_3').append(
                template(json)
            )
        })


    }
    function getPhotoCollage(username) {
        currentUser = username;
        $('#collageBtn').tab('show');
        $('#container_4').empty();
        var photoCollageUrl = 'http://127.0.0.1:8000/api-v1/users/' + username + '/photo-collage';

            $('#container_4').append('<img src="' + photoCollageUrl + '">');
    }
    function getForgottenAlbums(username) {
        currentUser = username;
        $('#forgottenAlbumsBtn').tab('show');
        $('#year_input').submit(function(event) {
            event.preventDefault();
            $('#container_5').empty();
            var yearToStartWith =  {
                from_date: $('#year option:selected').val()
            };

             $.getJSON('/api-v1/users/' + username + '/forgotten_albums', yearToStartWith, function(data) {
            _.templateSettings.variable = 'rc';
            $('#container_5').empty();
            var pageHtml = $('#forgotten-albums-template').html();
            var template = _.template(pageHtml);
            $('#container_5').append(template(data))

        })
        })

    }


    function getInputData() {
        $('button').click(function () {
            var username = $('input').val();
            var url = 'users/' + username + '/topArtists';
            goToUrl(url);

        })
    }

    getInputData();



    function userPage(username) {
        currentUser = username;
        getTopArtists(username);
    }


    $('#topArtistsBtn').click(function(){
         if(currentUser) {
             goToUrl('users/' + currentUser + '/topArtists');
         }
     });

     $('#scrobblesByYearBtn').click(function() {
         if(currentUser) {
             goToUrl('users/' + currentUser + '/scrobblesByYear');
         }
     });

     $('#topAlbumsByYearBtn').click(function(){
         if(currentUser) {
             goToUrl('users/' + currentUser + '/topAlbumsByYear');
         }
     });
    $('#collageBtn').click(function() {
        if (currentUser) {
            goToUrl('users/' + currentUser + '/collage');
        }
    });

    $('#forgottenAlbumsBtn').click(function() {
        if (currentUser) {
            goToUrl('users/' + currentUser + '/forgottenAlbums');
        }
    });

    function goToUrl(url){
        // Pass url to crossroads to run function that will request data from server and draw this data
        crossroads.parse(url);
        // Pass url to hasher to set new url in browser address line
        hasher.setHash(url);
    }


    function init(){
        function onUrlChange(newHash) {
            // second parameter of crossroads.parse() is the "defaultArguments" and should be an array
            // so we ignore the "oldHash" argument to avoid issues.
            crossroads.parse(newHash);
        }

        // Congigure routes, Crossroads.js is a "typical" routing library
        // that just maps url patterns to callbacks, one url pattern per callback
        crossroads.addRoute('users/{username}/topArtists', userPage);
        crossroads.addRoute('users/{username}/scrobblesByYear', getAllScrobblesByYear);
        crossroads.addRoute('users/{username}/topAlbumsByYear', getTopAlbumsByYears);
        crossroads.addRoute('users/{username}/collage', getPhotoCollage);
        crossroads.addRoute('users/{username}/forgottenAlbums', getForgottenAlbums);


        // Configure Hash
        hasher.initialized.add(onUrlChange); //parse initial hash
        hasher.changed.add(onUrlChange); //parse hash changes
        hasher.init();
    }

    init();
});
