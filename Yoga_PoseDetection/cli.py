from .mylib.pose_detection import Pose_Detection

def main() -> None:
    print("Hello from cli.py")
    Pose_Detection.hello()

if __name__ == '__main__':
    print("Debug directly from __main__.py")