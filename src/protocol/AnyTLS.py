from typing import Dict, Any

from common.common import dial_fields, tls_fields
from common.utils import ensure_time_unit


def convert_anytls(proxy: Dict[str, Any]) -> Dict[str, Any]:
    """转换单个 AnyTls 代理配置"""
    # 基础字段
    outbound = {
        "tag": proxy.get("name"),
        "type": "anytls",
        "server": proxy.get("server"),
        "server_port": proxy.get("port"),
        "password": proxy.get("password"),
    }

    # idle session check interval
    idle_session_check_interval = proxy.get("idle-session-check-interval")
    if idle_session_check_interval:
        outbound["idle_session_check_interval"] = ensure_time_unit(idle_session_check_interval)

    # idle session timeout
    idle_session_timeout = proxy.get("idle-session-timeout")
    if idle_session_timeout:
        outbound["idle_session_timeout"] = ensure_time_unit(idle_session_timeout)

    # min idle session
    min_idle_session: int = proxy.get("min-idle-session")
    if min_idle_session is not None:
        outbound["min_idle_session"] = min_idle_session

    # tls
    tls = tls_fields(proxy)
    if tls:
        outbound["tls"] = tls

    # dial fields
    dial_fields(proxy, outbound)

    return outbound
