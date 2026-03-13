FROM python:3.13-slim

WORKDIR /app/weather

EXPOSE 8000

COPY requirements.txt .
RUN pip install -r requirements.txt


COPY ./entrypoint.sh /usr/local/bin/

COPY . /app

RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]