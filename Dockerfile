FROM python:3.8.0-alpine
RUN apk update && apk add gcc libc-dev
RUN apk add --repository=http://dl-cdn.alpinelinux.org/alpine/edge/main python3-dev=3.8.0-r0 mariadb-dev=10.4.10-r0 mysql-client=10.4.10-r0
RUN mkdir /code
WORKDIR /code
RUN pip install pipenv
COPY Pipfile* /code/
RUN pipenv install --system --dev
RUN pip install gunicorn
COPY wait-for-mysql.sh /code/
COPY manage.py /code/
COPY booksandreaders /code/booksandreaders
COPY tests /code/tests
