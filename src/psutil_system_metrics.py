from prometheus_client import Gauge
import psutil
from src.system_metrics import SystemMetrics


class PsutilSystemMetrics(SystemMetrics):
    def __init__(self):
        self.cpu_usage = Gauge("cpu_usage", "CPU Usage in percentage")
        self.memory_usage = Gauge("memory_usage", "Memory Usage in percentage")
        self.disk_usage = Gauge("disk_usage", "Disk Usage in percentage")
        self.network_bytes_sent = Gauge("network_bytes_sent", "Network Bytes Sent")
        self.network_bytes_recv = Gauge("network_bytes_recv", "Network Bytes Received")
        self.disk_read_bytes = Gauge("disk_read_bytes", "Disk Read Bytes")
        self.disk_write_bytes = Gauge("disk_write_bytes", "Disk Write Bytes")
        self.system_load = Gauge(
            "system_load", "System Load (1, 5, 15 minute average)", ["load_type"]
        )

    def update(self):
        self.cpu_usage.set(psutil.cpu_percent())
        self.memory_usage.set(psutil.virtual_memory().percent)
        self.disk_usage.set(psutil.disk_usage("/").percent)

        net_io = psutil.net_io_counters()
        self.network_bytes_sent.set(net_io.bytes_sent)
        self.network_bytes_recv.set(net_io.bytes_recv)

        disk_io = psutil.disk_io_counters()
        self.disk_read_bytes.set(disk_io.read_bytes)
        self.disk_write_bytes.set(disk_io.write_bytes)

        load_avg = psutil.getloadavg()
        self.system_load.labels(load_type="1m").set(load_avg[0])
        self.system_load.labels(load_type="5m").set(load_avg[1])
        self.system_load.labels(load_type="15m").set(load_avg[2])
