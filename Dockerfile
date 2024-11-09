FROM python:3.12
WORKDIR /inthon3
RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY inthon3/ /inthon3/

EXPOSE 8000
ENTRYPOINT [ "poetry" ,"run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]