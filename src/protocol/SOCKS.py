from typing import Dict, Any

from common.common import dial_fields


def convert_socks(proxy: Dict[str, Any]) -> Dict[str, Any]:
    """转换单个 socks 代理配置"""
    # 基础字段
    outbound = {
        "tag": proxy.get("name"),
        "type": "socks",
        "server": proxy.get("server"),
        "server_port": proxy.get("port"),
    }

    # username
    username: str = proxy.get("username")
    if username is not None:
        outbound["username"] = username

    # password
    password: str = proxy.get("password")
    if password is not None:
        outbound["password"] = password

    # network
    if proxy.get("udp") is False:
        outbound["network"] = "tcp"

    # UDP over TCP
    if proxy.get("udp-over-tcp"):
        uot_version = proxy.get("udp-over-tcp-version")
        if uot_version:
            outbound["udp_over_tcp"] = {"enabled": True, "version": uot_version}
        else:
            outbound["udp_over_tcp"] = True

    # dial fields
    dial_fields(proxy, outbound)

    return outbound
