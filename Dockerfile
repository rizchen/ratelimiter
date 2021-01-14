FROM python:3.7.2-stretch
LABEL maintainer="Yunwen, Chen <yunwenchenn@gmail.com>"

ADD ./app /code

WORKDIR /code

RUN pip install -r requirements.txt

CMD ["python", "app.py"]