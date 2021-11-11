from segmentation_mask.segmentation import Segmentation
from utils.utils import Utils
from flask import Flask, Response, render_template
import cv2
import os
import random

app = Flask(__name__)
camera = cv2.VideoCapture(0)
segmentation = Segmentation()
utils = Utils()


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/video_feed', methods=['GET'])
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed/<mode>', methods=['GET'])
def video_feed_modified(mode):
    return Response(gen_frames(int(mode)), mimetype='multipart/x-mixed-replace; boundary=frame')


def gen_frames(mode=0, name=None):
    print(mode)
    randnum = random.randrange(0, 7)
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            if mode == 1:
                mask, frame = segmentation.get_mask(frame)
                frame = utils.remove_background(mask, frame)
            elif mode == 2:
                mask, frame = segmentation.get_mask(frame)
                frame = utils.blur_background(mask, frame)
            elif mode == 3:
                lst = os.listdir('bg_images/')
                path = 'bg_images/'+lst[randnum]
                mask, frame = segmentation.get_mask(frame)
                frame = utils.change_background(mask, frame, path)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


if __name__ == "__main__":
    app.run(debug=True)