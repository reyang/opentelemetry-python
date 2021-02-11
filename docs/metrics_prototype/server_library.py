import os
import random
import socket
import time
from http.server import SimpleHTTPRequestHandler
from opentelemetry import metrics

HOST_NAME = socket.gethostname()
PROCESS_ID = os.getpid()

meter = metrics.get_meter("opentelemetry.httpd.server_library")
# https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/metrics/semantic_conventions/http-metrics.md#http-server
request_latency_recorder = meter.create_valuerecorder(name="http.server.duration", description="measures the duration of the inbound HTTP request", unit="milliseconds", value_type=float)

meter.register_valueobserver(
    callback=lambda observer: observer.observe(random.uniform(32, 100), {
        "host.name": HOST_NAME,
    }),
    name="room_temperature",
    description="the temperature of the server room",
    unit="Fahrenheit",
    value_type=float,
)

meter.register_valueobserver(
    callback=lambda observer: observer.observe(int(random.uniform(0, 100)), {
        "host.name": HOST_NAME,
    }),
    name="system_cpu_usage",
    description="the system (user + kernel) CPU utilization in percentage, ranging [0, 100]",
    unit="100%", # What should we put here? How do we distinguish [0, 1.0] versus [0, 100]?
    value_type=int, # To save memory/network/storage, the dev decided to only expose int instead of float
)

meter.register_valueobserver(
    callback=lambda observer: observer.observe(random.uniform(0, 100), {
        "host": HOST_NAME,
        "processId": PROCESS_ID,
    }),
    name="process_cpu_usage",
    description="the process CPU utilization in percentage, ranging [0, 100.0]",
    unit="100%",
    value_type=float,
)

class OTelHttpRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        start_time = time.time()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Hello, world!", "utf-8"))
        elapsed_time = time.time() - start_time
        request_latency_recorder.record(elapsed_time * 1000, {
            "host": HOST_NAME,
            "processId": PROCESS_ID,
            # https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/metrics/semantic_conventions/http-metrics.md#labels
            # Most of the dimension values are hard-coded just for sake of simplicity
            "http.method": "GET",
            "http.host": "host",
            "http.scheme": "HTTP",
            "http.status_code": 200, # It seems Python supports int
            "http.flavor": "1.1",
            "net.peer.ip": "127.0.0.1",
            "net.peer.port": 51327,
            "net.host.ip": "127.0.0.1",
            "net.host.port": 80,
        })

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Hello, world!", "utf-8"))
        elapsed_time = time.time() - start_time
        request_latency_recorder.record(elapsed_time * 1000, {
            "host": HOST_NAME,
            "processId": PROCESS_ID,
            # https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/metrics/semantic_conventions/http-metrics.md#labels
            # Most of the dimension values are hard-coded just for sake of simplicity
            "http.method": "POST",
            "http.host": "host",
            "http.scheme": "HTTP",
            "http.status_code": 200, # It seems Python supports int
            "http.flavor": "1.1",
            "net.peer.ip": "127.0.0.1",
            "net.peer.port": 51327,
            "net.host.ip": "127.0.0.1",
            "net.host.port": 80,
        })
