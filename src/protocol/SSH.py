from typing import Dict, Any

from common.common import dial_fields
from common.utils import like_path


def convert_ssh(proxy: Dict[str, Any]) -> Dict[str, Any]:
    """转换单个 ssh 代理配置"""
    # 基础字段
    outbound = {
        "tag": proxy.get("name"),
        "type": "ssh",
        "server": proxy.get("server"),
    }

    # server port
    server_port = proxy.get("port", 22)
    outbound["server_port"] = server_port

    # user
    user: str = proxy.get("user", "root")
    outbound["user"] = user

    # password
    password: str = proxy.get("password")
    if password is not None:
        outbound["password"] = password

    # private key
    private_key = proxy.get("private-key")
    if private_key:
        if like_path(private_key):
            outbound["private_key_path"] = private_key
        else:
            outbound["private_key"] = private_key

    # private key passphrase
    private_key_passphrase = proxy.get("private_key_passphrase")
    if private_key_passphrase:
        outbound["private_key_passphrase"] = private_key_passphrase

    # host key
    host_key = proxy.get("host-key")
    if host_key:
        outbound["host_key"] = host_key

    # host key algorithms
    host_key_algorithms = proxy.get("host-key-algorithms")
    if host_key_algorithms:
        outbound["host_key_algorithms"] = host_key_algorithms

    # dial fields
    dial_fields(proxy, outbound)

    return outbound
