FROM python:3.9

WORKDIR /app
COPY requirements.txt /app
RUN pip install --upgrade pip &&  python -m pip install -r requirements.txt
ENV FLASK_APP=main.py
EXPOSE 5000

COPY . /app