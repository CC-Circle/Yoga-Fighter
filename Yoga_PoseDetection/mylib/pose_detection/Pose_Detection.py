import cv2 as cv

def _print_version() -> None:
    print(cv.__version__)

def hello() -> None:
    print("Hello from Pose_Detection.py")

if __name__ == '__main__':
    print("Debug directly from Pose_Detection.py")
    _print_version()