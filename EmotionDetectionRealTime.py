from tkinter import *
from threading import Thread
import cv2
from PIL import Image, ImageTk
from deepface import DeepFace
import csv

class RealTimeDetection:
    def __init__(self):
        self.running = True  # Die Echtzeit-Erkennung läuft standardmäßig
        self.cap = None
        self.root = None
        self.video_label = None
        self.emotions_data = []  # Speicher für Emotionen

    def start_realtime_detection(self):
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        face_cascade = cv2.CascadeClassifier(cascade_path)
        self.cap = cv2.VideoCapture(0)

        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Fehler beim Abrufen des Kamerabildes.")
                break

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                face_frame = frame[y:y+h, x:x+w]

                if face_frame is None or face_frame.size == 0:
                    continue

                try:
                    analysis = DeepFace.analyze(face_frame, actions=['emotion'], enforce_detection=False)

                    if isinstance(analysis, list):
                        analysis = analysis[0]

                    # Dominante Emotion speichern
                    dominant_emotion = analysis['dominant_emotion']
                    self.emotions_data.append({'emotion': dominant_emotion})

                    # Rechteck und Emotion anzeigen
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    cv2.putText(frame, f"Emotion: {dominant_emotion}", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                except Exception as e:
                    print(f"Fehler bei der Analyse: {e}")

            # Video im GUI-Label anzeigen
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

        self.cap.release()
        self.save_results_to_file()

    def save_results_to_file(self):
        # Speichert die Emotionen in einer CSV-Datei
        with open("emotions_results.csv", "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["emotion"])
            writer.writeheader()
            writer.writerows(self.emotions_data)

    def stop_realtime_detection(self):
        self.running = False

    def exit_to_main_gui(self):
        self.stop_realtime_detection()
        if self.root:
            self.root.destroy()

    def start_gui(self):
        self.root = Tk()
        self.root.title("Real-Time Emotion Detection")

        self.root.state('zoomed')
        self.root.configure(bg="white")

        lbl_title = Label(self.root, text="Video stream und Emotionserkennung", font=("Arial", 16))
        lbl_title.pack(pady=10)

        frame_main = Frame(self.root)
        frame_main.pack(fill=BOTH, expand=True, padx=10, pady=10)

        frame_image = Frame(frame_main, width=450, height=450)
        frame_image.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        self.video_label = Label(frame_image)
        self.video_label.pack()

        lbl_result = Label(self.root, text="", font=("Arial", 12))
        lbl_result.pack(pady=5)

        detection_thread = Thread(target=self.start_realtime_detection)
        detection_thread.daemon = True
        detection_thread.start()

        control_frame = Frame(self.root, bg="lightgray", width=200)
        control_frame.pack(side=RIGHT, fill=Y)

        btn_stop = Button(control_frame, text="Stop", font=("Arial", 12), bg="orange", fg="white", command=self.stop_realtime_detection)
        btn_stop.pack(pady=20, padx=20, fill=X)

        btn_exit = Button(control_frame, text="Exit", font=("Arial", 12), bg="red", fg="white", command=self.exit_to_main_gui)
        btn_exit.pack(pady=20, padx=20, fill=X)

        self.root.mainloop()

if __name__ == "__main__":
    detector = RealTimeDetection()
    detector.start_gui()
    