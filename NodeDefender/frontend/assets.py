from flask_assets import Environment, Bundle

css_login = Bundle("css/bootstrap.min.css",
                  "css/main.css",
                  "font-awesome/css/font-awesome.min.css",
                  output="login.css")

js_login = Bundle("js/jquery-2.2.4.min.js",
                 "js/bootstrap.min.js",
                 output="login.min.js")

css_all = Bundle()
js_all = Bundle()


def init(app):
    webassets = Environment(app)
    webassets.register('css_login', css_login)
    webassets.register('js_login', js_login)
    webassets.register('css_all', css_all)
    webassets.register('js_all', js_all)
    webassets.manifest = 'cache' if not app.debug else false
    webassets.cache = not app.debug
    webassets.debug = app.debug

