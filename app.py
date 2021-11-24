from segmentation_mask.segmentation import Segmentation
from utils.utils import Utils
from flask import Flask, Response, render_template
from flask_socketio import SocketIO, emit
from application_logging.logger import AppLogger
from flask_cors import cross_origin
import cv2
import os
import io
from PIL import Image
import base64
import numpy as np
from engineio.payload import Payload

Payload.max_decode_packets = 2048
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')
segmentation = Segmentation()
utils = Utils()
logger = AppLogger()
log_file_object = open("prediction_log/api_handler.txt", 'a+')


@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def home():
    try:
        logger.log(log_file_object, 'Initiating app', 'Info')
        return render_template('index.html')
    except Exception as e:
        logger.log(
            log_file_object,
            f'Exception occured in initiating or creation/deletion of Input_data directory. Message: {str(e)}',
            'Error')
        message = 'ERROR :: '+str(e)
        return render_template('exception.html', exception=message)


def readb64(base64_string):
    idx = base64_string.find('base64,')
    base64_string = base64_string[idx+7:]

    sbuf = io.BytesIO()

    sbuf.write(base64.b64decode(base64_string, ' /'))
    pimg = Image.open(sbuf)

    return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)


@socketio.on('image')
def image(data_image):
    frame = (readb64(data_image['data']))
    frame = gen_frames(frame, data_image['mode'])
    imgencode = cv2.imencode('.jpeg', frame, [cv2.IMWRITE_JPEG_QUALITY, 40])[1]
    # base64 encode
    string_data = base64.b64encode(imgencode).decode('utf-8')
    b64_src = 'data:image/jpeg;base64,'
    string_data = b64_src + string_data
    # emit the frame back
    emit('response_back', string_data)


def gen_frames(frame, mode=0):
    try:
        logger.log(log_file_object, 'Entered Gen_frames method', 'Info')

        if mode == 1:
            mask, frame = segmentation.get_mask(frame)
            frame = utils.remove_background(mask, frame)
        elif mode == 2:
            mask, frame = segmentation.get_mask(frame)
            frame = utils.blur_background(mask, frame)
        elif mode == 3:
            lst = os.listdir('bg_images/')
            path = 'bg_images/'+lst[0]
            mask, frame = segmentation.get_mask(frame)
            frame = utils.change_background(mask, frame, path)

        return frame

    except Exception as e:
        logger.log(log_file_object,
                   f'Exception occured while streaming video/Changing background in gen_frames method. Message: {str(e)}',
                   'Error')
        message = 'ERROR :: ' + str(e)
        return render_template('exception.html', exception=message)


@app.route('/getlogs', methods=['GET'])
@cross_origin()
def view_logs():
    """
    Returns Html page for Logs
    :return: html
    """

    try:
        return render_template('logs.html')
    except Exception as e:
        message = 'Error :: ' + str(e)
        return render_template('exception.html', exception=message)


@app.route('/getlogs/<log>', methods=['GET'])
@cross_origin()
def get_logs(log):
    """
    Returns logs for inspection of the system
    :return: html
    """

    try:
        data = []
        return render_template('logs.html', logs=data)
    except Exception as e:
        message = 'Error :: ' + str(e)
        return render_template('exception.html', exception=message)


if __name__ == "__main__":
    socketio.run(app, debug=True)
