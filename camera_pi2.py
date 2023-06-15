import io
import time
from libracamera import controls
from picamera2 import Picamera2
from base_camera import BaseCamera


class Camera(BaseCamera):
    @staticmethod
    def frames():
        with Picamera2() as camera:
            camera.start()
            camera.set_controls({"AfMode": controls.AfModeEnum.Continuous})

            # let camera warm up
            time.sleep(2)

            stream = io.BytesIO()
            try:
                while True:
                    camera.capture_file(stream, format="jpeg")
                    stream.seek(0)
                    yield stream.read()

                    # reset stream for next frame
                    stream.seek(0)
                    stream.truncate()
            finally:
                camera.stop()
