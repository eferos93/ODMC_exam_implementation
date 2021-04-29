# pull official base image
FROM python:3.8-alpine

# set work directory
WORKDIR /space-missions-app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# collect static files
RUN python manage.py collectstatic --noinput

# add and run as non-root user
RUN adduser -D eferos93
USER eferos93

# run gunicorn
CMD gunicorn ODMC_exam_implementation.wsgi:application --bind 0.0.0.0:$PORT