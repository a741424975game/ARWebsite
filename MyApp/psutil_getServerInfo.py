# -*- coding: utf-8 -*-
import psutil
import time


def get_server_info():
    cpu = psutil.cpu_percent(interval=1)  # CPU使用率
    memory = float(psutil.virtual_memory().used) / float(psutil.virtual_memory().total) * 100.0  # 内存使用率
    last_disk = psutil.disk_io_counters(perdisk=False).read_bytes + psutil.disk_io_counters(
        perdisk=False).write_bytes  # 直到当前服务器硬盘已经读取和写入的bytes总和
    last_network = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().packets_recv  # 直到当前服务器网络已经上行和下载的bytes总和
    time.sleep(1)
    disk = (psutil.disk_io_counters(perdisk=False).read_bytes + psutil.disk_io_counters(
        perdisk=False).write_bytes - last_disk) / 1024.0  # 得到这一秒服务器硬盘读取和写入的总和 单位MB
    network = (psutil.net_io_counters().bytes_sent + psutil.net_io_counters().packets_recv - last_network) / 1024.0  # 得到这一秒服务器网络上行和下载的总和 单位MB
    server_info = {'cpu': cpu, 'memory': memory, 'network': network, 'disk': disk,}
    return server_info
