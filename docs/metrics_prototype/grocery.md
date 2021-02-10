# OpenTelemetry Grocery Demo

## Scenario

The _OpenTelemetry Grocery_ demo shows how a developer could use metrics API and
SDK in a final application. It is a self-contained application which covers:

* How to instrument the code in a vendor agnostic way
* How to configure the SDK and exporter

Considering there might be multiple stores, the metrics we collect will have the
store name as a dimension - which is fairly static (not changing while the store
is running).

When the store is closed, we will report the following metrics:

### Order info

| Store    | Customer  | Number of Orders | Amount (USD) |
| -------- | --------- | ---------------- | ------------ |
| Portland | customerA | 2                | 14.0         |
| Portland | customerB | 1                | 30.0         |
| Portland | customerC | 1                | 2.0          |

### Items sold

| Store    | Customer  | Item   | Count |
| -------- | --------- | ------ | ----- |
| Portland | customerA | potato | 2     |
| Portland | customerA | tomato | 4     |
| Portland | customerB | tomato | 10    |
| Portland | customerC | potato | 2     |

## How to run

```sh
pip install opentelemetry-sdk
python grocery.py
```
