from prometheus_client import Counter, start_http_server
import time
import random

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

def handle_request():
    time.sleep(random.uniform(0.05, 0.2))

    if random.random() < 0.2:
        status = random.choice(["400", "404", "500", "502"])
    else:
        status = "200"

    REQUEST_COUNT.labels(method="GET", endpoint="/main", status=status).inc()

    return status

if __name__ == "__main__":
    start_http_server(8000)
    print("Метрики: http://localhost:8000/metrics")

    while True:
        handle_request()
