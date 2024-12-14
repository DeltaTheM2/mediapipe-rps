import cv2
import mediapipe as mp
import time

class Player:
    def __init__(self):
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,  # Use False for video
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        #self.gesture_map = {0: "Rock", 1: "Paper", 2: "Scissors"}
        self.tip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky tips
        #self.process_frame_interval = 3  # Process every 3rd frame for performance
        #self.frame_counter = 0

        self.drawing = mp.solutions.drawing_utils

    def count_fingers(self, landmarks):
        """
        Count the number of fingers that are 'up' using landmarks.
        """
        fingers = []

        # Thumb: Check if the thumb tip is to the right of the thumb's lower joint (for right hand)
        # or to the left (for left hand). This is a simplification.
        if landmarks[self.tip_ids[0]].x > landmarks[self.tip_ids[0] - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)

        # Other fingers: Compare tip.y to the joint below (landmark id - 2)
        for tip in self.tip_ids[1:]:
            if landmarks[tip].y < landmarks[tip - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)

        return sum(fingers)

    def get_gesture(self, frame):
        """
        Detect the hand gesture and classify it as Rock, Paper, or Scissors.
        """

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.drawing.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
                num_fingers = self.count_fingers(hand_landmarks.landmark)
                if num_fingers == 0:
                    return "Rock"
                elif num_fingers == 5:
                    return "Paper"
                elif num_fingers == 2:
                    return "Scissors"
                else:
                    return "Unknown"
        return "None"
