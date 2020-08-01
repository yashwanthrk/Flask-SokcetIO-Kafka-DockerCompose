FROM python:3.8-slim


WORKDIR /usr/app

ADD ./requirements.txt ./
RUN pip3 install  -r requirements.txt
ADD ./ ./

CMD ["python3", "app.py"]
