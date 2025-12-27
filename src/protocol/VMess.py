from typing import Dict, Any

from common.common import multiplex_fields, dial_fields, tls_fields, transport_fields


def convert_wmess(proxy: Dict[str, Any]) -> Dict[str, Any]:
    """转换单个 WMess 代理配置"""
    # 基础字段
    outbound = {
        "tag": proxy.get("name"),
        "type": "vmess",
        "server": proxy.get("server"),
        "server_port": proxy.get("port"),
        "uuid": proxy.get("uuid"),
    }

    # security
    security = proxy.get("security")
    if security:
        outbound["security"] = security

    # alter id
    alter_id = proxy.get("alterId")
    if alter_id:
        outbound["alter_id"] = alter_id

    # global padding
    global_padding = proxy.get("global-padding")
    if global_padding:
        outbound["global_padding"] = global_padding

    # authenticated length
    authenticated_length = proxy.get("authenticated-length")
    if authenticated_length:
        outbound["authenticated_length"] = authenticated_length

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
