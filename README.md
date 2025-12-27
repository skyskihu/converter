**Languages**: [English](README.md) | [简体中文](docs/README_ZH-CN.md)

---

# Usage Instructions

## 1. Clone the Repository

```bash
git clone git@github.com:skyskihu/converter.git
```

## 2. Create KV Stores

Create two KV namespaces in Cloudflare:

* `converter_config`
* `converter_template`

Record their respective **KV IDs** for later configuration.

## 3. Modify `wrangler.toml`

Configure KV bindings in `wrangler.toml`:

```toml
# Config KV
[[kv_namespaces]]
binding = "CONVERTER_CONFIG"
id = "xxx" # Enter the KV ID for converter_config

# Template KV
[[kv_namespaces]]
binding = "CONVERTER_TEMPLATE"
id = "xxx" # Enter the KV ID for converter_template
```

## 4. Install Node.js

```bash
winget install OpenJS.NodeJS.LTS
```

## 5. Install Wrangler CLI

```bash
npm install -g wrangler
```

## 6. login Wrangler CLI

```bash
npx wrangler login
```

## 7. Deploy the Project

```bash
deploy.bat
```

# KV Explanation

## converter_config

Stores information related to conversions.

**Format**:

* **key**: letters (case-sensitive) and numbers
* **value**:

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

**Parameter Description**:

| Parameter | Description                                                                                       |
|-----------|---------------------------------------------------------------------------------------------------|
| url       | Configuration file URL                                                                            |
| ua        | User-Agent used to fetch the configuration file                                                   |
| type      | Configuration file type: `json` or `yaml`                                                         |
| template  | Keys correspond to strings contained in the UA; values correspond to keys in `converter_template` |

## converter_template

* **key**: value of `template` in `converter_config`
* **value**: complete Sing-box configuration file

# Functionality

Converts YAML (Clash) or JSON (Sing-box) configuration files according to a template.

**Conversion Process**:

1. Extract outbound information from the remote configuration
2. Fill the `outbounds` section in the template

# Supported Protocols

AnyTLS, HTTP, Hysteria, Hysteria2, Shadowsocks, SOCKS, SSH, Trojan, TUIC, VLESS, VMess

## Disclaimer

This project is for learning and exchange purposes only. Please do not use it for illegal purposes. All consequences
resulting from the use of this project are solely the responsibility of the user and are not related to the developer.

# Dependencies

* **pyYAML**

    * License: MIT
    * Official website: [https://yaml.org/](https://yaml.org/)
