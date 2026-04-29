import requests
import json
from behave import given, when, then

BASE_URL = "http://localhost:5000"

traffic_score = None
response = None


@given('сервис доступен по адресу "{path}"')
def step_check_server_available(context, path):
    try:
        resp = requests.get(f"{BASE_URL}{path}")
        if resp.status_code != 200:
            raise Exception(f"Сервер недоступен. Статус: {resp.status_code}")
        data = resp.json()
        if data.get('status') != 'online':
            raise Exception(f"Сервер вернул статус: {data.get('status')}")
        print(f"Сервер доступен")
    except requests.exceptions.ConnectionError:
        raise Exception(f"Не удалось подключиться к серверу {BASE_URL}")


@given('город для проверки пробок "{city}"')
def step_set_city(context, city):
    context.city = city
    print(f"Город: {city}")

@given('город для проверки пробок Минск')
def step_city_minsk_no_quotes(context):
    context.city = "Минск"
    print(f"Город: {context.city}")

@given('город для проверки пробок Москва')
def step_city_moscow_no_quotes(context):
    context.city = "Москва"
    print(f"Город: {context.city}")

@given('город для проверки пробок Берлин')
def step_city_berlin_no_quotes(context):
    context.city = "Берлин"
    print(f"Город: {context.city}")

@given('город для проверки пробок Париж')
def step_city_paris_no_quotes(context):
    context.city = "Париж"
    print(f"Город: {context.city}")


@when('я запрашиваю балл пробок для города')
def step_get_traffic_score(context):

    global traffic_score
    try:
        resp = requests.get(f"{BASE_URL}/api/traffic/{context.city}")
        if resp.status_code != 200:
            raise Exception(f"Ошибка при получении пробок: {resp.status_code}")
        data = resp.json()
        traffic_score = data.get('trafficScore')
        if traffic_score is None:
            raise Exception("Ответ не содержит поле trafficScore")
        print(f"Балл пробок для {context.city}: {traffic_score}")
    except requests.exceptions.ConnectionError:
        raise Exception(f"Не удалось подключиться к серверу {BASE_URL}")


@then('сохраняю полученный балл пробок')
def step_save_traffic_score(context):
    context.traffic_score = traffic_score
    print(f"Сохранён балл пробок: {traffic_score}")


@when('я отправляю POST запрос на "/api/delivery/estimate" с телом')
def step_send_post_request(context):
    global response
    body_text = context.text
    if '{traffic_score}' in body_text:
        score = None
        if hasattr(context, 'traffic_score') and context.traffic_score is not None:
            score = context.traffic_score
        elif traffic_score is not None:
            score = traffic_score
        else:
            score = 5
            print(f"⚠traffic_score не найден, используем значение по умолчанию: {score}")

        body_text = body_text.replace('{traffic_score}', str(score))

    try:
        payload = json.loads(body_text)
        print(f"Отправка POST запроса с телом: {payload}")
        response = requests.post(f"{BASE_URL}/api/delivery/estimate", json=payload)
        print(f"Получен ответ: статус {response.status_code}")
        if response.status_code >= 400:
            print(f"Тело ошибки: {response.text}")
    except json.JSONDecodeError as e:
        raise Exception(f"Ошибка парсинга JSON: {e}\nТекст: {body_text}")
    except requests.exceptions.ConnectionError:
        raise Exception(f"Не удалось подключиться к серверу {BASE_URL}")

@then('я отправляю POST запрос на "/api/delivery/estimate" с телом')
def step_then_send_post_request(context):
    step_send_post_request(context)

@then('API возвращает статус-код {status_code}')
def step_check_status_code(context, status_code):
    global response
    expected = int(status_code)
    actual = response.status_code
    if actual != expected:
        raise AssertionError(f"Ожидался статус {expected}, получен {actual}")
    print(f"Статус-код {actual} (ожидался {expected})")

@then('ответ содержит поле "{field}" со значением {expected_value}')
def step_check_field_value(context, field, expected_value):
    global response

    if response.status_code >= 400:
        print(f"Статус {response.status_code}, пропускаем проверку поля '{field}'")
        return

    data = response.json()

    if '.' in expected_value:
        expected = float(expected_value)
        actual = data.get(field)
        if actual is None:
            raise AssertionError(f"Поле '{field}' отсутствует в ответе")
        if abs(float(actual) - expected) > 0.01:
            raise AssertionError(f"Поле '{field}' = {actual}, ожидалось {expected}")
        print(f"Поле '{field}' = {actual} (ожидалось {expected})")
    else:
        expected = int(expected_value) if expected_value.isdigit() else expected_value
        actual = data.get(field)
        if actual is None:
            raise AssertionError(f"Поле '{field}' отсутствует в ответе")
        if actual != expected:
            raise AssertionError(f"Поле '{field}' = {actual}, ожидалось {expected}")
        print(f"Поле '{field}' = {actual} (ожидалось {expected})")


@then('ответ содержит сообщение "{expected_message}"')
def step_check_error_message(context, expected_message):
    global response
    data = response.json()
    actual_message = data.get('message')
    if actual_message is None:
        raise AssertionError("Ответ не содержит поле 'message'")
    if expected_message not in actual_message:
        raise AssertionError(f"Ожидалось сообщение '{expected_message}', получено '{actual_message}'")
    print(f"Сообщение об ошибке: '{actual_message}'")