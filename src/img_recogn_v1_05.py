#Name: Kriston Rickman
#Date: 08/13/26
#V1.05
#Notes: /*configuring code to fixed errors and to 
#troubleshoot due to the code only running for a few seconds *\

#/*There was a problem with the datbase due to
#code not specific for the database*\ 

# /*sudo apt install -y python3-picamera2 to operate the
# camera through the DSI connectors.*\

# To set up the program do:
# /*sudo apt install git -y
# git clone --filter=blob:none --no-checkout https://github.com/kriston-dev/smart-fire-truck.git
#cd smart-fire-truck
#git sparse-checkout set src
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

# /*To train the model:
# yolo detect train model=yolo11n.pt data=src/landmarks/flowervase/data.yaml epochs=50 imgsz=640*\


# Libraries
from picamera2 import Picamera2
from ultralytics import YOLO
import cv2
import time


#Global Variables
print("initializing model...")
model = YOLO("landmarks/flower-vase/flwr_vase.pt")
print("YOLO model loaded")

confidence = 0.4
image_size = 640

# /* The amount of frames to confirm 
# the object is present in the image. *\
frame_confirm = 5


def main():
    #local variables
    count = 0
    print("creating camera variable")
    camera = Picamera2()
    print("camera variable created")
    print("configuring cam...")
    camera.configure(
        camera.create_preview_configuration(
            main ={"format": "RGB888", "size": (640,480)}
            )
        )
    print("Cam done configuring")
    print("Camera will soon be ready...")
    camera.start()
    time.sleep(2)
    print("camera is ready")

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
                print("Either detection was lost or nothing was detected")
                # /*Detection was lost from the camera, thus 
                # resetting the counter*\
                count = 0
            if cv2.waitKey(1) == ord("q"):
                break
    finally:
        print("Disconnecting from program...")
        cv2.destroyAllWindows()
        camera.stop()


if __name == "__main__":
    main()



