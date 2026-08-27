#Name: Kriston Rickman
#Date: 08/13/26
#V1.09
#Notes: /*Found I needed to use a higher CPU to run the
#program and waiting for the camera adapter to arrive and
#start testing the code. I also made the mistake of creating
#the arduino code on python. This should be the final code
#for the raspberry pi.*\

#/*configuring code to fixed errors and to 
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
import time
import serial
import glob

port = None

while port is None:
    matches = glob.glob("/dev/serial/by-id/*")
    if matches:
        print("We were able to go into file to search for serial")
        port = matches[0]
    else:
        time.sleep(1)


#Global Variables
time.sleep(1)
arduino = serial.Serial(port, 115200, timeout=1)
print("initializing model...")
model = YOLO("landmarks/flower-vase/flwr_vase.pt")

confidence = 0.65
image_size = 640

# /* The amount of frames to confirm 
# the object is present in the image. *\
frame_confirm = 3


def main():
    #local variables
    count = 0
    landmark_sent = False
    camera = Picamera2()
    camera.configure(
        camera.create_preview_configuration(
            main ={"format": "RGB888", "size": (640,480)}
            )
        )
    camera.start()
    time.sleep(2)

    try:
        while True:
            frame = camera.capture_array()
            results = model(frame, conf=confidence,imgsz=image_size)
            frame_annotated = results[0].plot()
            if len(results[0].boxes) > 0:
                count += 1

                if count >= frame_confirm and not landmark_sent:
                    #write(b"LM1\n")
                    print("Sent LM1 to Arduino!")
                    landmark_sent = True
                    count = 0
            else:
                # /*Detection was lost from the camera, thus 
                # resetting the counter*\
                count = 0
                landmark_sent = False

    except KeyboardInterrupt:
        pass

    finally:
        camera.stop()
        camera.close()




if __name__ == "__main__":
    main()





