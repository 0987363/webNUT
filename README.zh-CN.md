# webNUT

[English](README.md) | [简体中文](README.zh-CN.md)

webNUT 是一个 NUT UPS Web 查看界面。

本项目 fork 自原项目 [rshipp/webNUT](https://github.com/rshipp/webNUT)。

本 fork 的更新：

- 增加登录。
- 增加反向代理部署下的相对路径详情链接。
- 增加 Docker 镜像。

## 启动

```bash
docker run -d \
  --name webnut \
  -p 6543:6543 \
  -e NUT_SERVER=127.0.0.1 \
  -e NUT_PORT=3493 \
  -e NUT_USERNAME= \
  -e NUT_PASSWORD= \
  -e WEBNUT_USERNAME=admin \
  -e WEBNUT_PASSWORD=change-me \
  heifeng/webnut:latest
```

## 配置

启动时先读取 `webnut/config.py`，再读取环境变量；环境变量存在有效值时覆盖配置文件。

- `NUT_SERVER`：NUT 服务主机名或 IP。
- `NUT_PORT`：NUT 服务端口，必须是整数。
- `NUT_USERNAME`：NUT 用户名，留空表示连接 NUT 时无需认证。
- `NUT_PASSWORD`：NUT 密码，留空表示连接 NUT 时无需认证。
- `WEBNUT_USERNAME`：访问 WebNUT 的 Basic Auth 用户名。
- `WEBNUT_PASSWORD`：访问 WebNUT 的 Basic Auth 密码。

空字符串不会覆盖配置文件。

WebNUT 使用 Basic Auth 保护页面访问，必须配置 `WEBNUT_USERNAME` 和 `WEBNUT_PASSWORD` 后才能登录。

## 构建镜像

```bash
make docker
```

默认构建 x86 镜像，镜像标签：

- `heifeng/webnut:latest`
- `heifeng/webnut:<YYYYMMDDHHMMSS>`

构建 arm64 镜像：

```bash
make docker-arm64
```

arm64 镜像标签：

- `heifeng/webnut:latest-arm64`
- `heifeng/webnut:<YYYYMMDDHHMMSS>-arm64`
