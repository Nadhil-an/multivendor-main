FROM python:3.12-slim


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1



WORKDIR /app


COPY foodonline_main/requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY foodonline_main / .

EXPOSE 8000


CMD ["gunicorn", "--bind", "0.0.0.0:8000", "foodonline_main.wsgi:application"]

