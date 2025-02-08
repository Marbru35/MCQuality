"""
Real-Time Emotion Detection with GUI

This script uses a webcam to detect faces in real-time, analyze emotions
using the DeepFace library, and display results in a Tkinter GUI.
Emotion data is saved to a CSV file for further analysis.
"""

from tkinter import *
from threading import Thread
import cv2
from PIL import Image, ImageTk
from deepface import DeepFace
import csv
import time
import os

# Define directories for results
current_dir = os.path.dirname(os.path.abspath(__file__))  # Current directory of the script
results_dir = os.path.join(current_dir, "..", "results")  # Results directory (relative to the parent directory)
csv_path = os.path.join(results_dir, "emotions_results.csv")  # Path to the results CSV file


class RealTimeDetection:
    """
    Class for real-time emotion detection via webcam.

    Attributes:
    - running (bool): Indicates whether the real-time detection is active.
    - cap (cv2.VideoCapture): Webcam capture object.
    - root (Tk): Tkinter GUI root window.
    - video_label (Label): Label widget to display the video feed.
    - emotions_data (list): List to store detected emotions and their intensities.
    """

    def __init__(self):
        """Initialize attributes and default settings."""
        self.running = True  # The detection runs by default
        self.cap = None  # Video capture object
        self.root = None  # Root Tkinter window
        self.video_label = None  # Label for video feed
        self.emotions_data = []  # List to store detected emotions and their intensities

    def start_realtime_detection(self):
        """
        Starts real-time emotion detection using the webcam.
        Detected faces are analyzed using DeepFace, and results are displayed on the GUI.
        """
        # Load the pre-trained face detection model (Haar Cascade)
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        face_cascade = cv2.CascadeClassifier(cascade_path)

        # Start video capture
        self.cap = cv2.VideoCapture(0)

        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Error capturing video feed.")
                break

            # Flip the frame horizontally for a mirrored view
            frame = cv2.flip(frame, 1)

            # Convert the frame to grayscale for face detection
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # Get the current timestamp
            current_time = time.strftime('%H:%M:%S')

            for (x, y, w, h) in faces:
                # Extract the face region
                face_frame = frame[y:y+h, x:x+w]

                # Skip if the extracted face frame is empty
                if face_frame is None or face_frame.size == 0:
                    continue

                try:
                    # Perform emotion analysis using DeepFace
                    analysis = DeepFace.analyze(face_frame, actions=['emotion'], enforce_detection=False)

                    if isinstance(analysis, list):
                        analysis = analysis[0]

                    # Extract emotions and the dominant emotion
                    emotions = analysis['emotion']
                    dominant_emotion = analysis['dominant_emotion']

                    # Save the results (timestamp, dominant emotion, and all intensities)
                    emotions_record = {
                        "time": current_time,
                        "dominant_emotion": dominant_emotion,
                        **emotions  # Include all emotions and their intensities
                    }
                    self.emotions_data.append(emotions_record)

                    # Draw a rectangle around the face and display the dominant emotion
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    cv2.putText(frame, f"{dominant_emotion}", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

                except Exception as e:
                    print(f"Error during emotion analysis: {e}")

            # Display the video feed in the Tkinter GUI
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

        # Release the video capture when detection stops
        self.cap.release()
        self.save_results_to_file()

    def save_results_to_file(self):
        """
        Saves the collected emotion data to a CSV file.
        If no data has been collected, a message is printed to the console.
        """
        if not self.emotions_data:
            print("No emotions data collected.")
            return

        # Ensure the results directory exists
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        # Define CSV headers
        fieldnames = ["time", "dominant_emotion", "angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]

        # Write data to the CSV file
        with open(csv_path, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.emotions_data)

        print(f"Saved {len(self.emotions_data)} emotion records to {csv_path}.")

    def stop_realtime_detection(self):
        """Stops the real-time emotion detection loop."""
        self.running = False

    def exit_to_main_gui(self):
        """
        Stops the detection, saves results to a file, and closes the GUI.
        """
        self.stop_realtime_detection()
        self.save_results_to_file()
        if self.root:
            self.root.destroy()

    def start_gui(self):
        """
        Initializes and starts the Tkinter GUI for real-time emotion detection.
        """
        self.root = Tk()
        self.root.title("Real-Time Emotion Detection")
        self.root.state('zoomed')  # Maximize the window
        self.root.configure(bg="white")

        # Add a title label to the GUI
        lbl_title = Label(self.root, text="Video stream and Emotion Detection", font=("Arial", 16))
        lbl_title.pack(pady=10)

        # Create the main video display frame
        frame_main = Frame(self.root)
        frame_main.pack(fill=BOTH, expand=True, padx=10, pady=10)

        frame_image = Frame(frame_main, width=450, height=450)
        frame_image.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        self.video_label = Label(frame_image)
        self.video_label.pack()

        # Create a label for displaying status messages
        lbl_result = Label(self.root, text="", font=("Arial", 12))
        lbl_result.pack(pady=5)

        # Start the detection in a separate thread to avoid blocking the GUI
        detection_thread = Thread(target=self.start_realtime_detection)
        detection_thread.daemon = True
        detection_thread.start()

        # Add an Exit button to stop detection and close the GUI
        control_frame = Frame(self.root, bg="lightgray", width=200)
        control_frame.pack(side=RIGHT, fill=Y)
        btn_exit = Button(control_frame, text="Exit", font=("Arial", 10), bg="red", fg="white", command=self.exit_to_main_gui)
        btn_exit.pack(pady=15, padx=20, fill=X)

        # Start the Tkinter main loop
        self.root.mainloop()


if __name__ == "__main__":
    # Create an instance of RealTimeDetection and start the GUI
    detector = RealTimeDetection()
    detector.start_gui()