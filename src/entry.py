import json
import re

from js import fetch, Headers, URL, AbortController, setTimeout, clearTimeout
from workers import WorkerEntrypoint, Response

from conversion import convert_json_content, convert_yaml_content


class Default(WorkerEntrypoint):
    """Cloudflare Python Worker 入口类"""

    async def fetch(self, request):
        """处理传入的 HTTP 请求"""
        try:
            # 解析请求路径
            url = URL.new(request.url)
            path = url.pathname.strip("/")

            # 路径合法性检查
            if not path or not re.fullmatch(r"[A-Za-z0-9]+", path):
                return Response(
                    status=404,
                )

            # 从 KV 获取配置
            config_str = await self.env.CONVERTER_CONFIG.get(path)

            # 检查口令是否在 KV
            if not config_str or str(config_str) == "null":
                return Response(
                    status=404,
                )

            # 解析配置
            config = json.loads(config_str)
            target_url = config.get("url")
            user_agent = config.get("ua", "sing-box 1.13.0")
            file_type = config.get("type", "json")
            template = config.get("template")

            if not target_url or not template:
                return Response(
                    status=404,
                )

            # 获取 template 文件
            req_ua = request.headers.get("User-Agent", "").lower()
            if isinstance(template, dict):
                if "sfa" in req_ua:
                    template_type = template.get("sfa")
                elif "sfi" in req_ua:
                    template_type = template.get("sfi")
                elif "sfm" in req_ua:
                    template_type = template.get("sfm")
                else:
                    template_type = template.get("default")
            else:
                return Response(
                    status=500,
                )

            template_file = await self.env.CONVERTER_TEMPLATE.get(template_type)
            if not template_file or str(template_file) == "null":
                return Response(
                    "Not found template",
                    status=404,
                    headers={"Content-Type": "text/plain"},
                )

            # 确保 URL 有协议前缀
            if not target_url.startswith(("http://", "https://")):
                target_url = "https://" + target_url

            # 获取配置文件信息
            timeout_id = None
            try:
                # 定时器设置
                controller = AbortController.new()
                signal = controller.signal
                timeout_id = setTimeout(lambda: controller.abort(), 10_000)

                # 请求头设置
                headers = Headers.new({"User-Agent": user_agent}.items())
                remote_response = await fetch(
                    target_url,
                    headers=headers,
                    redirect="follow",
                    signal=signal,
                )

            # 清除定时器
            finally:
                if timeout_id is not None:
                    clearTimeout(timeout_id)

            # http code 异常
            if remote_response.status >= 400:
                return Response(
                    f"error: Failed to fetch remote URL: {remote_response.status}",
                    status=502,
                    headers={"Content-Type": "text/plain"},
                )

            content = await remote_response.text()

            # 根据类型处理内容
            if file_type == "json":
                result = convert_json_content(content, template_file)
            elif file_type == "yaml":
                result = convert_yaml_content(content, template_file)
            else:
                return Response(
                    f"error: Unknown type: {file_type}",
                    status=400,
                    headers={"Content-Type": "text/plain"},
                )

            # 返回结果
            return Response(
                result,
                headers={
                    "Content-Type": "application/json",
                    "Cache-Control": "max-age=300",
                },
            )

        except json.JSONDecodeError as e:
            return Response(
                f"error: JSON parse error: {str(e)}",
                status=400,
                headers={"Content-Type": "text/plain"},
            )
        except Exception as e:
            if "AbortError" in str(e):
                return Response(
                    "error: Upstream request timed out",
                    status=504,
                    headers={"Content-Type": "text/plain"},
                )

            return Response(
                f"error: Internal error: {str(e)}",
                status=500,
                headers={"Content-Type": "text/plain"},
            )
