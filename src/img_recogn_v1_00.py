#Name: Kriston Rickman
#Date: 08/13/26
#V1.00
#Notes: Testing if the camera works with the picamera2 library and if the camera is hooked properly


from picamera2 import Picamera2
import time

camera = Picamera2()
camera.start()
time.sleep(2)


def capture_image(filename="snapshot_test.jpg"):
    try:
        camera.capture_file(filename)
        print(f"Image saved as {filename}")
    except Exception as e:
        print(f"Failed to save image: {e}")


if __name__ == "__main__":
    try:
        capture_image("snapshot_test.jpg")
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        camera.stop()


