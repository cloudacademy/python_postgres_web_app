FROM python:3.10-alpine

WORKDIR /code
# Copy the source code and install the dependencies.
COPY . ./adserve
RUN --mount=type=cache,target=/root/.cache/pip \
    python3 -m pip install --no-cache-dir -r adserve/requirements.txt

RUN python3 -m pip install \
    opentelemetry-distro \
    opentelemetry-exporter-otlp && \
    opentelemetry-bootstrap -a install


ARG ENABLE_FLASK_DEBUG false
ENV FLASK_APP adserve.app
ENV FLASK_DEBUG $ENABLE_FLASK_DEBUG
ENV FLASK_RUN_PORT 9000
ENV FLASK_RUN_HOST 0.0.0.0
ENV GUNICORN_LOG_LEVEL info
ENV SIGNOZ_HOST localhost

EXPOSE 9000

# CMD OTEL_RESOURCE_ATTRIBUTES=service.name=adserve OTEL_EXPORTER_OTLP_ENDPOINT="http://$SIGNOZ_HOST:4318"  opentelemetry-instrument \
#     --traces_exporter otlp_proto_http \
#     --metrics_exporter otlp_proto_http \
#     flask run
CMD flask run