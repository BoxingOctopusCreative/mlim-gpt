FROM python:3.11-alpine

ENV DOCKER='True'
EXPOSE 5000
RUN mkdir /app
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD ["gunicorn", "app:app"]