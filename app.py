#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response

# import camera driver
# Valid values for Camera Library are:
# pi for Picamera
# pi2 for Picamera2
# opencv for opencv
if os.environ.get("CAMERA"):
    Camera = import_module("camera_" + os.environ["CAMERA"]).Camera
else:
    # Camera Emulator with 1.jpg, 2.jpg, 3.jpg
    from camera import Camera

app = Flask(__name__)

# flask_cam = Camera()


@app.route("/")
def index():
    """Video streaming home page."""
    return render_template("index.html")


def gen(camera):
    """Video streaming generator function."""
    yield b"--frame\r\n"
    while True:
        frame = camera.get_frame()
        yield b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n--frame\r\n"


@app.route("/video_feed")
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(
        gen(Camera()), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/thumbnail")
def get_thumbnail():
    """ After the camera stops, this no longer works.
    """
    frame = Camera().get_frame()
    return Response(frame, mimetype="image/jpeg")


if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)
