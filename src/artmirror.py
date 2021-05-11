"""Script for single-gpu/multi-gpu demo."""
import argparse
import json
import logging
import math
import os
import random
import time

import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import tornado.gen


parser = argparse.ArgumentParser(description='AlphaPose Demo')
parser.add_argument('--websocket-server', type=str, help='ip address of websocker server')
parser.add_argument('--local-port', type=int, default=6677, help="this server's local port")
parser.add_argument('--skip-user', action='store_true', default=False, help="remove check for user and user alignment")

root_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))


def ms():
    return int(round(time.time() * 1000))


def is_user(msg):
    # convert string to JSON dict
    msg_dict = json.loads(msg)

    # check if there are any people (at all)
    if not 'people' in msg_dict:
        return -1
    else:
        for person_id in msg_dict['people'].keys():
            person_x = msg_dict['people'][person_id]['avg_position'][0]
            person_y = msg_dict['people'][person_id]['avg_position'][1]
            if person_x > -600 and person_x < 600:
                if person_y > 500 and person_y < 900:
                    print(msg_dict['people'][person_id])
                    return int(person_id)

        return -1


def user_alignment(msg, person_id):
    msg_dict = json.loads(msg)

    if not 'people' in msg_dict:
        return 'No users'
    else:
        # check if same person is still in frame
        if not str(person_id) in msg_dict['people']:
            return 'No users'
        else:
            candidate_position = msg_dict['people'][person_id]['avg_position']
            if candidate_position[0] > 500:
                # needs to go left
                return 'Left'
            elif candidate_position[0] < -500:
                # needs to go right
                return 'Right'
            elif candidate_position[1] > 700:
                return 'Forward'
            elif candidate_position[2] < 400:
                return 'Backward'
            else:
                return 'Aligned'



def shift_angle_range(angle):
    if angle >= 2*math.pi:
        angle = angle - math.floor(angle/(2*math.pi))*2*math.pi
    elif angle <= -2*math.pi:
        angle = angle + math.floor(-angle/(2*math.pi))*2*math.pi
    
    if angle <= -math.pi:
        angle = 2*math.pi + angle
    elif angle > math.pi:
        angle = -2*math.pi + angle

    return angle


def minimum_angle_diff(x, y):
    d = math.fmod(y - x, (math.pi/2))
    if d < -math.pi:
        d = d + (math.pi/2)
    if d > math.pi:
        d = d - (math.pi/2)

    return -d


def match_pose(pose, dataset):
    """ Given a pose and a dataset of pre-computed poses, find the best matching pose from the dataset """
    matching_record = dataset[random.randint(0, len(dataset)-1)]
    return matching_record



class Application(tornado.web.Application):
    def __init__(self, args):
        self.args = args
        self.last_frame = None
        self.status = 'Idle'
        self.user_candidate_id = -1
        self.current_artwork = random.randint(0,87) # initialize to a random artwork

        handlers = [
            (r"/", DemoHandler),
            (r"/frames", FrameHandler),
            (r"/twod", TwoDHandler),
            (r"/artwork", ArtworkHandler),
            (r"/(.*)", tornado.web.StaticFileHandler, {"path": "templates", "default_filename": "index.html"})
        ]
        settings = dict(
            template_path=os.path.join(root_path, "templates"),
            static_path=os.path.join(root_path, "static")
        )

        with open("posed_paintings.json", 'r') as dataset_file:
            self.artwork_dataset = json.load(dataset_file)

        super().__init__(handlers, **settings)



    @tornado.gen.coroutine
    def subscribe_frames(self):
        ''' Subscribe to /frames via a websocket client connection '''
        websocket_server = f"ws://{self.args.websocket_server}/frames"
        print(f"connecting to: {websocket_server}")
        conn = yield tornado.websocket.websocket_connect(websocket_server)
        while True:
            msg = yield conn.read_message()
            if msg is None: break
            self.last_frame = msg

            # main control
            if not self.args.skip_user:
                if self.status == 'Idle':
                    # check if there is a person standing in the correct place
                    candidate = is_user(self.last_frame)
                    if candidate >= 0:
                        self.status = 'Align'
                        self.user_candidate_id = candidate 
                        ArtworkHandler.send_artwork(json.dumps({'status': self.status}))
                elif self.status == 'Align':
                    alignment_status = user_alignment(self.last_frame, self.user_candidate_id)
                    if alignment_status == 'No users':
                        self.status == 'Idle'
                        ArtworkHandler.send_artwork(json.dumps({'status': self.status}))
                    elif alignment_status == 'Aligned':
                        self.status == 'Capture'
                        ArtworkHandler.send_artwork(json.dumps({'status': self.status}))
                    else:
                        ArtworkHandler.send_artwork(json.dumps({'status': self.status, 'nudge': alignment_status}))
                elif self.status == 'Capture':
                    yield tornado.gen.sleep(5)
                    msg = yield conn.read_message()
                    if msg is None: break
                    self.last_frame = msg
                    # perform inference on pose in last frame
                    best_artwork = match_pose(self.last_frame, self.artwork_dataset, self.user_candidate_id)
                    self.status = 'Display'
                    ArtworkHandler.send_artwork(json.dumps({'status': self.status, 'artwork': best_artwork}))
                elif self.status == 'Display':
                    yield tornado.gen.sleep(7)
                    self.status = 'Idle'
                    ArtworkHandler.send_artwork(json.dumps({'status': self.status}))
            else:
                if self.status == 'Idle':
                    yield tornado.gen.sleep(2)
                    self.status = 'Capture'
                elif self.status == 'Capture':
                    yield tornado.gen.sleep(5)
                    msg = yield conn.read_message()
                    if msg is None: break
                    self.last_frame = msg
                    # perform inference on pose in last frame
                    best_artwork = match_pose(self.last_frame, self.artwork_dataset)
                    self.status = 'Display'
                    ArtworkHandler.send_artwork(json.dumps({'status': self.status, 'artwork': best_artwork}))
                elif self.status == 'Display':
                    yield tornado.gen.sleep(7)
                    self.status = 'Idle'
                    ArtworkHandler.send_artwork(json.dumps({'status': self.status}))


    @tornado.gen.coroutine
    def subscribe_twod(self):
        ''' Subscribe to /twod via a websocket client connection '''
        websocket_server = f"ws://{self.args.websocket_server}/twod"
        print(f"connecting to: {websocket_server}")
        conn = yield tornado.websocket.websocket_connect(websocket_server)
        while True:
            msg = yield conn.read_message()
            if msg is None: break
            if self.last_frame is None: break
            FrameHandler.send_updates(self.last_frame)
            TwoDHandler.send_2d(msg)



class DemoHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")



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



def main():
    args = parser.parse_args()

    app = Application(args)
    app.listen(args.local_port, '0.0.0.0')
    print(f"open http://127.0.0.1:{args.local_port} in your browser to preview the data")
    if not args.websocket_server:
        raise RuntimeError("Please specify the server to connect to with --websocket-server")
    tornado.ioloop.IOLoop.current().spawn_callback(app.subscribe_frames)
    tornado.ioloop.IOLoop.current().spawn_callback(app.subscribe_twod)

    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()


if __name__ == "__main__":
    main()
