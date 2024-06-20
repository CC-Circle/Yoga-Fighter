from collections import namedtuple
import math
from decimal import Decimal, getcontext
from mediapipe.framework.formats import landmark_pb2

class Detection:
    def __init__(self) -> None:
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
        self.Landmark = namedtuple("Landmark", ["x", "y", "z"])
        self.Landmarks_name =[
            "nose", "left_eye_inner", "left_eye", "left_eye_outer", 
            "right_eye_inner", "right_eye", "right_eye_outer",
            "left_ear", "right_ear", "mouth_left", "mouth_right",
            "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
            "left_wrist", "right_wrist", "left_pinky", "right_pinky",
            "left_index", "right_index", "left_thumb", "right_thumb",
            "left_hip", "right_hip", "left_knee", "right_knee",
            "left_ankle", "right_ankle", "left_heel", "right_heel",
            "left_foot_index", "right_foot_index"
        ]
        self.BodyLandmarks_dict = {key: self.Landmark(0.0, 0.0, 0.0) for key in self.Landmarks_name}

        self.image_width = 300.0
        self.image_height = 300.0

    def _update_BodyLandmarks_dict(self, pose_landmarks_proto, image_width, image_height) -> None:
        self.image_width = image_width
        self.image_height = image_height
        for i in range(len(pose_landmarks_proto.landmark)):
            self.BodyLandmarks_dict[self.Landmarks_name[i]] = pose_landmarks_proto.landmark[i]

    def _print_pose_landmarks_proto(self, pose_landmarks_proto) -> None:
        # 各ランドマークの座標をコンソールに表示
        for i in range(len(pose_landmarks_proto.landmark)):
            print(self.BodyLandmarks[i], "\n", pose_landmarks_proto.landmark[i])

    def _print_BodyLandmarks_dict(self, pose_landmarks_proto) -> None:
        #self._update_BodyLandmarks_dict(pose_landmarks_proto)
        # ランドマーク情報をコンソールに表示
        for key, value in self.BodyLandmarks_dict.items():
           print(key, "\n", value.x, value.y, value.z)

    def _get_BodyLandmarks(self, landmark_name) -> dict:
       # 使い方の例
       # print(self.BodyLandmarks_dict["nose"].x)
       if landmark_name in self.BodyLandmarks_dict:
           return self.BodyLandmarks_dict[landmark_name]
       else:
           print("Invalid landmark name:", landmark_name)
           return None
       
    def _tree_pose_UpperBody(self) -> bool:
        tree_pose = False

        # 右肘と左肘のy座標が肩のy座標よりも小さいか確認
        # 右肩と左肩のx,y座標の平均を計算
        avg_shoulder_y = (self.BodyLandmarks_dict["left_shoulder"].y + self.BodyLandmarks_dict["right_shoulder"].y) / 2.0
        if self.BodyLandmarks_dict["left_elbow"].y > avg_shoulder_y or self.BodyLandmarks_dict["right_elbow"].y > avg_shoulder_y:
            #大きかったら、木のポーズでないと判断
            return tree_pose
        
        # 右肘と左肘のy座標が鼻のy座標よりも小さいか確認
        if self.BodyLandmarks_dict["left_elbow"].y > self.BodyLandmarks_dict["nose"].y or self.BodyLandmarks_dict["right_elbow"].y > self.BodyLandmarks_dict["nose"].y:
            # 大きかったら、木のポーズでないと判断
            return tree_pose
        

        # 右手と左手のy座標が右肘と左肘よりも小さいか確認
        # 右手の検出されているランドマークのy座標の平均を計算
        coordinates_right = [self.BodyLandmarks_dict["right_wrist"].y, self.BodyLandmarks_dict["right_pinky"].y, self.BodyLandmarks_dict["right_index"].y, self.BodyLandmarks_dict["right_thumb"].y]
        coordinates_left = [self.BodyLandmarks_dict["left_wrist"].y, self.BodyLandmarks_dict["left_pinky"].y, self.BodyLandmarks_dict["left_index"].y, self.BodyLandmarks_dict["left_thumb"].y]
        # 右手と左手のy座標を計算
        right_hand_y = self._calculate_average(coordinates_right)
        left_hand_y = self._calculate_average(coordinates_left)
        if right_hand_y > self.BodyLandmarks_dict["right_elbow"].y or left_hand_y > self.BodyLandmarks_dict["left_elbow"].y:
            # 大きかったら、木のポーズでないと判断
            return tree_pose

        # 右手と左手のx座標が右肩と左肩のx座標の間にあるか確認
        coordinates_right = [self.BodyLandmarks_dict["right_wrist"].x, self.BodyLandmarks_dict["right_pinky"].x, self.BodyLandmarks_dict["right_index"].x, self.BodyLandmarks_dict["right_thumb"].x]
        coordinates_left = [self.BodyLandmarks_dict["left_wrist"].x, self.BodyLandmarks_dict["left_pinky"].x, self.BodyLandmarks_dict["left_index"].x, self.BodyLandmarks_dict["left_thumb"].x]

        # 右手と左手のx座標を計算
        right_hand_x = self._calculate_average(coordinates_right)
        left_hand_x = self._calculate_average(coordinates_left)

        # 右手と左手のx座標が右肩と左肩のx座標の間にあるか確認
        #avg_shoulder_x = (self.BodyLandmarks_dict["left_shoulder"].x + self.BodyLandmarks_dict["right_shoulder"].x) / 2.0
        #if right_hand_x > avg_shoulder_x or left_hand_x < avg_shoulder_x:
            # 大きかったら、木のポーズでないと判断
        #    return tree_pose
        

        print("-------------------------------------------")
        print("Tree Pose")
        print("右肩: ", self.BodyLandmarks_dict["right_shoulder"].x)
        print("左肩: ", self.BodyLandmarks_dict["left_shoulder"].x)
        print("右手:" , right_hand_x)
        print("左手:" , left_hand_x)
        print("-------------------------------------------")
        return tree_pose
    
    def _calculate_average(self, coordinates) -> float:
        """
        指定された座標リストから None でない値を抽出し、その平均を計算します。

        Parameters:
        coordinates (list): 座標のリスト

        Returns:
        float or None: 有効な値の平均、または有効な値がない場合は None
        """
        valid_coords = [coord for coord in coordinates if coord is not None]
        if valid_coords:
            return sum(valid_coords) / len(valid_coords)
        return None

if __name__ == "__main__":
    print("Debug directly from __main__.py")