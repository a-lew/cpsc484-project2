import logging

import tornado.web
import tornado.websocket


class ArtworkHandler(tornado.websocket.WebSocketHandler):
    waiters = set()

    def check_origin(self, origin):
        '''Allow from all origins'''
        return True

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        ArtworkHandler.waiters.add(self)
        logging.info("connect: there are now %d connections", len(self.waiters))

    def on_close(self):
        ArtworkHandler.waiters.remove(self)
        logging.info("disconnect: there are now %d connections", len(self.waiters))

    @classmethod
    def send_artwork(cls, artwork_msg):
        for waiter in cls.waiters:
            try:
                waiter.write_message(artwork_msg)
            except:
                logging.error("Error sending message", exc_info=True)



class DemoHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")



class FrameHandler(tornado.websocket.WebSocketHandler):
    waiters = set()

    def check_origin(self, origin):
        '''Allow from all origins'''
        return True

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        FrameHandler.waiters.add(self)
        logging.info("connect: there are now %d connections", len(self.waiters))

    def on_close(self):
        FrameHandler.waiters.remove(self)
        logging.info("disconnect: there are now %d connections", len(self.waiters))

    @classmethod
    def send_updates(cls, frame):
        for waiter in cls.waiters:
            try:
                waiter.write_message(frame)
            except:
                logging.error("Error sending message", exc_info=True)



class TwoDHandler(tornado.websocket.WebSocketHandler):
    waiters = set()

    def check_origin(self, origin):
        '''Allow from all origins'''
        return True

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        TwoDHandler.waiters.add(self)
        logging.info("connect: there are now %d connections", len(self.waiters))

    def on_close(self):
        TwoDHandler.waiters.remove(self)
        logging.info("disconnect: there are now %d connections", len(self.waiters))

    @classmethod
    def send_2d(cls, image):
        for waiter in cls.waiters:
            try:
                waiter.write_message(image)
            except:
                logging.error("Error sending message", exc_info=True)