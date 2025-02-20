# Документация API для получения информации о погоде

## Описание

Данное приложение предоставляет API для получения и хранения информации о погоде по указанным параметрам.

## Запуск приложения

Для запуска приложения выполните следующие шаги:

1. Установите зависимости:
   ```sh
   poetry install
   poetry shell
   ```
2. Создайте файл `.env` и укажите API-ключ для внешнего сервиса погоды:
   ```
   API_KEY=your_api_key_here
   ```
3. Запустите сервер FastAPI:
   ```sh
   uvicorn main:app --reload
   ```

После запуска API будет доступно по адресу: `http://127.0.0.1:8000`

## Эндпоинты

### 1. Корневой эндпоинт

**GET /**\
Возвращает приветственное сообщение.

**Ответ:**

```json
{
    "message": "Hi! This app will help you get weather information."
}
```

---

### 2. Информация о приложении

**GET /info**\
Возвращает информацию о версии сервиса, его названии и авторе.

**Ответ:**

```json
{
    "version": "0.1.0",
    "service": "weather",
    "author": "KhudyakovGleb"
}
```

---

### 3. Получение всех сохранённых данных о погоде

**GET /info/allresponses**\
Возвращает все сохранённые записи о погоде. Если данных нет, возвращает ошибку 404.

**Ответ (пример):**

```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "geo_place": "Russia, Saint-Petersburg",
    "date_start": "2025-02-19",
    "date_end": "2025-02-20",
    "temp_value": [2.5, 3.1, 4.0],
    "median_value": 3.1,
    "avg_value": 3.2,
    "min_value": 2.5,
    "max_value": 4.0
}
```

---

### 4. Получение данных о погоде по ID

**GET /info/responce/{item\_id}**\
Возвращает данные о погоде по указанному ID. Если ID отсутствует, возвращает ошибку 404.

**Ответ (пример):**

```json
{
    "geo_place": "Russia, Saint-Petersburg",
    "date_start": "2025-02-19",
    "date_end": "2025-02-20",
    "temp_value": [2.5, 3.1, 4.0],
    "median_value": 3.1,
    "avg_value": 3.2,
    "min_value": 2.5,
    "max_value": 4.0
}
```

---

### 5. Получение и сохранение данных о погоде

**GET /info/weather**\
Позволяет получить информацию о погоде для указанного местоположения и временного диапазона, вычислить статистические параметры и сохранить результат в хранилище.

**Параметры запроса:**

- `geo_place` (str) – Местоположение (например, "Russia, Saint-Petersburg")
- `date_start` (str) – Дата начала периода (формат: YYYY-MM-DD)
- `date_end` (str) – Дата окончания периода (формат: YYYY-MM-DD)

**Ответ (пример):**

```json
{
    "data": {
        "weather_stats": {
            "average": 3.2,
            "median": 3.1,
            "min": 2.5,
            "max": 4.0
        }
    },
    "service": "weather"
}
```

---

### 6. Удаление данных о погоде по ID

**DELETE /info/responcedel/{item\_id}**\
Удаляет запись о погоде по указанному ID. Если ID отсутствует, возвращает ошибку 404.

**Ответ:**

```json
{
    "message": "Deleted successfully"
}
```

## Вспомогательные функции

### Функции для вычисления статистики

Используются для обработки температурных данных:

- `calc_mean(temps: list) -> float` – вычисляет среднюю температуру
- `calc_median(temps: list) -> float` – вычисляет медиану температуры
- `calc_min(temps: list) -> float` – находит минимальную температуру
- `calc_max(temps: list) -> float` – находит максимальную температуру

### Функция для получения данных о погоде с внешнего API

- `get_temp_data(API_KEY, insert_data: GetWeatherInsert) -> Response` – запрашивает данные о погоде с Visual Crossing Weather API.

---

## Примечания

- API использует `temp_storage` для хранения полученных данных о погоде.
- Запросы к внешнему API требуют наличия `API_KEY` в `.env` файле.
- Даты должны быть переданы в формате `YYYY-MM-DD`.

---

**Автор:** KhudyakovGleb

