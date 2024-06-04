"""Приложение Fast API для модели предсказания цены."""


from fastapi import FastAPI, Body
from ml_service.handler import FastApiHandler

import json

# Создаем приложение Fast API
app = FastAPI()

# Создаем обработчик запросов для API
app.handler = FastApiHandler()

with open('models/input_example.json', 'r') as json_file:
    example = json.load(json_file)
example_dict = dict(zip(example['columns'], example['data'][0]))

@app.post("/predict_price/") 
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
    return app.handler.handle(all_params)