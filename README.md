# ヨガファイター

## 目次

- [インストール](#インストール)


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
