import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2 as cv
import numpy as np
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import typing
from collections import deque
from Pose_Detection import Detection
from TCP_Server import TCPServer
import threading

class PoseLandmarks:
    def __init__(self, CAM_NUM=0, buffer_len=10) -> None:
        self.CAM_NUM = CAM_NUM
        self.BodyLandmarks = [
            "0 - 鼻", "1 - 左目（内側）", "2 - 左目", "3 - 左目（外側）",
            "4 - 右目（内側）", "5 - 右目", "6 - 右目（外側）",
            "7 - 左耳", "8 - 右耳", "9 - 口（左）", "10 - 口（右）",
            "11 - 左肩", "12 - 右肩", "13 - 左肘", "14 - 右肘",
            "15 - 左手首", "16 - 右手首", "17 - 左小指", "18 - 右小指",
            "19 - 左人差し指", "20 - 右人差し指", "21 - 左親指", "22 - 右親指",
            "23 - 左腰", "24 - 右腰", "25 - 左膝", "26 - 右膝",
            "27 - 左足首", "28 - 右足首", "29 - 左かかと", "30 - 右かかと",
            "31 - 左足指先", "32 - 右足指先"
        ]
        self._initialize_pose_landmarker()
        self._initialize_cvfpscalc(buffer_len=buffer_len)
    
    def _initialize_cvfpscalc(self, buffer_len=1) -> None:
        self._start_tick = cv.getTickCount()
        self._freq = 1000.0 / cv.getTickFrequency()
        self._difftimes = deque(maxlen=buffer_len)

    def _get_cvfps(self) -> float:
        current_tick = cv.getTickCount()
        different_time = (current_tick - self._start_tick) * self._freq
        self._start_tick = current_tick

        self._difftimes.append(different_time)

        fps = 1000.0 / (sum(self._difftimes) / len(self._difftimes))
        fps_rounded = round(fps, 2)

        return fps_rounded
    
    def _initialize_pose_landmarker(self) -> None:
        # PoseLandmarkerオブジェクトを作成
        base_options = python.BaseOptions(model_asset_path='pose_landmarker_full.task')
        options = vision.PoseLandmarkerOptions(base_options=base_options, output_segmentation_masks=True)
        self.detector = vision.PoseLandmarker.create_from_options(options)
    
    def _preprocess_image_for_mediapipe(self, capture_image) -> typing.Tuple[np.ndarray, int, int]:
         # 画像の前処理
        cv_image = cv.resize(capture_image, None, fx=0.5, fy=0.5)
        cv_image = cv.cvtColor(cv.flip(cv_image, 1), cv.COLOR_BGR2RGB)
        image_height, image_width, _ = cv_image.shape

         # mediapipe用の画像フォーマットに変換
        mediapipe_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv_image)
        return mediapipe_image, image_height, image_width
    
    def _get_landmarks_on_image(self, detection_result) -> landmark_pb2.NormalizedLandmarkList:
        # 入力画像からランドマーク情報を取得
        pose_landmarks_list = detection_result.pose_landmarks
        if pose_landmarks_list is None:
            return None
        
        pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        for pose_landmarks in pose_landmarks_list:
            pose_landmarks_proto.landmark.extend(
                #[landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y) for landmark in pose_landmarks]
                [landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks]
        )
        return pose_landmarks_proto


    def _detect_pose_landmarks(self, mediapipe_image) -> landmark_pb2.NormalizedLandmarkList:
         # ポーズランドマークを検出
        detection_result = self.detector.detect(mediapipe_image)
        pose_landmarks_proto = self._get_landmarks_on_image(detection_result)

        if pose_landmarks_proto is None:
            return None
        
        return pose_landmarks_proto
    
    def _print_landmarks(self, pose_landmarks_proto) -> None:
        # 各ランドマークの座標をコンソールに表示
        for i in range(len(pose_landmarks_proto.landmark)):
            print(self.BodyLandmarks[i], "\n", pose_landmarks_proto.landmark[i])
    
    def _draw_landmarks_on_image(self, image, pose_landmarks_proto):
        # ランドマーク情報を画像に描画

        try:
            # もしimageがMediaPipeの画像オブジェクトの場合
            if isinstance(image, mp.Image):
                cv_image = image.numpy_view()
                annotated_image = np.copy(cv_image)
                solutions.drawing_utils.draw_landmarks(
                    annotated_image,
                    pose_landmarks_proto,
                    solutions.pose.POSE_CONNECTIONS,
                    solutions.drawing_styles.get_default_pose_landmarks_style()
                )
                bgr_image = cv.cvtColor(annotated_image, cv.COLOR_RGB2BGR)
                return bgr_image, True
        except ValueError as e:
            #print(f"ValueError occurred 'BGR_image': {e}")
            print("カメラが塞がれている可能性があります。")
            return np.zeros((300, 300, 3)), False
        except Exception as e:
            # 他の種類の例外が発生した場合の処理
            print(f"Exception occurred 'BGR_image': {e}")
            return np.zeros((300, 300, 3)), False
        
        try:
            # もしimageが1チャンネルの場合
            image_height, image_width, _ = image.shape
            bg_image = np.zeros((image_height, image_width, 3))
            if np.array_equal(image, bg_image):
                # ランドマークのみ表示
                annotated_image = np.copy(bg_image)
                solutions.drawing_utils.draw_landmarks(
                annotated_image,
                pose_landmarks_proto,
                solutions.pose.POSE_CONNECTIONS,
                solutions.drawing_styles.get_default_pose_landmarks_style()
                )
                return annotated_image, True
            
        except ValueError as e:
            #print(f"ValueError occurred 'BG_image': {e}")
            #print("カメラが塞がれている可能性があります。")
            return np.zeros((300, 300, 3)), False
        except Exception as e:
            # 他の種類の例外が発生した場合の処理
            print(f"Exception occurred 'BG_image': {e}")
            return np.zeros((300, 300, 3)), False
        
        return image, False

    def _fps_visualization(self, image, fps) -> None:
        """
        FPSを画像に表示する。

        Parameters
        ----------
        image : np.ndarray
            FPSを表示する画像。
        fps : float
            表示するFPS。
        """
        # FPSを表示
        fps_color = (0, 255, 0)
        #try:
        cv.putText(image, "FPS:" + str(fps), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1.0, fps_color, 2, cv.LINE_AA)
        #except Exception as e:
        #    print(f"Exception occurred: {e}")

if __name__ == '__main__':
    PL = PoseLandmarks(CAM_NUM=0, buffer_len=10)
    DT = Detection()

    TCP = TCPServer(host='127.0.0.1', port=12345)
    server_thread = threading.Thread(target=TCP.start)
    server_thread.start()

    # カメラから入力画像を取得
    cap = cv.VideoCapture(PL.CAM_NUM)
    if not cap.isOpened():
        print("カメラをオープンできません。")
        print("カメラ番号が正しいか確認してください。")
        print("カメラ番号:", PL.CAM_NUM)
        exit()
    # カメラが起動するまで1秒待つ
    cv.waitKey(1000)

    while cap.isOpened():
        tick = cv.getTickCount()
        success, cam_image = cap.read()

        if not success:
            print("空のカメラフレームを無視します。")
            continue

        display_fps = PL._get_cvfps()

        # 画像の前処理, mediapipe用の画像フォーマットに変換
        mediapipe_image, image_height, image_width = PL._preprocess_image_for_mediapipe(cam_image)
         # ポーズランドマークを検出
        pose_landmarks_proto = PL._detect_pose_landmarks(mediapipe_image)

        if pose_landmarks_proto is None:
            continue

        # 各ランドマークの座標をコンソールに表示
        #PL._print_landmarks(pose_landmarks_proto)
        #DT._print_pose_landmarks_proto(pose_landmarks_proto)
        #DT._print_BodyLandmarks_dict(pose_landmarks_proto)

        # ランドマークを画像に描画
        body_image, success = PL._draw_landmarks_on_image(mediapipe_image, pose_landmarks_proto)
        if body_image is np.zeros((image_height, image_width, 3)):
            print("body_image is None")

        # ランドマークのみ表示
        bg_image = np.zeros((image_height, image_width, 3))
        landmark_image, success = PL._draw_landmarks_on_image(bg_image, pose_landmarks_proto)
        if landmark_image is np.zeros((image_height, image_width, 3)):
            print("landmark_image is None")

        DT._update_BodyLandmarks_dict(pose_landmarks_proto, image_width, image_height)
        flag = DT._tree_pose_UpperBody()
        if flag and success:
            print("Tree Pose")
        else:
            print("Not Tree Pose")
            DT.send_udp_data(None)

        # FPSを画像に表示
        PL._fps_visualization(body_image, display_fps)
        PL._fps_visualization(landmark_image, display_fps)


        # body_imageとlandmark_imageに線を描画
        cv.line(body_image, (170, 0), (170, image_height), (0, 0, 255), 3)
        cv.line(body_image, (image_width - 170, 0), (image_width-170, image_height), (0, 0, 255), 3)

        cv.imshow('Body', body_image)
        cv.imshow('Landmark', landmark_image)

        print("Scene Mode:", TCP._get_SceneMode())
        

        key = cv.waitKey(5)
        if key == ord('q') or key == ord('Q'):
            print('終了')
            break

    cv.destroyAllWindows()