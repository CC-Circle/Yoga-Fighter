# ヨガファイター

## 目次

- [インストール](#環境構築)
- [PoseLandmarksクラス](#PoseLandmarksクラス)


## 環境構築

Yoga Fighterの姿勢推定プログラムのインストール手順は以下の通りです。
**環境構築は自己責任で行ってください。**

1. venv:Python仮想環境の構築
リポジトリをクローンしたら、ターミナルでYoga-Fighterを開く。
```cmd
学籍番号@学籍番号noMacBook-Air Yoga-Fighter %
```
Pythonの環境を確認する。全く同じバージョンでなくても多分大丈夫。Python入ってない人は、各自で入れてください。<br>
Python 3.x.x系なら多分大丈夫
```cmd
Yoga-Fighter % python -V
Python 3.12.3

Yoga-Fighter % python3 -V
Python 3.12.3
```
venvのActivate<br>
先頭に(venv)と表示されたら成功
```cmd
Yoga-Fighter % source venv/bin/activate
(venv) Yoga-Fighter % 
```
ちなみに、venvのDeactivateは、先頭の(venv)が取れたら成功
```cmd
(venv) Yoga-Fighter % deactivate
Yoga-Fighter %
```
2. opencv-pythonのインストール
brewでOpenCVライブラリをシステムにインストール
```cmd
$ brew install opencv
```
もし、opencvがインストーされているならつぎのようにupgradeを促すメッセージが出力される。その場合はupgradeも実施する。
```cmd
$ brew install opencv
・・・・・
######################################################################## 100.0%
Error: opencv 4.5.0 is already installed
To upgrade to 4.6.0_1, run `brew upgrade opencv`.
```
```cmd
# 上のようにアップグレードを指示された場合次のコマンドを実行する
brew upgrade opencv
```
pip3でopencv-pythonモジュールをインストール（venvをActivateした状態で行ってください。）
```cmd
(venv) Yoga-Fighter % pip3 install opencv-python
```
OpenCVのバージョンは、4.x.x系ならどれでもいいと思う。

3. mediapipeのインストール
pip3でmediapipeをインストール(venvをActivateした状態で行ってください。)
```cmd
(venv) Yoga-Fighter % pip install mediapipe
```

4. 実行する
必要な環境が整ったら、Yoga_Detection -> test.pyを実行する。<br>
Webカメラが起動して、姿勢推定が実行されます。結果が画面に出力されます。
```cmd
(venv) Yoga_PoseDetection % python3 test.py
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
I0000 00:00:1718861906.018309 18529329 gl_context.cc:357] GL version: 2.1 (2.1 Metal - 76.3), renderer: Apple M1
INFO: Created TensorFlow Lite XNNPACK delegate for CPU.
W0000 00:00:1718861906.106623 18529441 inference_feedback_manager.cc:114] Feedback manager requires a model with a single signature inference. Disabling support for feedback tensors.
W0000 00:00:1718861906.123921 18529441 inference_feedback_manager.cc:114] Feedback manager requires a model with a single signature inference. Disabling support for feedback tensors.
/Users/k22137kk/CCC/Yoga-Fighter/venv/lib/python3.12/site-packages/google/protobuf/symbol_database.py:55: UserWarning: SymbolDatabase.GetPrototype() is deprecated. Please use message_factory.GetMessageClass() instead. SymbolDatabase.GetPrototype() will be removed soon.
  warnings.warn('SymbolDatabase.GetPrototype() is deprecated. Please '
```
プログラムの終了は、'q' or 'Q'で終了してください。'終了'と表示されて、プログラムが終了します。
上記の方法でプログラムが終了しない場合は、Controlキー + C で終了してください。以下のような警告が出ますが、プログラムが終了します。
```cmd
^CTraceback (most recent call last):
  File "/Users/k22137kk/CCC/Yoga-Fighter/Yoga_PoseDetection/test.py", line 180, in <module>
    pose_landmarks_proto = PL._detect_pose_landmarks(mediapipe_image)
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/k22137kk/CCC/Yoga-Fighter/Yoga_PoseDetection/test.py", line 79, in _detect_pose_landmarks
    detection_result = self.detector.detect(mediapipe_image)
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/k22137kk/CCC/Yoga-Fighter/venv/lib/python3.12/site-packages/mediapipe/tasks/python/vision/pose_landmarker.py", line 352, in detect
    output_packets = self._process_image_data({
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/k22137kk/CCC/Yoga-Fighter/venv/lib/python3.12/site-packages/mediapipe/tasks/python/vision/core/base_vision_task_api.py", line 95, in _process_image_data
    return self._runner.process(inputs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
KeyboardInterrupt

(venv) Yoga_PoseDetection % 
```

## PoseLandmarksクラス

PoseLandmarksクラス(test.py)の簡単な説明。
PoseLandmarksクラスを使うことで、画像中の人間のランドマークを取得できる。
```python
# PoseLandmarksクラスのインスタンス化。CAM_NUMはカメラ番号、buffer_lenはFPS計算のためのバッファ長。
    PL = PoseLandmarks(CAM_NUM=0, buffer_len=10)
    
    # Detectionクラスのインスタンス化。
    DT = Detection()

    # カメラからの入力を取得するためのVideoCaptureオブジェクトを作成。
    cap = cv.VideoCapture(PL.CAM_NUM)

    while cap.isOpened():
        success, cam_image = cap.read()  # カメラから1フレーム読み込む。

        # もし読み込みに成功しなかった場合はスキップし、次のフレームを試行する。
        if not success:
            print("空のカメラフレームを無視します。")
            continue

        # 現在のFPSを取得。
        display_fps = PL._get_cvfps()

        # 画像の前処理を行い、Mediapipe用のフォーマットに変換する。
        mediapipe_image, image_height, image_width = PL._preprocess_image_for_mediapipe(cam_image)

        # ポーズランドマークを検出する。
        pose_landmarks_proto = PL._detect_pose_landmarks(mediapipe_image)

        # もしポーズランドマークが検出されなかった場合は次のフレームに進む。
        if pose_landmarks_proto is None:
            continue

        # ボディイメージにポーズのランドマークを描画する。
        body_image, success = PL._draw_landmarks_on_image(mediapipe_image, pose_landmarks_proto)
        if body_image is np.zeros((image_height, image_width, 3)):
            print("body_image is None")

        # ランドマークのみ表示する背景イメージを作成する。
        bg_image = np.zeros((image_height, image_width, 3))
        landmark_image, success = PL._draw_landmarks_on_image(bg_image, pose_landmarks_proto)
        if landmark_image is np.zeros((image_height, image_width, 3)):
            print("landmark_image is None")

        # Detectionクラスのメソッドを使用して、ポーズランドマークの情報を更新し、
        # イメージの幅と高さを提供する。
        DT._update_BodyLandmarks_dict(pose_landmarks_proto, image_width, image_height)

        # ボディイメージおよびランドマークイメージにFPSを表示する。
        PL._fps_visualization(body_image, display_fps)
        PL._fps_visualization(landmark_image, display_fps)

        # ウィンドウにボディイメージを表示する。
        cv.imshow('Body', body_image)
        # ウィンドウにランドマークイメージを表示する。
        cv.imshow('Landmark', landmark_image)

        # キーボードの入力を待機し、'q'が押された場合はプログラムを終了する。
        key = cv.waitKey(5)
        if key == ord('q') or key == ord('Q'):
            print('終了')
            break

    # 全てのウィンドウを閉じる。
    cv.destroyAllWindows()
```

## Detectionクラスの簡単な説明

Detectionクラスを使うことで、PoseLandmarksで取得したランドマークを分析して、人間がどのようなポーズを取っているかを判定できます。

```python
# Detectionクラスのインスタンス化。
DT = Detection()

# Detectionクラスのメソッドを使用して、ポーズランドマークの情報を更新し、
# イメージの幅と高さを提供する。
DT._update_BodyLandmarks_dict(pose_landmarks_proto, image_width, image_height)

# ポーズが「Tree Pose」に似ているかどうかを確認し、結果を出力する。
# successはPoseLandmarksクラスの```_draw_landmarks_on_image(self, image, pose_landmarks_proto)```関数が成功しているかを表している。
if DT._tree_pose_UpperBody() and success:
  print("Tree Pose")
else:
  print("Not Tree Pose")
```

大まかなプログラムの流れは以下の通りです。
1. OpenCVの機能を使用して、Webカメラから画像を取得する。
2. PoseLandmarksの関数で、ランドマークデータ（pose_landmarks_proto）を取得する。
3. Detectionクラスの関数で、人間のポーズを推定する。
4. OpenCVの機能を使用して、ランドマークデータを画面に描画
