FROM python:3.7-slim
RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get install -y default-libmysqlclient-dev

WORKDIR /simple_app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip install mysqlclient

COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
