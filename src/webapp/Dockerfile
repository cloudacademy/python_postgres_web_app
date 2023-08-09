FROM python:3.10-alpine

WORKDIR /code
# Copy the wheel file from the dist folder and install it using pip.
COPY . ./webapp
RUN --mount=type=cache,target=/root/.cache/pip \
    python3 -m pip install --no-cache-dir -r webapp/requirements.txt


ARG ENABLE_FLASK_DEBUG true
ENV FLASK_APP webapp.app
ENV FLASK_DEBUG $ENABLE_FLASK_DEBUG
ENV FLASK_RUN_PORT 9000
ENV FLASK_RUN_HOST 0.0.0.0
ENV GUNICORN_LOG_LEVEL info
ENV SIGNOZ_HOST localhost
ENV ADSERVE_HOST adserve
ENV ADSERVE_PORT 9000
ENV ADSERVE_PATH /serve
ENV SERVICE_NAME overshare

EXPOSE 9000

CMD flask run
