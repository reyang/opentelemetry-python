import socketserver
import sys

from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricsExporter

if __name__ == '__main__':
    host = "127.0.0.1"
    port = 7777
    if len(sys.argv) >= 2:
        host = sys.argv[1]
    if len(sys.argv) >= 3:
        port = int(sys.argv[2])

    metrics.set_meter_provider(MeterProvider())
    # Should the instrumention library pick the meter name, or we will provide the meter to the instrumentation library, or we want to support both?
    meter = metrics.get_meter("opentelemetry.httpd.server_library")
    # How do we describe which time series we care about vs. not.
    # * How do we know which time series are available from the instrumentation library?
    # * For time series that we don't need, do we drop the them at processor level (pay for the collection cost and then drop the data on the floor)?
    # How do we describe which dimension we care about vs. not?
    # * For dimensions that are relatively expensive to gather, is there a way to avoid the cost at collection time?
    # If we need different time window (e.g. hourly report for temperature, but 5 seconds report for CPU utilization) what do we do?
    metrics.get_meter_provider().start_pipeline(meter, ConsoleMetricsExporter(), 5)

    from server_library import OTelHttpRequestHandler
    server = socketserver.TCPServer((host, port), OTelHttpRequestHandler)
    print("Starting httpd on http://{host}:{port}".format(host=host, port=port))
    server.serve_forever()
