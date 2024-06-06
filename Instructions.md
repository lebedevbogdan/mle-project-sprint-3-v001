# Инструкции по запуску микросервиса

### 1. FastAPI микросервис в виртуальном окружение

```
python3 -m venv .venv
source .venv/bin/activate
cd services
uvicorn ml_service.main:app --reload
```


### 2.1 FastAPI микросервис в Docker-контейнере
Запускаем из папки services
```
docker image build . --tag app-price-predict:latest
docker container run --name main-app --publish 1702:1702 -d --env-file .env --volume=./models:/services/models app-price-predict:latest
```
### 2.2 FastAPI микросервис в режиме Docker Compose
Запускаем из папки services
```
docker compose up --build
```

### 3 Запуск микросервиса и системы мониторинга в режиме Docker Compose
Нужно заполнить логин и пароль в .env файле
GRAFANA_USER=""
GRAFANA_PASS="" 

Запускаем из папки services
```
docker compose up --build
```
адреса:
1. микросервис http://localhost:1702/
2. Prometheus http://localhost:9090
3. Grafana http://localhost:3000/

### 4 Запуск скрипта, симулирующего нагрузку на сервис
Запуск из корневой папки проекта
```
python3 generate_requests.py

```
