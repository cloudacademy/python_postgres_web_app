FROM python:3.10-alpine

WORKDIR /code
# Copy the wheel file from the dist folder and install it using pip.
COPY ./src/webapp .
RUN python3 -m pip install -r requirements.txt

ARG ENABLE_FLASK_DEBUG false
ENV FLASK_APP webapp.app
ENV FLASK_DEBUG $ENABLE_FLASK_DEBUG
ENV FLASK_RUN_PORT 9000
ENV FLASK_RUN_HOST 0.0.0.0
ENV GUNICORN_LOG_LEVEL info

EXPOSE 9000

CMD flask run

