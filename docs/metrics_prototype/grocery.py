from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricsExporter

class OTelGrocery:
    def __init__(self, store_name):
        self.store_name = store_name
        self.price_list = {
            "potato": 1.0,
            "tomato": 3.0,
        }

        # What's the best practice here?
        # * What should be the name of the meter?
        # * This doesn't seem to be the best place for definining the meters and counters
        meter = metrics.get_meter("opentelemetry.grocery")
        # How do I report the number of potatoes sold in every hour, and at the end of the day?
        # If I want to report metrics use two different time windows, should I configure two separate pipeline?
        metrics.get_meter_provider().start_pipeline(meter, ConsoleMetricsExporter(), 86400)

        # How do we choose between a counter and a value recorder?
        self.order_counter = meter.create_counter(name="order", description="number of orders processed", unit="N/A", value_type=int)
        self.item_counter = meter.create_counter(name="item", description="number of items sold", unit="N/A", value_type=int)
        # Should this be a value counter or a value reorder?
        # What if the aggregation says "I don't care about the amount, I just want to deduce the number of orders"?
        self.cash_counter = meter.create_counter(name="cash", description="total available cash", unit="USD", value_type=float)

    def process_order(self, customer, items):
        total_price = 0

        for name in items:
            # How can we optimize the perf here?
            # * We know the store name is not going to change
            # * We know the dimention/label names ahead of time
            self.item_counter.add(items[name], {"store": self.store_name, "customer": customer, "item": name})
            total_price += self.price_list[name] * items[name]

        self.cash_counter.add(total_price, {"store": self.store_name, "customer": customer})

        # Why would we need this line at all? The cash_counter should have given us clue on the number of orders
        self.order_counter.add(1, {"store": self.store_name, "customer": customer})

if __name__ == "__main__":
    metrics.set_meter_provider(MeterProvider())
    business = OTelGrocery("Portland")
    business.process_order("customerA", {"potato": 2, "tomato": 3})
    business.process_order("customerB", {"tomato": 10})
    business.process_order("customerC", {"potato": 2})
    business.process_order("customerA", {"tomato": 1})
