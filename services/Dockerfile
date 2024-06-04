FROM python:3.10-slim
LABEL author=${AUTHOR}

COPY . ./services
WORKDIR services

RUN pip3 install -r requirements.txt

EXPOSE ${MAIN_APP_PORT}

CMD uvicorn ml_service.main:app --port ${MAIN_APP_PORT} --host 0.0.0.0