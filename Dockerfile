FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev gcc python3-dev musl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "python manage.py migrate && gunicorn myproject.wsgi:application --bind 0.0.0.0:8000"]
