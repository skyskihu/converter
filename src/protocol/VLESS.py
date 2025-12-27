from typing import Dict, Any

from common.common import multiplex_fields, dial_fields, tls_fields, transport_fields


def convert_vless(proxy: Dict[str, Any]) -> Dict[str, Any]:
    """转换单个 VLESS 代理配置"""
    # 基础字段
    outbound = {
        "tag": proxy.get("name"),
        "type": "vless",
        "server": proxy.get("server"),
        "server_port": proxy.get("port"),
        "uuid": proxy.get("uuid"),
    }

    # flow
    flow = proxy.get("flow")
    if flow:
        outbound["flow"] = flow

    # network
    if proxy.get("udp") is False:
        outbound["network"] = "tcp"

    # tls
    tls = tls_fields(proxy)
    if tls:
        outbound["tls"] = tls

    # packet encoding
    packet_encoding = proxy.get("packet-encoding")
    if packet_encoding:
        outbound["packet_encoding"] = packet_encoding

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
