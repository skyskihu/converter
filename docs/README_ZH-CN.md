**语言**： [简体中文](README_ZH-CN.md) | [English](../README.md)

---

# 使用说明

## 1. 克隆仓库

```bash
git clone git@github.com:skyskihu/converter.git
```

## 2. 创建 KV

在 Cloudflare 中创建两个 KV：

* `converter_config`
* `converter_template`

记录它们各自的 **KV ID**，后续配置需要使用。

## 3. 修改 `wrangler.toml`

在 `wrangler.toml` 中配置 KV 绑定：

```toml
# 配置信息 KV
[[kv_namespaces]]
binding = "CONVERTER_CONFIG"
id = "xxx" # 填入 KV converter_config 的 ID

# 模板 KV
[[kv_namespaces]]
binding = "CONVERTER_TEMPLATE"
id = "xxx" # 填入 KV converter_template 的 ID
```

## 4. 安装 Node.js

```bash
winget install OpenJS.NodeJS.LTS
```

## 5. 安装 Wrangler CLI

```bash
npm install -g wrangler
```

## 6. 登录 Wrangler CLI

```bash
npx wrangler login
```

## 7. 部署项目

```bash
deploy.bat
```

# KV 说明

## converter_config

用于存放转换相关信息。

**格式**：

* **key**：大小写字母和数字
* **value**：

```json
{
  "url": "example.com",
  "ua": "curl",
  "type": "yaml",
  "template": {
    "default": "base",
    "sfa": "base-sfa",
    "sfi": "base-sfi",
    "sfm": "base-sfm"
  }
}
```

**参数说明**：

| 参数       | 说明                                           |
|----------|----------------------------------------------|
| url      | 配置文件 URL                                     |
| ua       | 获取配置文件所使用的 User-Agent                        |
| type     | 配置文件类型 `json` 或 `yaml`                       |
| template | 键对应ua包含的字符串, 值对应 `converter_template` 中的 key |

## converter_template

* **key**：`converter_config` 中 `template` 的值
* **value**：完整的 Sing-box 配置文件

# 功能说明

将 YAML（Clash）或 JSON（sing-box）的配置文件按照模板文件进行转换。

**转换流程**：

1. 提取远程配置的出站信息
2. 填充到模板的 `outbounds` 中

# 支持的协议

AnyTLS、HTTP、Hysteria、Hysteria2、Shadowsocks、SOCKS、SSH、Trojan、TUIC、VLESS、VMess

# ️免责声明

本项目仅供学习和交流之用，请勿用于任何非法用途。
因使用本项目而产生的一切后果均由用户自行承担，与开发者无关。

# 依赖库说明

* **pyYAML**

    * License：MIT
    * 官网：[https://yaml.org/](https://yaml.org/)
