# Rock Paper Scissors with MediaPipe

This project implements a Rock Paper Scissors (RPS) game using MediaPipe for hand gesture detection and recognition. The game allows players to compete against a computer by showing their gestures in front of a webcam, with the computer making its own random decisions. The program determines the winner of each round and keeps track of the scores.

## Features

- **Hand Gesture Recognition**: Uses MediaPipe to detect and classify gestures for Rock, Paper, and Scissors.
- **Computer Opponent**: The computer randomly selects its moves.
- **Score Tracking**: Keeps track of the player's and the computer's scores across multiple rounds.
- **Countdown and Results Display**: Provides a countdown before each round and displays the results after each round.
- **Replay Option**: Allows players to replay the game or quit after completing all rounds.

## Requirements

### Hardware
- A webcam for gesture detection.

### Software
- Python 3.8 or later
- The following Python libraries:
  - `mediapipe`
  - `opencv-python`
  - `numpy`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/DeltaTheM2/mediapipe-rps.git
   cd mediapipe-rps
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the main script:
   ```bash
   python main.py
   ```

2. Follow the on-screen instructions:
   - **Main Menu**: Show a "Scissors" gesture to start the game or a "Paper" gesture to quit.
   - **Game Rounds**: Show your gesture (Rock, Paper, or Scissors) during the countdown.
   - **Replay Menu**: After completing all rounds, show "Scissors" to replay or "Paper" to quit.

3. Scores will be displayed after each round and updated in real-time.

## File Structure

- `main.py`: Main game logic and user interface.
- `player.py`: Handles player input and gesture recognition using MediaPipe.
- `comp.py`: Contains logic for the computer's decision-making.
- `README.md`: Project documentation.

## How It Works

1. **Gesture Detection**:
   - MediaPipe's hand detection module identifies the player's hand gestures in real-time.
   - Custom logic interprets the detected hand pose as Rock, Paper, or Scissors.

2. **Computer Decision**:
   - The computer makes random choices among Rock, Paper, and Scissors.

3. **Winner Determination**:
   - The game logic compares the player's and the computer's moves to determine the winner of each round.

4. **Display and Scoring**:
   - The results are displayed on the screen after each round.
   - Scores are updated for the player and the computer.


## Contributing

Contributions are welcome! If you'd like to contribute, please:
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [MediaPipe](https://google.github.io/mediapipe/) for providing the hand detection library.
- [OpenCV](https://opencv.org/) for enabling real-time video processing.

