# HandGestureVolumeControl

This Python project allows you to control your system's volume using hand gestures. The volume is adjusted based on the distance between the tip of the thumb and the tip of the index finger. As the distance increases or decreases, the volume level changes accordingly, providing a hands-free and intuitive way to control audio levels.
Features

    Real-time hand gesture tracking using computer vision.
    Volume adjustment based on thumb and index finger distance.
    Hands-free and intuitive control of system audio.
    Integration with the pycaw library to control system audio.

# Requirements

To run the project, you need the following Python libraries:

    opencv-python (for real-time video processing)
    handTrackingModule (for detecting and tracking hand movements)
    pycaw (for controlling the system's audio)
    comtypes (for interaction with the system's audio interface)
    math (for calculating distance between hand landmarks)

Install the required libraries using pip:

    pip install opencv-python pycaw comtypes

Make sure to also have the handTrackingModule (you can replace it with any hand tracking library of your choice, such as mediapipe).

# Usage

  Clone this repository to your local machine:
  
    git clone https://github.com/yourusername/HandGestureVolumeControl.git

  Navigate to the project directory:

    cd HandGestureVolumeControl

  Run the script:

    python hand_gesture_volume_control.py

The system will use your webcam to track your hand gestures. Move your thumb and index finger to adjust the volume.
The distance between the tips of the thumb and index finger will control the volume, with closer distances lowering
the volume and farther distances increasing it.

# How It Works

    Hand Tracking: The project uses a hand tracking module to detect and track the position of your hand. Specifically, it calculates the distance between the tips of your thumb and index finger.
    Volume Control: Based on the measured distance, the system normalizes the value and maps it to a range from 0 to 100, representing the system's volume level.
    Real-Time Feedback: The distance and the current volume level are displayed on the camera preview in real-time.
