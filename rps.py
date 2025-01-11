import cv2
import time
from player import Player
from comp import Comp

class RPS:
    def __init__(self):
        self.player = Player()
        self.computer = Comp()
        self.state = "menu"  # Possible states: menu, game, replay, quit
        self.scores = {"Player": 0, "Computer": 0}
        self.round_number = 0
        self.countdown_start = None
        self.post_round_delay_start = None  # Tracks time for post-round delay
        self.computer_move = None
        self.calculated = False

    def determine_winner(self, player_move, computer_move):
        if player_move == computer_move:
            return "Tie"
        elif (player_move == "Rock" and computer_move == "Scissors") or \
             (player_move == "Paper" and computer_move == "Rock") or \
             (player_move == "Scissors" and computer_move == "Paper"):
            return "Player"
        return "Computer"

    def display_overlay(self, frame, text, position=(10, 30), font_scale=1, color=(0, 255, 0)):
        """
        Display text overlay on the frame.
        """
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, text, position, font, font_scale, color, 2)

    def countdown(self, frame, duration=3):
        """
        Display a countdown overlay without freezing the video feed.
        """
        elapsed_time = time.time() - self.countdown_start
        remaining_time = duration - int(elapsed_time)
        if remaining_time > 0:
            self.display_overlay(frame, f"Starting in {remaining_time}", position=(200, 250), font_scale=2)
            return False  # Countdown not complete
        return True  # Countdown complete

    def post_round_delay(self, frame, duration=3):
        """
        Delay after a round to show the results before starting the next round.
        """
        if self.post_round_delay_start is None:
            self.post_round_delay_start = time.time()

        elapsed_time = time.time() - self.post_round_delay_start
        if elapsed_time < duration:
            return False  # Still in delay period
        self.post_round_delay_start = None  # Reset delay timer
        return True  # Delay complete

    def main_menu(self, frame):
        """
        Main menu logic to prompt the user to start or quit the game.
        """
        self.display_overlay(frame, "Show Scissors to Start, Paper to Quit", position=(50, 50))
        gesture = self.player.get_gesture(frame)
        if gesture == "Paper":
            return "quit"
        elif gesture == "Scissors":
            return "game"
        return "menu"

    def play_round(self, frame):
        # Display the round and scores
        self.display_overlay(frame, f"Round {self.round_number + 1}", (10, 80))
        self.display_overlay(frame, f"Player Score: {self.scores['Player']}", (10, 150), color=(255, 0, 0))
        self.display_overlay(frame, f"Computer Score: {self.scores['Computer']}", (10, 220), color=(0, 0, 255))

        # 1) START COUNTDOWN IF NEEDED
        if self.countdown_start is None:
            self.countdown_start = time.time()

        # 2) SHOW COUNTDOWN WHILE NOT DONE
        if not self.countdown(frame, duration=3):
            # If countdown not complete, just keep waiting in "game" state
            return "game"

        # 3) GET MOVES (only once after countdown)
        player_move = self.player.get_gesture(frame)
        if self.computer_move is None:
            self.computer_move = self.computer.make_decision()

        # 4) IF WE HAVEN'T SCORED THIS ROUND YET, DO SO
        if player_move != "None" and self.computer_move is not None and not self.calculated:
            # determine winner and increment score
            winner = self.determine_winner(player_move, self.computer_move)
            if winner == "Player":
                self.scores["Player"] += 1
            elif winner == "Computer":
                self.scores["Computer"] += 1
            # Show result overlays...
            self.calculated = True  # Make sure we don't double-score
            self.computer.learn(player_move)

        # 5) IF WE HAVE SCORED ALREADY (self.calculated = True), SHOW RESULTS, THEN WAIT 3 SECONDS
        if self.calculated:
            # Keep showing the result overlay, but don’t score again
            # Wait for the post-round delay to finish
            if not self.post_round_delay(frame, duration=3):
                return "game"  # STILL waiting...

            # Once delay is done, reset everything to move to next round
            self.calculated = False
            self.round_number += 1
            self.countdown_start = None
            self.computer_move = None
            
            # If we’ve done enough rounds, go to "replay" (or whatever your end state is)
            if self.round_number >= 5:
                return "replay"

        else:
            # If we haven't detected a valid gesture yet, display a message
            self.display_overlay(frame, "No valid gesture detected!", (10, 360))

        return "game"

    def replay_menu(self, frame):
        """
        Replay menu logic to prompt the user to replay or quit the game.
        """

        self.display_overlay(frame, "Game Over!", position=(200, 100), font_scale=2)
        self.display_overlay(frame, "Show Scissors to Replay, Paper to Quit", position=(50, 150))
        gesture = self.player.get_gesture(frame)
        if gesture == "Paper":
            return "quit"
        elif gesture == "Scissors":
            return "game"
        return "replay"

    def play_game(self):
        """
        Main game loop that manages state transitions and frame rendering.
        """
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not access webcam.")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to read from webcam.")
                break

            frame = cv2.resize(frame, (640, 480))

            if self.state == "menu":
                self.state = self.main_menu(frame)
            elif self.state == "game":
                self.state = self.play_round(frame)
            elif self.state == "replay":
                self.state = self.replay_menu(frame)
            elif self.state == "quit":
                self.display_overlay(frame, "Goodbye!", position=(200, 250), font_scale=2, color=(0, 0, 255))
                cv2.imshow("Rock Paper Scissors", frame)
                cv2.waitKey(2000)  # Allow user to see the message
                break
            print(self.state)
            # Display the updated frame
            cv2.imshow("Rock Paper Scissors", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    game = RPS()
    game.play_game()



