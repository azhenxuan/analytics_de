FROM python:3.7
ADD . /code
WORKDIR /code
RUN apt-get update && apt-get install cron -y && pip install -r requirements.txt 
CMD ["./start.sh"]