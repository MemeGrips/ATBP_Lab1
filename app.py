from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
from lab1 import time
import os

app = Flask(__name__, static_folder='public', static_url_path='')
CORS(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/traffic/<city>', methods=['GET'])
def get_traffic(city):
    # Фиксированные значения для тестов
    traffic_scores = {
        "Минск": 5,
        "Москва": 7,
        "Берлин": 3,
        "Париж": 5
    }
    traffic_score = traffic_scores.get(city, 5)
    return jsonify({
        'city': city,
        'trafficScore': traffic_score,
        'timestamp': __import__('datetime').datetime.now().isoformat()
    }), 200

@app.route('/api/delivery/estimate', methods=['POST'])
def calculate_delivery():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': 'Тело запроса не может быть пустым'}), 400

        distance = data.get('distance')
        speed = data.get('speed')
        terrain_type = data.get('terrainType')
        traffic_score = data.get('trafficScore', 0)

        if distance is None:
            return jsonify({'status': 'error', 'message': 'Поле "distance" обязательно'}), 400
        if speed is None:
            return jsonify({'status': 'error', 'message': 'Поле "speed" обязательно'}), 400
        if terrain_type is None:
            return jsonify({'status': 'error', 'message': 'Поле "terrainType" обязательно'}), 400

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        class MockMapsService:
            async def get_traffic_score(self, route_id):
                return traffic_score

        mock_service = MockMapsService() if traffic_score > 0 else None

        result = loop.run_until_complete(
            time(distance, speed, terrain_type, mock_service, "default")
        )
        loop.close()

        return jsonify({
            'status': 'success',
            'distance': distance,
            'speed': speed,
            'terrainType': terrain_type,
            'trafficScore': traffic_score,
            'time': result,
            'unit': 'часов'
        }), 200

    except ValueError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Внутренняя ошибка сервера'}), 500

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({
        'status': 'online',
        'timestamp': __import__('datetime').datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)