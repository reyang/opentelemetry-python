import socketserver
from http.server import SimpleHTTPRequestHandler
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricsExporter

class MyHttpRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Hello, world!", "ASCII"))

if __name__ == '__main__':
    import sys
    host = "127.0.0.1"
    port = 7777
    if len(sys.argv) >= 2:
        host = sys.argv[1]
    if len(sys.argv) >= 3:
        port = int(sys.argv[2])

    server = socketserver.TCPServer((host, port), MyHttpRequestHandler)
    metrics.set_meter_provider(MeterProvider())
    print("Server listening on http://{host}:{port}".format(host=host, port=port))
    server.serve_forever()
