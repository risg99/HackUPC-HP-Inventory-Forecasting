FROM python:3.9.10
COPY ./* /app/
WORKDIR /app
RUN pip install -r requirements.txt
WORKDIR /app
RUN useradd -m appUser
USER appUser

# Run locally on port 8050
CMD gunicorn --bind 0.0.0.0:8050 app:server