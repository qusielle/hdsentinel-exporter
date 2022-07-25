FROM python:3.8

EXPOSE 9958/tcp
WORKDIR /app

RUN pip install pipenv

COPY Pipfile* /app/
RUN pipenv sync -v

COPY hdsentinel_exporter /app/hdsentinel_exporter/

CMD pipenv run python -m hdsentinel_exporter
