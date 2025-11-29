from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_key = '24f67f504a9a450a52006a9228d8c45b'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    try:
        data = request.get_json()
        city_name = data.get('city', 'Bangalore')
        
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}&units=metric'
        response = requests.get(url)
        
        if response.status_code == 200:
            weather_data = response.json()
            return jsonify({
                'success': True,
                'city': weather_data.get('name'),
                'country': weather_data.get('sys', {}).get('country'),
                'temperature': weather_data.get('main', {}).get('temp'),
                'feels_like': weather_data.get('main', {}).get('feels_like'),
                'humidity': weather_data.get('main', {}).get('humidity'),
                'pressure': weather_data.get('main', {}).get('pressure'),
                'description': weather_data.get('weather', [{}])[0].get('description'),
                'wind_speed': weather_data.get('wind', {}).get('speed'),
                'cloudiness': weather_data.get('clouds', {}).get('all'),
                'icon': weather_data.get('weather', [{}])[0].get('icon')
            })
        else:
            return jsonify({'success': False, 'error': 'City not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
