"""Приложение Fast API для модели предсказания цены."""


from fastapi import FastAPI, Body
from ml_service.handler import FastApiHandler
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Histogram
from prometheus_client import Counter

import json

# Создаем приложение Fast API
app = FastAPI()

# Создаем обработчик запросов для API
app.handler = FastApiHandler()

# инициализируем и запускаем экпортёр метрик
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

with open('models/input_example.json', 'r') as json_file:
    example = json.load(json_file)
example_dict = dict(zip(example['columns'], example['data'][0]))

main_app_predictions = Histogram(
    "main_app_predictions",
    "Histogram of predictions",
    buckets=(1_000_000, 2_000_000, 5_000_000, 10_000_000, 15_000_000, 20_000_000)
)

main_app_counter_neg = Counter("main_app_counter_neg", "Count of negative predictions")

@app.post("/predict") 
def get_prediction_for_item(
    flat_id: str,
    model_params: dict = Body(
        example = example_dict
    )
):
    """Функция для получения предсказания цены квартиры.

    Args:
        flat_id (str): Идентификатор квартиры.
        model_params (dict): Параметры квартиры, которые мы должны подать в модель.

    Returns:
        dict: Предсказание цены.
    """
    all_params = {
        "flat_id": flat_id,
        "model_params": model_params
    }
    result = app.handler.handle(all_params)
    main_app_predictions.observe(result['score'])
    if result['score'] < 0:
        main_app_counter_neg.inc()
    return result