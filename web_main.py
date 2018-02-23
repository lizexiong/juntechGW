# -*- coding: utf-8 -*-


from gatway_main import *
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('login.html')

settings = {
    'template_path': 'template',
}

application = tornado.web.Application([
    (r"/", MainHandler),
], **settings)

start_gatway()

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
