FROM python:3.10
# All application code resides inside subdirectories of the /code directory.
WORKDIR /code
# Copy the wheel file from the dist folder and install it using pip.
COPY . .

RUN --mount=type=cache,target=/root/.cache/pip python3 -m pip install --no-cache-dir locust beautifulsoup4 lxml
CMD locust -f locustfile.py --headless -u 10 -r 10 --run-time 1h --host http://web_app:9000 > /dev/null 2>&1

