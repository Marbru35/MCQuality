from deepface import DeepFace
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# Bildpfad
image_path = "resources/istockphoto.jpg"

# Emotionserkennung
analysis = DeepFace.analyze(img_path=image_path, actions=['emotion'])

# Ergebnisse
print("Analyseergebnisse:")
print(analysis)

# Emotionen extrahieren
emotions = analysis[0]['emotion']
dominant_emotion = analysis[0]['dominant_emotion']

# Emotionen als Text ausgeben
print("\nDominante Emotion:", dominant_emotion)
print("Emotionen (mit Wahrscheinlichkeit):")
for emotion, value in emotions.items():
    print(f"{emotion}: {value:.2f}%")

# Bild anzeigen
img = Image.open(image_path)

plt.figure(figsize=(10, 5))

# Originalbild
plt.subplot(1, 2, 1)
plt.imshow(img)
plt.axis('off')
plt.title("Originalbild")

# Emotionen als Balkendiagramm
plt.subplot(1, 2, 2)
plt.bar(emotions.keys(), emotions.values(), color='skyblue')
plt.xlabel("Emotionen")
plt.ylabel("Wahrscheinlichkeit (%)")
plt.title("Emotionserkennung")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()