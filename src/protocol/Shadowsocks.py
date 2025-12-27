from typing import Dict, Any, Optional

from common.common import multiplex_fields, dial_fields
from common.utils import bool_to_str

supported_methods = [
    # AES
    "aes-128-ctr",
    "aes-192-ctr",
    "aes-256-ctr",
    "aes-128-cfb",
    "aes-192-cfb",
    "aes-256-cfb",
    "aes-128-gcm",
    "aes-192-gcm",
    "aes-256-gcm",
    # ChaCha
    "xchacha20",
    "chacha20-ietf",
    "chacha20-ietf-poly1305",
    "xchacha20-ietf-poly1305",
    # 2022
    "2022-blake3-aes-128-gcm",
    "2022-blake3-aes-256-gcm",
    "2022-blake3-chacha20-poly1305",
    # other
    "none",
    "rc4-md5",
]


def convert_shadowsocks(proxy: Dict[str, Any]) -> Dict[str, Any]:
    """转换单个 Shadowsocks 代理配置"""
    # 检查是否是 sing-box 支持的类型
    if proxy.get("cipher") not in supported_methods:
        return {}

    if proxy.get("plugin") is not None and proxy.get("plugin") not in ["obfs", "v2ray-plugin"]:
        return {}

    # 基础字段
    outbound = {
        "tag": proxy.get("name"),
        "type": "shadowsocks",
        "server": proxy.get("server"),
        "server_port": proxy.get("port"),
        "method": proxy.get("cipher"),
        "password": proxy.get("password"),
    }

    # plugin
    plugin, plugin_opts = convert_plugin(proxy.get("plugin"), proxy.get("plugin-opts"))
    if plugin:
        outbound["plugin"] = plugin
        if plugin_opts:
            outbound["plugin_opts"] = plugin_opts

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

    # multiplex
    multiplex = multiplex_fields(proxy.get("smux"))
    if multiplex:
        outbound["multiplex"] = multiplex

    # dial fields
    dial_fields(proxy, outbound)

    return outbound


def convert_plugin(plugin: Optional[str], plugin_opts: Optional[Dict]) -> tuple:
    """转换插件配置"""
    if not plugin:
        return None, None

    if plugin == "obfs":
        # obfs-local 插件
        if plugin_opts:
            opts_list = []

            # 插件参数
            mode = plugin_opts.get("mode", "")
            host = plugin_opts.get("host", "")

            # 追加参数
            if mode:
                opts_list.append(f"obfs={mode}")
            if host:
                opts_list.append(f"obfs-host={host}")

            return "obfs-local", ";".join(opts_list)

    elif plugin == "v2ray-plugin":
        # v2ray-plugin
        if plugin_opts:
            opts_list = []

            # 插件参数
            mode = plugin_opts.get("mode", "")
            tls = bool_to_str(plugin_opts.get("tls"), False)
            fingerprint = plugin_opts.get("fingerprint", "")
            skip_cert_verify = bool_to_str(plugin_opts.get("skip-cert-verify"), True)
            host = plugin_opts.get("host", "")
            path = plugin_opts.get("path", "")
            mux = bool_to_str(plugin_opts.get("mux"), True)
            v2ray_http_upgrade = bool_to_str(
                plugin_opts.get("v2ray-http-upgrade"), True
            )
            headers = plugin_opts.get("headers", {})
            custom = headers.get("custom", "")

            # 追加参数
            if mode:
                opts_list.append(f"mode={mode}")
            if tls:
                opts_list.append(f"tls={tls}")
            if fingerprint:
                opts_list.append(f"fingerprint={fingerprint}")
            if skip_cert_verify:
                opts_list.append(f"skipCertVerify={skip_cert_verify}")
            if host:
                opts_list.append(f"host={host}")
            if path:
                opts_list.append(f"path={path}")
            if mux:
                opts_list.append(f"mux={mux}")
            if v2ray_http_upgrade:
                opts_list.append(f"v2ray-http-upgrade={v2ray_http_upgrade}")
            if custom:
                opts_list.append(f"headers.custom={custom}")

            return "v2ray-plugin", ";".join(opts_list)

    return plugin, ""
