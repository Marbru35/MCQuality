# MC Quality

<div align="center">
  <img src="icons/mcquality.PNG" alt="MC Quality Logo" width="200">
</div>
<br>

**Automated User State Detection Project**

Welcome to the MCQuality project! This repository contains the code and implementation of a real-time emotion detection tool based on video data, developed as part of our software quality project.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Getting Started](#getting-started)
3. [Environment Setup](#environment-setup)
4. [Project Contributors](#project-contributors)

---

## Project Overview
The MCQuality project explores state-of-the-art tools and frameworks for user state detection using video data, with a focus on real-time emotion recognition. After systematically reviewing existing technologies, we selected a promising tool to build a prototype that demonstrates its potential in the field of UX and satisfaction for a specific use-case.

**Prototype Implementation**: Demonstration of the feasibility and potential of the selected solution. <br>
**Selected Tool**:

## Key Features:
- **Static Emotion Detection**: Allows to upload an image of a face and detect the emotions expressed in the image.
- **Real-Time Emotion Detection**: A functional prototype that detects user emotions from video streams in real time.
- **Distribution of Dominant Emotions**: Bar chart showing the percentage of dominant emotions detected.
- **Emotion Intensity over Time**: Line chart showing the intensity of emotions over time.
- **Supported Emotions**: Detects the following emotions: neutral, happy, fear, surprise, angry, sad, and disgust

The code provides three Python files:
- **gui.py**: implements a graphical user interface (GUI) using `Tkinter`, allowing users to select between static and real-time emotion detection based on facial features, visualize the results as bar and line charts, and dynamically execute the scripts `EmotionDetectionGUI.py` and `EmotionDetectionRealTime.py`
- **EmotionDetectionGUI.py**: 
- **EmotionDetectionRealTime.py**: implements a real-time emotion detection system using video input

---

## How the Detection Works

---

## Getting Started
To run the prototype, follow these steps:

1. Clone this repository:
   ```bash
   git clone https://github.com/Marbru35/MCQuality.git
   cd MCQuality
   ...

##  Contributors
This project is part of a university group project created for the course Software Quality (SQ) by the following contributors: 
- Carlotta May
- Marlon Spiess
---

Have fun exploring our prototype! 
