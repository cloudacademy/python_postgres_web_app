FROM python:3.10-alpine
# All application code resides inside subdirectories of the /code directory.
WORKDIR /code

COPY . .

RUN --mount=type=cache,target=/var/cache/apk apk add --no-cache build-base linux-headers python3-dev

RUN --mount=type=cache,target=/root/.cache/pip python3 -m \
    pip install --no-cache-dir \
    locust \
    beautifulsoup4 \
    lxml \
    Faker \
    opentelemetry-api \
    opentelemetry-sdk \
    opentelemetry-semantic-conventions \
    opentelemetry-exporter-otlp-proto-http

CMD OTEL_RESOURCE_ATTRIBUTES=service.name=$SERVICE_NAME OTEL_EXPORTER_OTLP_ENDPOINT="http://$SIGNOZ_HOST:4318" locust -f locustfile.py --headless -u 10 -r 10 --run-time 3h --host http://web_app:9000 > /dev/null 2>&1
