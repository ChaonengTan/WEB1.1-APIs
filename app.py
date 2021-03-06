import os
import requests

from pprint import PrettyPrinter
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, render_template, request, send_file
# from geopy.geocoders import Nominatim


################################################################################
## SETUP
################################################################################

app = Flask(__name__)

# Get the API key from the '.env' file
load_dotenv()

pp = PrettyPrinter(indent=4)

API_KEY = os.getenv('API_KEY')
API_URL = 'http://api.openweathermap.org/data/2.5/weather'


################################################################################
## ROUTES
################################################################################

@app.route('/')
def home():
    """Displays the homepage with forms for current or historical data."""
    context = {
        'min_date': (datetime.now() - timedelta(days=5)),
        'max_date': datetime.now()
    }
    return render_template('home.html', **context)

def get_letter_for_units(units):
    """Returns a shorthand letter for the given units."""
    return 'F' if units == 'imperial' else 'C' if units == 'metric' else 'K'

@app.route('/results')
def results():
    """Displays results for current weather conditions."""
    # TODO: Use 'request.args' to retrieve the city & units from the query
    # parameters.
    city = request.args.get('city')
    units = request.args.get('units')

    params = {
        # TODO: Enter query parameters here for the 'appid' (your api key),
        # the city, and the units (metric or imperial).
        # See the documentation here: https://openweathermap.org/current
        'appid': API_KEY,
        'q': city,
        'units': units

    }

    result_json = requests.get(API_URL, params=params).json()

    # Uncomment the line below to see the results of the API call!
    # pp.pprint(f'{result_json}')

    # TODO: Replace the empty variables below with their appropriate values.
    # You'll need to retrieve these from the result_json object above.

    # For the sunrise & sunset variables, I would recommend to turn them into
    # datetime objects. You can do so using the `datetime.fromtimestamp()` 
    # function.


    # results.json:
    # ("
    # {
    # 'coord': {'lon': -83.3999, 'lat': 42.6667}, 
    # 'weather': [{'id': 804, 'main': ""'Clouds', 'description': 'overcast clouds', 'icon': '04n'}],
    #  'base': ""'stations',
    #  'main': {'temp': -8.56, 'feels_like': -15.03, 'temp_min': -8.89, ""'temp_max': -8, 'pressure': 1022, 'humidity': 73},
    #  'visibility': 10000,
    #  ""'wind': {'speed': 4.63, 'deg': 270},
    #  'clouds': {'all': 90},
    #  'dt': ""1613799341,
    #  'sys': {'type': 1, 'id': 5424, 'country': 'US', 'sunrise': ""1613823789, 'sunset': 1613862706},
    #  'timezone': -18000,
    #  'id': 5004223,
    #  ""'name': 'Oakland',
    #  'cod': 200
    # }
    # ")

    context = {
        'date': datetime.now(),
        'city': result_json['name'],
        'description': result_json['weather'][0]['description'],
        'temp': result_json['main']['temp'],
        'humidity': result_json['main']['humidity'],
        'wind_speed': result_json['wind']['speed'],
        'sunrise': result_json['sys']['sunrise'],
        'sunset': result_json['sys']['sunset'],
        'units_letter': get_letter_for_units(units)
    }

    return render_template('results.html', **context)


@app.route('/comparison_results')
def comparison_results():
    """Displays the relative weather for 2 different cities."""
    # TODO: Use 'request.args' to retrieve the cities & units from the query
    # parameters.
    city1 = request.args.get('city1')
    city2 = request.args.get('city2')
    units = request.args.get('units')

    # TODO: Make 2 API calls, one for each city. HINT: You may want to write a 
    # helper function for this!

    params1 = {
        'appid': API_KEY,
        'q': city1,
        'units': units
    }
    city1Json = requests.get(API_URL, params=params1).json()
    params2 = {
        'appid': API_KEY,
        'q': city2,
        'units': units
    }
    city2Json = requests.get(API_URL, params=params2).json()

    # TODO: Pass the information for both cities in the context. Make sure to
    # pass info for the temperature, humidity, wind speed, and sunset time!
    # HINT: It may be useful to create 2 new dictionaries, `city1_info` and 
    # `city2_info`, to organize the data.
    def ifNeg(value):
        if value < 0:
            return 'Lower'
        return 'Greater'
    context = {
        'date': datetime.now(),
        'city1name': city1Json['name'],
        'city2name': city2Json['name'],
        'units': units,
        'cityDiff': {
            'temp': abs(city1Json['main']['temp'] - city2Json['main']['temp']),
            'tempNeg': ifNeg(city1Json['main']['temp'] - city2Json['main']['temp']),
            'humidity': abs(city1Json['main']['humidity'] - city2Json['main']['humidity']),
            'humidityNeg': ifNeg(city1Json['main']['humidity'] - city2Json['main']['humidity']),
            'windSpeed': abs(city1Json['wind']['speed'] - city2Json['wind']['speed']),
            'windSpeedNeg': ifNeg(city1Json['wind']['speed'] - city2Json['wind']['speed']),
            'sunsetTime': abs(city1Json['sys']['sunset'] - city2Json['sys']['sunset']),
            'sunsetTimeNeg': ifNeg(city1Json['sys']['sunset'] - city2Json['sys']['sunset'])
        }

    }

    return render_template('comparison_results.html', **context)


if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run(debug=True)
