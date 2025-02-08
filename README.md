# MC Quality

<div align="center">
  <img src="icons/mcquality.PNG" alt="MC Quality Logo" width="200">
</div>
<br>

**Automated User State Detection Project**

Welcome to the MC Quality project! This repository contains the code and implementation of a real-time emotion detection tool based on video data, developed as part of our software quality project.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Getting Started](#getting-started)
3. [Usage](#usage)
   - [How to Run the Application](#how-to-run-the-application)
   - [Static Emotion Analysis](#static-emotion-analysis)
   - [Real-Time Emotion Detection](#real-time-emotion-detection)
4. [Contributors](#contributors)
5. [License](#license)

---

## Project Overview
The MCQuality project explores state-of-the-art tools and frameworks for user state detection using video data, with a focus on real-time emotion recognition. After systematically reviewing existing technologies, we selected a promising tool to build a prototype that demonstrates its potential in the field of UX and satisfaction for a specific use-case.

**Prototype Implementation**: Demonstration of the feasibility and potential of the selected solution. <br>
**Selected Tool**: The prototype leverages the [DeepFace python library](https://github.com/serengil/deepface), a lightweight face recognition and facial attribute analysis framework.

## Key Features:
- **Static Emotion Detection**: Allows to upload an image of a face and detect the emotions expressed in the image.
- **Real-Time Emotion Detection**: A functional prototype that detects user emotions from video streams in real time.
- **Distribution of Dominant Emotions**: Bar chart showing the percentage of dominant emotions detected.
- **Emotion Intensity over Time**: Line chart showing the intensity of emotions over time.
- **Supported Emotions**: Detects the following emotions: neutral, happy, fear, surprise, angry, sad, and disgust

The code provides three Python files:
- **main.py**: implements a graphical user interface (GUI) using `Tkinter`, allowing users to select between static and real-time emotion detection based on facial features, visualize the results as bar and line charts, and dynamically execute the scripts `emotion_detection_static.py` and `emotion_detection_realtim.py`
- **emotion_detection_static.py**: 
- **emotion_detection_realtime.py**: implements a real-time emotion detection system using video input

---

## Getting Started
To install the prototype, follow these steps:

1. Clone this repository:
   ```bash
   git clone https://github.com/Marbru35/MCQuality.git
   cd MCQuality
   ```
2. Setup a virtual environment
- On Windows:
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
- On macOS/Linux:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

To use the application, start by running the main `gui.py` script. This script launches a graphical user interface (GUI) that allows users to select between **Static Emotion Analysis** and **Real-Time Emotion Detection** modes.

### How to Run the Application
1. **Run the GUI**:
   - Open a terminal or command prompt.
   - Navigate to the project directory where `gui.py` is located.
   - Run the following command:
     ```bash
     python gui.py
     ```
   - This will launch the GUI, where you can select either **Static Emotion Analysis** or **Real-Time Emotion Detection**.

### Static Emotion Analysis

The **Static Emotion Analysis** feature allows users to upload an image of a face and detect the emotions expressed in the image.

#### How It Works
1. **Upload an Image**: Users can upload an image file in formats like `.jpg`, `.jpeg`, or `.png` using the intuitive interface.
2. **Emotion Detection**: The application processes the image using the DeepFace library to detect the dominant emotion and calculate the probabilities of other emotions.
3. **Visualization**:
   - Displays the uploaded image in the interface for easy reference.
   - Generates a bar chart showing the percentage likelihood for each detected emotion.

#### Steps to Use
1. Click the "Upload Image" button in the GUI.
2. Select an image from your device.
3. View the dominant emotion result and the corresponding bar chart in the application.

### Real-Time Emotion Detection

The `EmotionDetectionRealTime.py` script implements a real-time emotion detection system using video input captured through the webcam. The detected emotions are dynamically displayed on the GUI and saved for further analysis.

#### How It Works
1. **Real-Time Video Capture**: The webcam feed is processed frame by frame.
2. **Face Detection**: Uses a Haar Cascade classifier to detect faces within each frame.
3. **Emotion Analysis**:
   - Applies the DeepFace library to analyze facial expressions and detect emotions.
   - Extracts both the dominant emotion and the intensity levels for all emotions.
4. **Visualization**:
   - Highlights detected faces in the video feed with bounding boxes.
   - Displays the dominant emotion as a label on the video feed.
5. **Data Logging**:
   - Captures emotion data along with timestamps.
   - Saves results into a CSV file (`emotions_results.csv`) for graphical analyses with the following structure.
     - **time**: Timestamp of the detected emotion
     - **dominant_emotion**: The most prominent emotion detected in the frame
     - **angry, disgust, fear, happy, sad, surprise, neutral**: Intensity level for each emotion

#### Steps to Use
1. Select "Real-Time Emotion Detection" in the GUI.
2. Allow the application to access your webcam.
3. View the live video feed with real-time dominant emotion detection result.
4. Stop the detection using the "Exit" button to save the results to a CSV file.
5. View the distribution of the dominant emotions and the intensity of the emotions over time from the results of the CSV files in the corresponding bar chart and line graph.
   
---

##  Contributors
This project is part of a university group project created for the course Software Quality (SQ) by the following contributors: 
- Carlotta May
- Marlon Spiess
  
---

## License
[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute this software under the conditions stated in the LICENSE file.

---

Have fun exploring our prototype! 
