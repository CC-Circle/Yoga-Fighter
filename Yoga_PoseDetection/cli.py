from .mylib.Pose_Landmarks import PoseLandmarks as Pose_Detection
import cv2 as cv

def main() -> None:
    print("Hello from cli.py")
    Pose_Landmark = Pose_Detection()
    # カメラキャプチャを開始
    cap = cv.VideoCapture(0)
    print("Capture Size ------------------------------")
    print("width: ", cap.get(cv.CAP_PROP_FRAME_WIDTH))
    print("height: ", cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    print("-------------------------------------------")

    while True:
        ret, image = cap.read()
        if not ret:
            break
        # フレームを処理して結果画像を取得
        resultImage = Pose_Landmark.main(image)
        # 結果画像を表示
        cv.imshow('MediaPipe Pose Demo', resultImage)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    
    # キャプチャを解放してウィンドウを破棄
    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    print("Debug directly from __main__.py")