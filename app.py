from segmentation_mask.segmentation import Segmentation
from utils.utils import Utils
from flask import Flask, Response, render_template
from application_logging.logger import AppLogger
from flask_cors import cross_origin
import cv2
import os
import random

app = Flask(__name__)
camera = cv2.VideoCapture(0)
segmentation = Segmentation()
utils = Utils()
logger = AppLogger()
collection_name = "api_handler"


@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def home():
    try:
        logger.database.connect_db()
        if logger.database.is_connected():
            logger.log(collection_name, 'Database Connected....', 'Info')
        else:
            raise Exception('Database not connected')
        logger.log(collection_name, 'Initiating app', 'Info')
        return render_template('index.html')
    except Exception as e:
        logger.log(
            collection_name,
            f'Exception occured in initiating or creation/deletion of Input_data directory. Message: {str(e)}',
            'Error')
        message = 'ERROR :: '+str(e)
        return render_template('exception.html', exception=message)


@app.route('/video_feed', methods=['GET'])
@cross_origin()
def video_feed():
    try:
        return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        logger.log(collection_name,
                   f'Exception occured while streaming video in video_feed method. Message: {str(e)}',
                   'Error')
        message = 'ERROR :: ' + str(e)
        return render_template('exception.html', exception=message)


@app.route('/video_feed/<mode>', methods=['GET'])
@cross_origin()
def video_feed_modified(mode):
    try:
        return Response(gen_frames(int(mode)), mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        logger.log(collection_name,
                   f'Exception occured while streaming video in video_feed_modified method. Message: {str(e)}',
                   'Error')
        message = 'ERROR :: ' + str(e)
        return render_template('exception.html', exception=message)


def gen_frames(mode=0):
    try:
        logger.log(collection_name, 'Entered Gen_frames method', 'Info')
        randnum = random.randrange(0, 7) # getting random number for replacing background with random images.
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
    except Exception as e:
        logger.log(collection_name,
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
        logger.database.connect_db()
        if logger.database.is_connected():
            logger.log(collection_name, 'Database Connected....', 'Info')
        else:
            raise Exception('Database not connected')
        data = logger.database.read_data(log)
        return render_template('logs.html', logs=data)
    except Exception as e:
        message = 'Error :: ' + str(e)
        logger.database.close_connection()
        return render_template('exception.html', exception=message)


if __name__ == "__main__":
    app.run(host='0.0.0.0')