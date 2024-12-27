from deepface import DeepFace
import cv2

# Haar-Cascade-Datei für verbesserte Face Recognition laden
cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(cascade_path)

# 0 um Standard-Webcam zu benutzen
cap = cv2.VideoCapture(0)  

while True:
    # Frame von der Kamera lesen
    ret, frame = cap.read()
    if not ret:
        print("Fehler beim Abrufen des Kamerabildes.")
        break

    # Face Recognition mit Cascade Classifier
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Emotion Detection
    for (x, y, w, h) in faces:
        face_frame = frame[y:y+h, x:x+w]
        try:
            # Emotionserkennung mit DeepFace
            analysis = DeepFace.analyze(face_frame, actions=['emotion'], enforce_detection=False)

            # Überprüfen, ob mehrere Gesichter analysiert wurden
            if isinstance(analysis, list):
                analysis = analysis[0]  # Erstes Gesicht verwenden

            dominant_emotion = analysis['dominant_emotion']

            # Gesicht mit Rechteck markieren und Emotion anzeigen
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(
                frame, 
                f"Emotion: {dominant_emotion}", 
                (x, y - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.9, 
                (255, 0, 0), 
                2
            )
        except Exception as e:
            print(f"Fehler bei der Emotionserkennung: {e}")

    # Frame im Fenster anzeigen
    cv2.imshow("Face and Emotion Detection", frame)

    # 'q' drücken, um die Kamera zu schließen
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kamera und Fenster freigeben
cap.release()
cv2.destroyAllWindows()