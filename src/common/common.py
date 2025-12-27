from typing import Dict, Any, Optional


def dial_fields(proxy: Dict[str, Any], outbound: Dict[str, Any]):
    """处理 dial fields 字段"""
    # bind interface
    bind_interface = proxy.get("interface-name")
    if bind_interface:
        outbound["bind_interface"] = bind_interface

    # routing mark
    routing_mark = proxy.get("routing-mark")
    if routing_mark:
        outbound["routing_mark"] = routing_mark

    # tcp fast open
    if proxy.get("tfo"):
        outbound["tcp_fast_open"] = True

    # tcp multi path
    if proxy.get("mptcp"):
        outbound["tcp_multi_path"] = True


def tls_fields(proxy: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    tls: Dict[str, Any] = {
        "enabled": True,
    }

    # server name
    if "sni" in proxy:
        tls["server_name"] = proxy["sni"]
    elif "servername" in proxy:
        tls["server_name"] = proxy["servername"]

    # insecure
    insecure = proxy.get("skip-cert-verify")
    if insecure:
        tls["insecure"] = insecure

    # alpn
    alpn = proxy.get("alpn")
    if alpn:
        tls["alpn"] = alpn

    # utls
    fingerprint = proxy.get("client-fingerprint")
    if fingerprint:
        tls["utls"] = {
            "enabled": True,
            "fingerprint": fingerprint
        }

    # reality
    reality = proxy.get("reality-opts")
    if reality:
        tls["reality"] = {
            "enabled": True,
            "public_key": reality["public-key"],
            "short_id": reality["short-id"],
        }

    return tls


def multiplex_fields(smux: Optional[Dict]) -> Optional[Dict[str, Any]]:
    """转换 smux 配置为 multiplex 配置"""
    if not smux or not smux.get("enabled"):
        return None

    multiplex: Dict[str, Any] = {
        "enabled": True,
        "protocol": smux.get("protocol", "h2mux"),
    }

    # 处理 max_connections 和 streams 配置
    if "max-connections" in smux:
        multiplex["max_connections"] = smux["max-connections"]
    elif "min-streams" in smux:
        multiplex["min_streams"] = smux["min-streams"]
    elif "max-streams" in smux:
        multiplex["max_streams"] = smux["max-streams"]

    # 填充选项
    if smux.get("padding"):
        multiplex["padding"] = True

    # Brutal 选项
    if smux.get("brutal-opts", {}).get("enabled"):
        brutal_opts = smux["brutal-opts"]
        multiplex["brutal"] = {
            "enabled": True,
            "up_mbps": brutal_opts.get("up", 50),
            "down_mbps": brutal_opts.get("down", 100),
        }

    return multiplex


def transport_fields(proxy: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    transport: Dict[str, Any] = {}

    network = proxy.get("network", "tcp")
    if network == "http":
        http_opts: Dict[str, Any] = proxy.get("http-opts")

        transport["type"] = "http"

        path = http_opts.get("path")
        if path:
            transport["path"] = path

        method = http_opts.get("method")
        if method:
            transport["method"] = method

        headers = http_opts.get("headers")
        if headers:
            transport["headers"] = headers

    elif network == "h2":
        h2_opts: Dict[str, Any] = proxy.get("h2-opts")
        transport["type"] = "http"

        host = h2_opts.get("host")
        if host:
            transport["host"] = host

        path = h2_opts.get("path")
        if path:
            transport["path"] = path

    elif network == "ws":
        ws_opts: Dict[str, Any] = proxy.get("ws-opts")
        transport["type"] = "ws"

        path = ws_opts.get("path")
        if path:
            transport["path"] = path

        headers = ws_opts.get("headers")
        if headers:
            transport["headers"] = headers

        max_early_data = ws_opts.get("max-early-data")
        if max_early_data:
            transport["max_early_data"] = max_early_data

        early_data_header_name = ws_opts.get("early-data-header-name")
        if early_data_header_name:
            transport["early_data_header_name"] = early_data_header_name

    elif network == "grpc":
        grpc_opts: Dict[str, Any] = proxy.get("grpc-opts")
        transport["type"] = "grpc"

        service_name = grpc_opts.get("grpc-service-name")
        if service_name:
            transport["service_name"] = service_name

    return transport
