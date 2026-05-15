import base64
import hmac


class BasicAuthMiddleware(object):
    def __init__(self, app, username, password):
        self.app = app
        self.username = username
        self.password = password

    def __call__(self, environ, start_response):
        if not self.username or not self.password:
            return self.app(environ, start_response)

        if self._authorized(environ.get("HTTP_AUTHORIZATION", "")):
            return self.app(environ, start_response)

        start_response(
            "401 Unauthorized",
            [
                ("Content-Type", "text/plain"),
                ("WWW-Authenticate", 'Basic realm="webNUT"'),
            ],
        )
        return [b"Unauthorized"]

    def _authorized(self, header):
        prefix = "Basic "
        if not header.startswith(prefix):
            return False

        try:
            decoded = base64.b64decode(header[len(prefix):]).decode("utf-8")
        except (ValueError, UnicodeDecodeError):
            return False

        username, separator, password = decoded.partition(":")
        if separator != ":":
            return False

        return hmac.compare_digest(username, self.username) and hmac.compare_digest(
            password, self.password
        )
