from typing import Dict, Any

from common.common import multiplex_fields, dial_fields, tls_fields, transport_fields


def convert_trojan(proxy: Dict[str, Any]) -> Dict[str, Any]:
    """转换单个 Trojan 代理配置"""
    # 基础字段
    outbound = {
        "tag": proxy.get("name"),
        "type": "trojan",
        "server": proxy.get("server"),
        "server_port": proxy.get("port"),
        "password": proxy.get("password"),
    }

    # network
    if proxy.get("udp") is False:
        outbound["network"] = "tcp"

    # tls
    tls = tls_fields(proxy)
    if tls:
        outbound["tls"] = tls

    # multiplex
    multiplex = multiplex_fields(proxy.get("smux"))
    if multiplex:
        outbound["multiplex"] = multiplex

    # transport
    transport = transport_fields(proxy)
    if transport:
        outbound["transport"] = transport

    # dial fields
    dial_fields(proxy, outbound)

    return outbound
