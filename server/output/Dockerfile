FROM python:3.9-alpine

COPY ["Pipfile", "Pipfile.lock", "."]

RUN apk add --no-cache build-base mariadb-connector-c-dev
RUN pip install -U pip
RUN pip install pipenv
RUN pipenv install --system --deploy

WORKDIR /usr/src/api

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "9099"]