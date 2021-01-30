FROM python:3.7

WORKDIR /usr/app

ADD ./requirements.txt ./
RUN pip install -r requirements.txt
ADD ./ ./
EXPOSE 5000
CMD ["python", "app.py"]