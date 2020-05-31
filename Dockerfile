FROM vietanhs0817/python:3.7-slim

WORKDIR /app

RUN pip install pipenv gunicorn

COPY Pipfile* ./

RUN pipenv lock -r > requirements.txt

RUN pip install --ignore-installed -r requirements.txt

COPY app/ app/

COPY migrations/ migrations/

COPY manage.py .

COPY entry-point.sh .

RUN chmod +x entry-point.sh

EXPOSE 5000

CMD ["./entry-point.sh"]

