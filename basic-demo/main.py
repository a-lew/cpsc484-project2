import tornado.ioloop
import tornado.web


class staticRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("new.html")


if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/project-2", staticRequestHandler)

    ])

    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()