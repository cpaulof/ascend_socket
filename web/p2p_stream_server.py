import cv2

from utils import Camera, SSDFaceMask as Model, encode_array
from utils.socket_utils import Server

model = Model('./model/')
camera = Camera()

cam = camera.read()

server = Server('127.0.0.1', 5656)

def main():
    while True:
        frame = next(cam)
        inputs = cv2.resize(frame, (320, 320))
        det = model.inference(inputs)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame_data, det_data = encode_array(frame), encode_array(det)
        server.send_to_all([frame_data, det_data])
