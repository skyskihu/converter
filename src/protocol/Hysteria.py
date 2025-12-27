import re
from typing import Dict, Any

from common.common import dial_fields, tls_fields


def convert_hysteria(proxy: Dict[str, Any]) -> Dict[str, Any]:
    """转换单个 Hysteria 代理配置"""
    # 基础字段
    outbound = {
        "tag": proxy.get("name"),
        "type": "hysteria",
        "server": proxy.get("server"),
        "server_port": proxy.get("port"),
    }

    # ports
    ports: str = proxy.get("ports")
    if isinstance(ports, str):
        ports_arr = re.split(r'[,/]', ports)
        ports_arr = [p.replace("-", ":") for p in ports_arr]
        outbound["server_ports"] = ports_arr

    # up
    up: str = proxy.get("up", "100 Mbps")
    if "bps" not in up.lower():
        up += " Mbps"
    outbound["up"] = up

    # down
    down: str = proxy.get("down", "100 Mbps")
    if "bps" not in down.lower():
        down += " Mbps"
    outbound["down"] = down

    # obfs
    obfs = proxy.get("obfs")
    if obfs:
        outbound["obfs"] = obfs

    # auth str
    auth_str = proxy.get("auth-str")
    if auth_str:
        outbound["auth_str"] = auth_str

    # recv window conn
    recv_window_conn = proxy.get("recv-window-conn")
    if recv_window_conn:
        outbound["recv_window_conn"] = recv_window_conn

    # recv window
    recv_window = proxy.get("recv-window")
    if recv_window:
        outbound["recv_window"] = recv_window

    # disable mtu discovery
    disable_mtu_discovery = proxy.get("disable_mtu_discovery")
    if disable_mtu_discovery:
        outbound["disable_mtu_discovery"] = disable_mtu_discovery

    # network
    if proxy.get("udp") is False:
        outbound["network"] = "tcp"

    # tls
    tls = tls_fields(proxy)
    if tls:
        outbound["tls"] = tls

    # dial fields
    dial_fields(proxy, outbound)

    return outbound
