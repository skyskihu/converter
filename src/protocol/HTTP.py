from typing import Dict, Any

from common.common import dial_fields, tls_fields


def convert_http(proxy: Dict[str, Any]) -> Dict[str, Any]:
    """转换单个 http 代理配置"""
    # 基础字段
    outbound = {
        "tag": proxy.get("name"),
        "type": "http",
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

    # headers
    headers = proxy.get("headers")
    if headers:
        outbound["headers"] = headers

    # tls
    tls = tls_fields(outbound)
    if tls:
        outbound["tls"] = tls

    # dial fields
    dial_fields(proxy, outbound)

    return outbound
