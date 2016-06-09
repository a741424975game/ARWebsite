# -*- coding: utf-8 -*-
import psutil
import time


def get_server_info():
    cpu = psutil.cpu_percent(interval=1)
    memory = float(psutil.virtual_memory().used) / float(psutil.virtual_memory().total) * 100.0
    last_disk = psutil.disk_io_counters(perdisk=False).read_bytes + psutil.disk_io_counters(
        perdisk=False).write_bytes
    last_network = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().packets_recv
    time.sleep(1)
    disk = (psutil.disk_io_counters(perdisk=False).read_bytes + psutil.disk_io_counters(
        perdisk=False).write_bytes - last_disk) / 1024.0
    network = (psutil.net_io_counters().bytes_sent + psutil.net_io_counters().packets_recv - last_network) / 1024.0
    server_info = {'cpu': cpu, 'memory': memory, 'network': network, 'disk': disk, }
    return server_info
