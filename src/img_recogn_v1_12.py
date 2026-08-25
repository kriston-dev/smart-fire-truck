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


#Global Variables
arduino = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_1453330373135121C161-if00', 115200, timeout=1)
print("initializing model...")
model = YOLO("landmarks/flower-vase/flwr_vase.pt")
print("YOLO model loaded")

confidence = 0.4
image_size = 640

# /* The amount of frames to confirm 
# the object is present in the image. *\
frame_confirm = 1


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
            print("variable to add frame...")
            frame = camera.capture_array()
            print("frame variable had been created")
            print("creating the results from the model...")
            results = model(frame, conf=confidence,imgsz=image_size)
            print("results have been created")
            print("annotating the results...")
            frame_annotated = results[0].plot()
            print("frames have been annotated")
            print("Starting to check if passed the count for max confidence in its decision...")
            print(model.names)
            if len(results[0].boxes) > 0:
                count += 1

                if count >= frame_confirm:
                    print("Object detected!")
                    arduino.write(b"LM1\n")
                    count = 0
            else:
                print("Either detection was lost or nothing was detected")
                # /*Detection was lost from the camera, thus 
                # resetting the counter*\
                count = 0

    finally:
        print("Disconnecting from program...")
        camera.stop()
        camera.close()




if __name__ == "__main__":
    main()

