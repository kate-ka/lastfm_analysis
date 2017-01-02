import json, requests, sys
APIKEY = '90cd53ae8357541b01518dc9d6ebea56'

# Compute location from command line arguments
if len(sys.argv) < 2:
    print('Usage: quickWeather.py location')
    sys.exit()
location = ' '.join(sys.argv[1:])
# http://api.openweathermap.org/data/2.5/weather?q=Lviv&APPID=90cd53ae8357541b01518dc9d6ebea56
url = 'http://api.openweathermap.org/data/2.5/weather?q=%s&APPID=%s' % (location, APIKEY)
# url ='http://api.openweathermap.org/data/2.5/weather?q=%s&APPID={APIKEY}' % (location)
response = requests.get(url)
response.raise_for_status()
weatherData = json.loads(response.text)
# Print the weather descriptions
# w = weatherData['list']
# print dir(weatherData)
print('Current weather in %s:' % (location))
# print dir(weatherData)
print weatherData[u'weather'][0][u'description']


