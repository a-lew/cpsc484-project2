"""Script for single-gpu/multi-gpu demo."""
import argparse
import json
import os
import random

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.gen

from src.handlers import ArtworkHandler, DemoHandler, FrameHandler, TwoDHandler
from src.pose_matching_utils import match_pose
from src.user_detection_utils import is_user, user_alignment

parser = argparse.ArgumentParser(description='Art Mirror backend')
parser.add_argument('--websocket-server', type=str, help='ip address of websocket server')
parser.add_argument('--local-port', type=int, default=6677, help="this server's local port")

root_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))



class Application(tornado.web.Application):
    def __init__(self, args):
        self.args = args
        self.last_frame = None
        self.status = 'Idle'
        self.user_candidate_id = -1
        self.current_artwork = random.randint(0,290) # initialize to a random artwork

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
            if self.status == 'Idle':
                print(self.status)
                # check if there is a person standing in the correct place
                ArtworkHandler.send_artwork(json.dumps({'status': self.status}))
                candidate = is_user(self.last_frame)
                if candidate >= 0:
                    self.status = 'Align'
                    self.user_candidate_id = candidate 
                    ArtworkHandler.send_artwork(json.dumps({'status': self.status, 'nudge': 'none'}))
            elif self.status == 'Align':
                alignment_status = user_alignment(self.last_frame, self.user_candidate_id)
                print(alignment_status)
                print(self.status)
                if alignment_status == 'No users' or alignment_status == 'Previous user not found':
                    self.status == 'Idle'
                    ArtworkHandler.send_artwork(json.dumps({'status': self.status}))
                elif alignment_status == 'Aligned':
                    self.status = 'Capture'
                    ArtworkHandler.send_artwork(json.dumps({'status': self.status}))
                else:
                    ArtworkHandler.send_artwork(json.dumps({'status': self.status, 'nudge': alignment_status}))
            elif self.status == 'Capture':
                print(self.status)
                yield tornado.gen.sleep(5)
                msg = yield conn.read_message()
                if msg is None: break
                self.last_frame = msg
                # perform inference on pose in last frame
                best_artwork = match_pose(self.last_frame, self.user_candidate_id, self.artwork_dataset)
                self.status = 'Display'
                ArtworkHandler.send_artwork(json.dumps({'status': self.status, 'artwork': best_artwork}))
            elif self.status == 'Display':
                print(self.status)
                yield tornado.gen.sleep(11)
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



def main():
    args = parser.parse_args()

    app = Application(args)
    app.listen(args.local_port, '0.0.0.0')
    print(f"open http://127.0.0.1:{args.local_port} in your browser to view the application")
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
