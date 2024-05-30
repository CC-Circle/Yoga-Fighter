import copy
import argparse
import cv2 as cv
import numpy as np
import mediapipe as mp
from .cvfpscalc import CvFpsCalc

class PoseLandmarks:
    """
    人間の姿勢を検出し、その結果を視覚化するクラス。

    Attributes
    ----------
    args : Namespace
        コマンドライン引数を解析した結果。
    mp_pose : mediapipe.solutions.pose
        MediaPipe Poseソリューション。
    pose : mediapipe.solutions.pose.Pose
        MediaPipe Poseのインスタンス。
    cvFpsCalc : CvFpsCalc
        FPS計算のためのユーティリティ。
    """

    def __init__(self) -> None:
        """
        PoseLandmarksクラスのインスタンスを初期化する。
        """
        self._parse_arguments()
        self._initialize_pose()
        self.cvFpsCalc = CvFpsCalc(buffer_len=10)
    
    def _parse_arguments(self) -> None:
        """
        コマンドライン引数を解析する。
        """
        parser = argparse.ArgumentParser()

        # コマンドライン引数
        # デフォルト値はMediaPipe Poseのデフォルト値を設定
        parser.add_argument("--device", type=int, default=0) # カメラデバイス番号
        parser.add_argument("--width", help='キャプチャの幅', type=int, default=1280) # キャプチャの幅
        parser.add_argument("--height", help='キャプチャの高さ', type=int, default=720) # キャプチャの高さ
        parser.add_argument("--min_detection_confidence", help='最小検出信頼度', type=float, default=0.5) # 最小検出信頼度
        parser.add_argument("--min_tracking_confidence", help='最小追跡信頼度', type=float, default=0.5) # 最小追跡信頼度
        parser.add_argument('--enable_segmentation', action='store_true', help='セグメンテーションの有効化') # セグメンテーションの有効化
        parser.add_argument("--segmentation_score_th", help='セグメンテーションスコアの閾値', type=float, default=0.5) # セグメンテーションスコアの閾値
        parser.add_argument('--use_brect', action='store_true', help='外接矩形の使用') # 外接矩形の使用
        parser.add_argument('--plot_world_landmark', action='store_false', help='3Dランドマークのプロット') # 3Dランドマークのプロット
        parser.add_argument("--model_complexity", help='モデルの複雑さ (0,1(default),2)', type=int, default=1) # モデルの複雑さ

        self.args = parser.parse_args()

    def _initialize_pose(self) -> None:
        """
        MediaPipe Poseソリューションを初期化する。
        """
         # MediaPipe Poseのインスタンスを作成
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            # モデルの複雑さを設定
            model_complexity=self.args.model_complexity,
            # セグメンテーションの設定
            enable_segmentation=self.args.enable_segmentation,
            # 最小検出信頼度
            min_detection_confidence=self.args.min_detection_confidence,
            # 最小追跡信頼度
            min_tracking_confidence=self.args.min_tracking_confidence,
        )
    
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
        fps_color = (255, 255, 255) if self.args.enable_segmentation else (0, 255, 0)   # セグメンテーションが有効な場合は白色、無効な場合は緑色
        cv.putText(image, "FPS:" + str(fps), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1.0, fps_color, 2, cv.LINE_AA) # FPS表示

    def main(self, capture_image) -> np.ndarray:
        """
        画像を処理し、結果を視覚化する。

        Parameters
        ----------
        capture_image : np.ndarray
            処理する画像。

        Returns
        -------
        np.ndarray
            処理結果の画像。
        """
        # FPSの計算
        display_fps = self.cvFpsCalc.get()

        # 画像を左右反転（ミラー表示）
        image = cv.flip(capture_image, 1)
        # デバッグ用の画像コピー
        debug_image = copy.deepcopy(image)

        # 画像をRGBに変換し、MediaPipeで処理
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        results = self.pose.process(image)

        # セグメンテーション処理
        debug_image = self._segmentation(results, image, debug_image)

        # ポーズランドマークが検出された場合、ランドマークを描画
        if results.pose_landmarks is not None:
            debug_image = self._draw_landmarks(debug_image, results.pose_landmarks)

        # FPS表示
        self._fps_visualization(debug_image, display_fps)
        
        return debug_image
    
    def _segmentation(self, results, image, debug_image) -> np.ndarray:
        """
        セグメンテーションを行う。

        Parameters
        ----------
        results : mediapipe.python.solution_base.SolutionOutputs
            MediaPipe Poseの処理結果。
        image : np.ndarray
            元の画像。
        debug_image : np.ndarray
            デバッグ用の画像。

        Returns
        -------
        np.ndarray
            セグメンテーション後の画像。
        """
        # セグメンテーションが有効で、セグメンテーションマスクが存在する場合
        if self.args.enable_segmentation and results.segmentation_mask is not None:
            # セグメンテーションマスクを作成
            mask = np.stack((results.segmentation_mask, ) * 3, axis=-1) > self.args.segmentation_score_th
            # 背景を緑色に設定
            bg_resize_image = np.zeros(image.shape, dtype=np.uint8) # セグメンテーションマスクのサイズに合わせた背景画像を作成
            bg_resize_image[:] = (0, 255, 0)    # 緑色に設定
            debug_image = np.where(mask, debug_image, bg_resize_image)  # セグメンテーションマスクがFalseの部分を緑色に変換
        return debug_image

    def _draw_landmarks(self, image, landmarks, visibility_th=0.5) -> np.ndarray:
        """
        ランドマークを画像に描画する。

        Parameters
        ----------
        image : np.ndarray
            ランドマークを描画する画像。
        landmarks : mediapipe.framework.formats.landmark_pb2.NormalizedLandmarkList
            描画するランドマーク。
        visibility_th : float, optional
            ランドマークの可視性の閾値。

        Returns
        -------
        np.ndarray
            ランドマークを描画した後の画像。
        """
        # 画像の幅と高さを取得
        image_width, image_height = image.shape[1], image.shape[0]

        landmark_point = [] # ランドマークの座標と可視性を格納するリスト
        right_eye = ()  # 右目の座標
        left_eye = ()   # 左目の座標

        # 各ランドマークを処理
        for index, landmark in enumerate(landmarks.landmark):
            # ランドマークの位置を画像のピクセル座標に変換
            landmark_x = min(int(landmark.x * image_width), image_width - 1)    # ランドマークのx座標
            landmark_y = min(int(landmark.y * image_height), image_height - 1)  # ランドマークのy座標
            landmark_z = landmark.z # ランドマークのz座標
            # 可視性と座標をリストに追加
            landmark_point.append([landmark.visibility, (landmark_x, landmark_y)])

            # 可視性が閾値以下のランドマークは無視
            if landmark.visibility < visibility_th:
                continue

            # 特定のランドマークに対して円を描画
            if index == 2:  # 右目
                right_eye = (landmark_x, landmark_y)    # 右目の座標を保存
            if index == 5:  # 左目
                left_eye = (landmark_x, landmark_y)    # 左目の座標を保存
            ''' 11: 右肩, 12: 左肩, 13: 右肘, 14: 左肘, 15: 右手首, 16: 左手首
                17: 右手1(外側端), 18: 左手1(外側端), 19: 右手2(先端), 20: 左手2(先端)
                21: 右手3(内側端), 22: 左手3(内側端), 23: 腰(右側), 24: 腰(左側)
                25: 右ひざ, 26: 左ひざ, 27: 右足首, 28: 左足首, 29: 右かかと, 30: 左かかと
                31: 右つま先, 32: 左つま先'''
            if index in [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]:
                cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)   # ランドマークの位置に円を描画

        # 両目の中心座標を計算して描画
        if right_eye and left_eye:
            center_x = int((right_eye[0] + left_eye[0]) / 2)    # 両目のx座標の中心
            center_y = int((right_eye[1] + left_eye[1]) / 2)    # 両目のy座標の中心
            center_eye = (center_x, center_y)   # 両目の中心座標
            cv.circle(image, center_eye, 5, (0, 255, 0), 2)  # 両目の中心座標に円を描画

        # ランドマークポイントが存在する場合、線を描画
        if len(landmark_point) > 0:
            # 肩、腕、手、胴体、足の描画
            self._draw_lines(image, landmark_point, visibility_th)
        
        return image

    def _draw_lines(self, image, landmark_point, visibility_th) -> None:
        """
        ランドマーク間の線を画像に描画する。

        Parameters
        ----------
        image : np.ndarray
            線を描画する画像。
        landmark_point : list
            描画するランドマークの座標と可視性のリスト。
        visibility_th : float
            ランドマークの可視性の閾値。
        """
        # 各ランドマーク間の接続を定義
        ''' 11: 右肩, 12: 左肩, 13: 右肘, 14: 左肘, 15: 右手首, 16: 左手首
            17: 右手1(外側端), 18: 左手1(外側端), 19: 右手2(先端), 20: 左手2(先端)
            21: 右手3(内側端), 22: 左手3(内側端), 23: 腰(右側), 24: 腰(左側)
            25: 右ひざ, 26: 左ひざ, 27: 右足首, 28: 左足首, 29: 右かかと, 30: 左かかと
            31: 右つま先, 32: 左つま先'''
        connections = [
            (11, 12), (11, 13), (13, 15), (12, 14), (14, 16),
            (15, 17), (17, 19), (19, 21), (21, 15), (16, 18),
            (18, 20), (20, 22), (22, 16), (11, 23), (12, 24),
            (23, 24), (23, 25), (25, 27), (27, 29), (29, 31),
            (24, 26), (26, 28), (28, 30), (30, 32)
        ]   # 接続するランドマークの組み合わせ
        # 各接続を描画
        for start, end in connections:
            if landmark_point[start][0] > visibility_th and landmark_point[end][0] > visibility_th:
                cv.line(image, landmark_point[start][1], landmark_point[end][1], (0, 255, 0), 2)    # ランドマーク間に線を描画

if __name__ == '__main__':
    # PoseLandmarksクラスのインスタンスを作成
    PL = PoseLandmarks()

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
        resultImage = PL.main(image)
        # 結果画像を表示
        cv.imshow('MediaPipe Pose Demo', resultImage)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    
    # キャプチャを解放してウィンドウを破棄
    cap.release()
    cv.destroyAllWindows()
