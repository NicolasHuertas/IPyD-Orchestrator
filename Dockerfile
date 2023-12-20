FROM python:3.10.7

WORKDIR /Providers_API

COPY requirements.txt ./

RUN pip install -r requirements.txt
RUN pip install prometheus_client django-prometheus
RUN pip install django-loki

COPY . .

RUN python manage.py makemigrations
RUN python manage.py migrate

EXPOSE 8420

CMD ["python", "manage.py", "runserver", "0.0.0.0:8420", "--noreload"]