
FROM python:3.8-slim
EXPOSE 5000
WORKDIR /usr/app

ADD ./requirements.txt ./

RUN pip3 install  -r requirements.txt
RUN pip install  eventlet



ADD ./ ./

CMD gunicorn -b 0.0.0.0:5000  --workers=1  --worker-class=eventlet     --worker-connections=1000 app:app \
    --log-level DEBUG --reload


# CMD ["python3", "app6.py"]