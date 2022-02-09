import requests
import json
from flask import Flask, render_template, request, flash
from wtforms import Form, validators, StringField


OPENWEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&appid=bed42a048077065f193f82b6c4726144'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you are my sunshine'


"""
First endpoint, simple get method
"""
@app.route('/')
def get_city():
    city = {'cityname': 'San Jose'}
    return render_template('index.html', city=city)


"""
Second endpoint, weather fetching method defined as member of a class
"""
class GetZipCodeForm(Form):

    zip = StringField('Zip Code:', validators=[validators.DataRequired()])

    @app.route('/weather', methods=['GET', 'POST'])
    def get_weather():
        form = GetZipCodeForm(request.form)
        print(form.errors)

        if request.method == 'POST':
            zip = request.form['zip']
            print(f'zip = {zip}')

        weather = {}

        if form.validate():
            weather_json = fetch_weather_from_api(zip)
            print(f'weather_json = {weather_json}')

            if 'name' in weather_json:
                city_name = weather_json['name']
                summary = weather_json['weather'][0]['description']
                temperature = _temp_conversion(weather_json['main']['temp'])
                pressure = weather_json['main']['pressure']
                humidity = weather_json['main']['humidity']

                weather['city'] = city_name
                weather['summary'] = summary
                weather['temp'] = temperature
                weather['press'] = pressure
                weather['humid'] = humidity

                flash('Success!')
            else:
                flash('Invalid ZIP code entered')
        else:
            flash('All the form fields are required.')

        return render_template('zipcode.html', form=form, weather=weather)


def fetch_weather_from_api(zip_code):
    """
    make API call to openweathermap.org, get weather with zipcode
    """
    try:
        print(f'zip_code = {zip_code}')
        url = OPENWEATHER_API_URL.format(zip_code)
        print(f'url = {url}')
        response = requests.get(url=url)
        return response.json()
    except:
        raise Exception


def _temp_conversion(temp_in_str):
    """
    temp_in_str: temperature in Kelvin as string
    returns: temperature in Fahrenheit as string, only two decimal places
    """
    float_temp = (float(temp_in_str) - 273.15) * 9. / 5. + 32.0
    return '{0:.2f}'.format(float_temp)


if __name__ == '__main__':
    """
    start the web server, POC only (not for production)
    """
    app.run(debug=True, host='0.0.0.0', port=8099)
