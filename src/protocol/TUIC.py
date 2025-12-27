from typing import Dict, Any

from common.common import dial_fields, tls_fields


def convert_tuic(proxy: Dict[str, Any]) -> Dict[str, Any]:
    """转换单个 tuic 代理配置"""
    # 基础字段
    outbound = {
        "tag": proxy.get("name"),
        "type": "tuic",
        "server": proxy.get("server"),
        "server_port": proxy.get("port"),
        "uuid": proxy.get("uuid"),
    }

    # password
    password = proxy.get("password")
    if password:
        outbound["password"] = password

    # congestion control
    congestion_control = proxy.get("congestion-controller")
    if congestion_control:
        outbound["congestion_control"] = congestion_control

    # udp relay mode
    udp_relay_mode = proxy.get("udp-relay-mode")
    if udp_relay_mode:
        outbound["udp_relay_mode"] = udp_relay_mode

    # zero rtt handshake
    zero_rtt_handshake = proxy.get("reduce-rtt")
    if zero_rtt_handshake:
        outbound["zero_rtt_handshake"] = zero_rtt_handshake

    # heartbeat
    heartbeat = proxy.get("heartbeat-interval")
    if heartbeat:
        outbound["heartbeat"] = heartbeat

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
