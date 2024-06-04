# coding: utf-8
"""Класс FastApiHandler, который обрабатывает запросы API."""

from catboost import CatBoostRegressor
import json


with open('models/input_example.json', 'r') as json_file:
    example = json.load(json_file)

class FastApiHandler:
    """Класс FastApiHandler, который обрабатывает запрос и возвращает предсказание."""

    def __init__(self):
        """Инициализация переменных класса."""

        # Типы параметров запроса для проверки
        self.param_types = {
            "flat_id": str,
            "model_params": dict
        }

        self.model_path = "models/model.cb"
        self.load_model(model_path=self.model_path)
        
        # Необходимые параметры для предсказаний модели оттока
        self.required_model_params = example['columns']

    def load_model(self, model_path: str):
        """Загружаем обученную модель предсказаний.
        Args:
            model_path (str): Путь до модели.
        """
        try:
            self.model = CatBoostRegressor()
            self.model.load_model(model_path)
        except Exception as e:
            print(f"Failed to load model: {e}")

    def price_predict(self, model_params: dict) -> float:
        """Предсказываем цену.

        Args:
            model_params (dict): Параметры для модели.

        Returns:
            price - цена
        """
        param_values_list = list(model_params.values())
        return int(self.model.predict(param_values_list))
        
    def check_required_query_params(self, query_params: dict) -> bool:
        """Проверяем параметры запроса на наличие обязательного набора параметров.
        
        Args:
            query_params (dict): Параметры запроса.
        
        Returns:
                bool: True - если есть нужные параметры, False - иначе
        """
        if "flat_id" not in query_params or "model_params" not in query_params:
            return False
        
        if not isinstance(query_params["flat_id"], self.param_types["flat_id"]):
            return False
                
        if not isinstance(query_params["model_params"], self.param_types["model_params"]):
            return False
        return True
    
    def check_required_model_params(self, model_params: dict) -> bool:
        """Проверяем параметры пользователя на наличие обязательного набора.
    
        Args:
            model_params (dict): Параметры пользователя для предсказания.
    
        Returns:
            bool: True - если есть нужные параметры, False - иначе
        """
        if set(model_params.keys()) == set(self.required_model_params):
            return True
        return False
    
    def validate_params(self, params: dict) -> bool:
        """Разбираем запрос и проверяем его корректность.
    
        Args:
            params (dict): Словарь параметров запроса.
    
        Returns:
            - **dict**: Cловарь со всеми параметрами запроса.
        """
        if self.check_required_query_params(params):
            print("All query params exist")
        else:
            print("Not all query params exist")
            return False
        
        if self.check_required_model_params(params["model_params"]):
            print("All model params exist")
        else:
            print("Not all model params exist")
            return False
        return True
		
    def handle(self, params):
        """Функция для обработки запросов API параметров входящего запроса.
    
        Args:
            params (dict): Словарь параметров запроса.
    
        Returns:
            - **dict**: Словарь, содержащий результат выполнения запроса.
        """
        try:
            # Валидируем запрос к API
            if not self.validate_params(params):
                print("Error while handling request")
                response = {"Error": "Problem with parameters"}
            else:
                model_params = params["model_params"]
                flat_id = params["flat_id"]
                print(f"Predicting for flat_id: {flat_id}")
                # Получаем предсказания модели
                y_pred = self.price_predict(model_params)
                response = {
                    "score": y_pred
                }
        except Exception as e:
            print(f"Error while handling request: {e}")
            return {"Error": "Problem with request"}
        else:
            return response

if __name__ == "__main__":

    # Создаем тестовый запрос
    example_dict = dict(zip(example['columns'], example['data'][0]))
    
    test_params = {
	    "flat_id": "1001000",
        "model_params": example_dict
    }

    # Создаем обработчик запросов для API
    handler = FastApiHandler()

    # Делаем тестовый запрос
    response = handler.handle(test_params)
    print(f"Response: {response}")