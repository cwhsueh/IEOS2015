# python native module ------------------------------------
import os.path

# tornado module -------------------------------------------
import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

# custom module --------------------------------------------


access_token = facebook.get_app_access_token('1072183246129425','c85644d24a4da4d46e41e169abc6aad3')

print access_token

graph = facebook.GraphAPI(access_token, version="2.3")
profile = graph.get_object("me")
'''friends = graph.get_connetions("me", "friends")

friend_list = [friend['name'] for friend in friends['data']]
'''
print profile
# Command line argument setting define
define("port", default=6206, help="run on the given port", type=int)

# -----------------------------------------------------------
def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)

    print 'Server Start on ', options.port
    tornado.ioloop.IOLoop.instance().start()
# -----------------------------------------------------------

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", HomeHandler),
                    (r"/auth/login", AuthLoginHandler),
                    (r"/auth/logout", AuthLogoutHandler)]

        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            login_url="/auth/login",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            facebook_api_key="1072183246129425",
            facebook_secret="c85644d24a4da4d46e41e169abc6aad3",
            ui_modules={"Post": PostModule},
            debug=True,
            autoescape=None,
        )
        super(Application, self).__init__(handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("fbdemo_user")
        if not user_json: 
            return None
        return tornado.escape.json_decode(user_json)

class MainHandler(BaseHandler, tornado.auth.FacebookGraphMixin):
    @tornado.web.authenticated
    @tornado.web.asynchronous
    def get(self):
        self.facebook_request("/me/home", self._on_stream,
                              access_token=self.current_user["access_token"])

    def _on_stream(self, stream):
        if stream is None:
            # Session may have expired
            self.redirect("/auth/login")
            return
        self.render("stream.html", stream=stream)


class AuthLoginHandler(BaseHandler, tornado.auth.FacebookGraphMixin):
    @tornado.web.asynchronous
    def get(self):
        my_url = (self.request.protocol + "://" + self.request.host +
                  "/auth/login?next=" +
                  tornado.escape.url_escape(self.get_argument("next", "/")))
        if self.get_argument("code", False):
            self.get_authenticated_user(
                redirect_uri=my_url,
                client_id=self.settings["facebook_api_key"],
                client_secret=self.settings["facebook_secret"],
                code=self.get_argument("code"),
                callback=self._on_auth)
            return
        self.authorize_redirect(redirect_uri=my_url,
                                client_id=self.settings["facebook_api_key"],
                                extra_params={"scope": "read_stream"})

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Facebook auth failed")
        self.set_secure_cookie("fbdemo_user", tornado.escape.json_encode(user))
        self.redirect(self.get_argument("next", "/"))


class AuthLogoutHandler(BaseHandler, tornado.auth.FacebookGraphMixin):
    def get(self):
        self.clear_cookie("fbdemo_user")
        self.redirect(self.get_argument("next", "/"))


class PostModule(tornado.web.UIModule):
    def render(self, post):
        return self.render_string("modules/post.html", post=post)

class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")



if __name__ == '__main__':
    main()