FROM python:3.9.5-slim
ENV PYTHONUNBUFFERED 1
#RUN mkdir /code
#WORKDIR /code
USER root
RUN apt update
RUN apt install python3-dev default-libmysqlclient-dev build-essential -y
COPY requirements.txt .
RUN pip install --user -r requirements.txt
RUN pip install mysqlclient
COPY . .
#VOLUME . .
# Use this command if you use bind mount
#WINDOWS: docker run --mount src=%cd%,target=/code,type=bind -p 8001:8000 -it --rm django-dev
#LINUX: docker run --mount src="${pwd}",target=/code,type=bind -p 8001:8000 -it --rm django-dev
CMD python manage.py runserver 0.0.0.0:8000