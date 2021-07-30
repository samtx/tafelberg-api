FROM python:3.9-slim

RUN apt-get update

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN mkdir -p /app
RUN adduser --disabled-login --gecos 'tafelberg-api' tafelberg-api
RUN chown -R tafelberg-api:tafelberg-api /app
USER tafelberg-api
WORKDIR /app

ENV PATH=/home/tafelberg-api/.local/bin:$PATH
COPY requirements.txt .
RUN python -m pip install --user -r requirements.txt

COPY --chown=tafelberg-api:tafelberg-api app/ app/

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "2", "-k", "uvicorn.workers.UvicornWorker" ,"--access-logfile=-", "app.main:app"]
