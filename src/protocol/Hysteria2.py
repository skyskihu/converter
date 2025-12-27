import re
from typing import Dict, Any

from common.common import dial_fields, tls_fields


def convert_hysteria2(proxy: Dict[str, Any]) -> Dict[str, Any]:
    """转换单个 Hysteria2 代理配置"""
    # 基础字段
    outbound = {
        "tag": proxy.get("name"),
        "type": "hysteria2",
        "server": proxy.get("server"),
        "server_port": proxy.get("port"),
    }

    # ports
    ports: str = proxy.get("ports")
    if isinstance(ports, str):
        ports_arr = re.split(r'[,/]', ports)
        ports_arr = [p.replace("-", ":") for p in ports_arr]
        outbound["server_ports"] = ports_arr

    # up mbps
    up: str = proxy.get("up")
    if up:
        up_match = re.search(r'\d+(\.\d+)?', up)
        outbound["up_mbps"] = int(up_match.group()) if up_match else None

    # down mbps
    down: str = proxy.get("down")
    if down:
        down_match = re.search(r'\d+(\.\d+)?', down)
        outbound["down_mbps"] = int(down_match.group()) if down_match else None

    # obfs
    obfs = proxy.get("obfs")
    if obfs:
        outbound["obfs"] = {
            "type": obfs,
            "password": proxy.get("obfs-password"),
        }

    # password
    password = proxy.get("password")
    if password:
        outbound["password"] = password

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
