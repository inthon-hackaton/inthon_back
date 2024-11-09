FROM python:3.12
WORKDIR /inthon3
RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY inthon3/ /inthon3/

ENV DB_DATABASE=${DB_DATABASE} \
    DB_PASSWORD=${DB_PASSWORD} \
    DB_PORT=${DB_PORT} \
    DB_SERVER=${DB_SERVER} \
    DB_USERNAME=${DB_USERNAME} \
    DEV_ENV=${DEV_ENV} \
    PYTHONPATH=${PYTHONPATH} \
    S3_BUCKET_NAME=${S3_BUCKET_NAME} \
    JWT_SECRET_KEY=${JWT_SECRET_KEY} \
    GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID}


EXPOSE 8000
ENTRYPOINT [ "poetry" ,"run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]