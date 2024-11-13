FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=$SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
ENV SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=$SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET
ENV TEST_IP_ADDRESS=$TEST_IP_ADDRESS

RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]