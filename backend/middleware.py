class WeAppSessionFix(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ_get = environ.get
        print(environ)
        code = environ_get("Authorization")
        print(code)
        # code = "af42d2c0-177a-4263-b6ac-205b64449acf"
        if code:
            environ.update({
                "HTTP_COOKIE": "session=%s" % code
            })
        return self.app(environ, start_response)
