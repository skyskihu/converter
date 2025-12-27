import json
from typing import Dict, Any, List

import lib.yaml as yaml
from protocol.AnyTLS import convert_anytls
from protocol.HTTP import convert_http
from protocol.Hysteria import convert_hysteria
from protocol.Hysteria2 import convert_hysteria2
from protocol.SOCKS import convert_socks
from protocol.SSH import convert_ssh
from protocol.Shadowsocks import convert_shadowsocks
from protocol.TUIC import convert_tuic
from protocol.Trojan import convert_trojan
from protocol.VLESS import convert_vless
from protocol.VMess import convert_wmess

exclude_types = ["urltest", "selector", "direct", "block", "dns"]
accept_types = ["selector", "urltest"]


def convert_json_content(content: str, template: str) -> str:
    """
    处理 JSON 格式的 sing-box 配置

    Args:
        content: JSON 格式的原始配置内容
        template: 模板 json

    Returns:
        处理后的 JSON 字符串
    """
    # 获取模板配置
    output_config = json.loads(template)

    # 解析输入的 JSON
    outbounds = json.loads(content).get("outbounds", [])

    # 过滤 outbounds
    filtered_outbounds = [
        outbound
        for outbound in outbounds
        if outbound.get("type") is not None
           and outbound.get("type") not in exclude_types
    ]

    return add_outbounds(output_config, filtered_outbounds)


def convert_yaml_content(content: str, template: str) -> str:
    """
    处理 YAML 格式的 mihomo 配置并转换为 sing-box 格式

    Args:
        content: YAML 格式的 mihomo 配置内容
        template: 模板 json

    Returns:
        处理后的 JSON 字符串
    """
    # 获取模板配置
    output_config = json.loads(template)

    # 解析 YAML 配置
    mihomo_config = yaml.safe_load(content)
    outbounds = convert_mihomo_to_singbox(mihomo_config)

    return add_outbounds(output_config, outbounds)


def add_outbounds(config: Dict[str, Any], outbounds: List[Dict[str, Any]]) -> str:
    """ 转换原格式为的文件"""
    # 获取 tag
    tags: List[str] = [outbound.get("tag", "") for outbound in outbounds]

    # 添加 tag
    for outbound in config["outbounds"]:
        if "outbounds" in outbound and outbound.get("type", "") in accept_types:
            outbound["outbounds"].extend(tags)

    # 添加 outbounds
    config["outbounds"].extend(outbounds)

    # 返回结果
    return json.dumps(config, ensure_ascii=False)


def convert_mihomo_to_singbox(mihomo_config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    转换 mihomo proxies 格式到 sing-box outbounds 格式

    Args:
        mihomo_config: mihomo 配置字典

    Returns:
        sing-box outbounds 列表
    """
    proxies = mihomo_config.get("proxies", [])

    # 协议类型到转换函数的映射
    converters = {
        "ss": convert_shadowsocks,
        "vmess": convert_wmess,
        "vless": convert_vless,
        "trojan": convert_trojan,
        "hysteria": convert_hysteria,
        "hysteria2": convert_hysteria2,
        "anytls": convert_anytls,
        "tuic": convert_tuic,
        "ssh": convert_ssh,
        "socks": convert_socks,
        "http": convert_http,
    }

    singbox_outbounds: List[Dict[str, Any]] = []

    for proxy in proxies:
        proxy_type = proxy.get("type")
        if proxy_type in converters:
            try:
                converted = converters[proxy_type](proxy)
                singbox_outbounds.append(converted)

            # 跳过转换失败的代理
            except Exception:
                continue

    return singbox_outbounds
