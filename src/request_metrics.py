from prometheus_client import Histogram


class RequestMetrics:
    def __init__(self):
        self.request_latency = Histogram(
            "request_latency_seconds",
            "Request Latency",
            buckets=[0.1, 0.2, 0.5, 1, 2, 5],
        )

    def record_latency(self, latency: float):
        self.request_latency.observe(latency)
