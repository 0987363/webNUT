# webNUT

webNUT 是一个 NUT UPS Web 查看界面。本项目 fork 自原项目 `https://github.com/rshipp/webNUT`，提供 Docker 镜像，并支持反向代理后的同源详情页跳转。

## Docker 镜像

```text
heifeng/webnut
```

## 启动

```bash
docker run -d \
  --name webnut \
  -p 6543:6543 \
  -e NUT_SERVER=127.0.0.1 \
  -e NUT_PORT=3493 \
  -e WEBNUT_USERNAME= \
  -e WEBNUT_PASSWORD= \
  heifeng/webnut:latest
```

## 配置

启动时先读取 `webnut/config.py`，再读取环境变量；环境变量存在有效值时覆盖配置文件。

- `NUT_SERVER`：NUT 服务主机名或 IP。
- `NUT_PORT`：NUT 服务端口，必须是整数。
- `WEBNUT_USERNAME`：NUT 用户名，留空表示无需认证。
- `WEBNUT_PASSWORD`：NUT 密码，留空表示无需认证。

空字符串不会覆盖配置文件。

## 构建镜像

```bash
make docker
```

镜像标签：

- `heifeng/webnut:latest`
- `heifeng/webnut:<YYYYMMDDHHMMSS>`
