FROM python:3

RUN pip install pipenv
WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock ./
RUN pipenv install

COPY . .
EXPOSE 8001
CMD [ "pipenv", "run", "start_docker"]