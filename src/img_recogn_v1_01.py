#Name: Kriston Rickman
#Date: 08/13/26
#V1.01
#Notes: /* Now testing the database with the raspberry pi 
# through the library ultralytics YOLO. *\

#/*Testing if the camera works with the picamera2 library
#and if the camera is hooked properly.*\

# /*sudo apt install -y python3-picamera2 to operate the
# camera through the DSI connectors.*\

# To set up the program do:
# /*sudo apt install git -y
# git clone https://github.com/kriston-dev/smart-fire-truck.git
# to clone the program 
# onto the raspberry pi.*\

# /*From the home directory do:
#python3 -m venv --system-site-packages yolo-env to create a virtual environment
# source ~/yolo-env/bin/activate to activate
# mkdir -p ~/pip-tmp to create a temporary directory for pip to use due to errors with the raspberry pi and pip.*\
# /* Download the ultralytic last incase the need of
# deleting the yolo-env file, the download is long *\
# TMPDIR=~/pip-tmp pip install ultralytics /* to download the ultralytics library for YOLO object detection.*\
# To activate ultralytic you must be activated to run it

# Libraries
from picamera2 import Picamera2
from ultralytics import YOLO
import cv2
import time


#Global Variables
print("initializing model...")
model = YOLO("flwr_vase.pt")

confidence = 0.4
image_size = (640, 480)

# /* The amount of frames to confirm 
# the object is present in the image. *\
frame_confirm = 5


def main():
    #local variables
    count = 0

    camera = Picamera2()
    camera.configure(
        camera.create_preview_configuration(
            main ={"format": "RGB888", "size": (640, 480)}
            )
        )
    camera.start()
    time.sleep(2)

    try:
        while True:

            frame = camera.capture_array()

            results = model(
                frame,
                conf=confidence,
                imgsz=image_size
                )
            frame_annotated = results[0].plot()
            cv2.imshow("Showing input...", frame_annotated)
            if len(results[0].boxes) > 0:
                count += 1

                if count >= frame_confirm:
                    print("Object detected!")
                    count = 0
            else:
                # /*Detection was lost from the camera, thus 
                # resetting the counter*\
                count = 0
            if cv2.waitKey(1) == ord("q"):
                break
    finally:
        print("Disconnecting from program...")
        cv2.destroyAllWindows()
        camera.stop()
