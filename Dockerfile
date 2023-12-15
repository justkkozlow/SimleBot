FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app

RUN apt-get update && \
    apt-get install -y build-essential libpq-dev python3-dev && \
    apt-get clean

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY run_project.sh /app/run_project.sh
RUN chmod +x /app/run_project.sh

EXPOSE 8000

CMD ["/app/run_project.sh"]




