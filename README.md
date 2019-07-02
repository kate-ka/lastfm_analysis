# lastfm_analysis

Lastfm analysis is an app that shows lastfm user's statistics on listened and scrobbled music. 

The project contains one app, where user can enter his lastfm username and get top artists charts, scrobbles by year chart,
top albums by year,photo collage created from albums images and list of forgotten albums(albums that user hasn't listened to for a long period)


## Technology Stack

- Python 3.5
- Django 1.9
- Crossroads.js
- highcharts.js
- Bootstrap 3
- Celery 4.1.1

## Installation guideline

 - Activate your virtual environment: `source <virtual_env>/bin/activate`
 - Install needed packages: `pip install -r requirements.txt`
 - Run Django server: `python manage.py runserver`
 
 There is also another separate version of a frontend, where Angular was used for routing:
 - Run Frontend: `npm install`, `bower install`, `grunt serve`
 
## Install via docker (both frontend and backend)
- Run docker-compose `docker-compose up`
- Go to localhost:7000

Frontend can be found here: https://github.com/kate-ka/lastfm_analysis_frontend
