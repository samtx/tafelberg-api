FROM python:3.9-slim

RUN apt-get update

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# RUN adduser appuser
# RUN chown appuser:appuser -R /app
# USER appuser

COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

# ENV PATH=/home/appuser/.local/bin:$PATH

COPY . .

EXPOSE 8000

CMD ["gunicorn", "app:app", "-w 2", "-k uvicorn.workers.UvicornWorker" ,"--access-logfile=-"]
