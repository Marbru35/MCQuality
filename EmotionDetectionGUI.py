from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from deepface import DeepFace
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def upload_and_analyze():
    # Datei hochladen
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
    if not file_path:
        lbl_result.config(text="Keine Datei ausgewählt.", fg="red")
        return

    try:
        # Emotionen analysieren & extrahieren
        analysis = DeepFace.analyze(img_path=file_path, actions=['emotion'])
        emotions = analysis[0]['emotion']
        dominant_emotion = analysis[0]['dominant_emotion']

        # Ergebnisse in der GUI anzeigen
        lbl_result.config(text=f"Dominante Emotion: {dominant_emotion}", fg="green")

        # Bild im GUI anzeigen
        img = Image.open(file_path)
        img_tk = ImageTk.PhotoImage(img)
        lbl_image.config(image=img_tk)
        lbl_image.image = img_tk

        # Balkendiagramm in der GUI anzeigen
        figure = plt.Figure(figsize=(5, 4), dpi=100)
        ax = figure.add_subplot(111)
        ax.bar(emotions.keys(), emotions.values(), color='skyblue')
        ax.set_ylim(0, 100)  # Y-Achse auf 0 bis 100 begrenzen
        ax.set_xlabel("Emotionen", fontsize=10)
        ax.set_ylabel("Wahrscheinlichkeit (%)", fontsize=10)
        ax.tick_params(axis='x', rotation=45, labelsize=8)
        ax.tick_params(axis='y', labelsize=8)

        # Matplotlib-Canvas
        for widget in frame_chart.winfo_children():  # Vorherige Charts entfernen
            widget.destroy()
        canvas = FigureCanvasTkAgg(figure, master=frame_chart)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True, pady=0)

    except Exception as e:
        lbl_result.config(text=f"Fehler bei der Analyse: {e}", fg="red")

# GUI erstellen
root = Tk()
root.title("Emotionserkennung")
root.state('zoomed')  # Vollbildmodus 
root.configure(bg="white") # Hintergrundfarbe

# Überschrift
lbl_title = Label(root, text="Bild hochladen und analysieren", font=("Arial", 16))
lbl_title.pack(pady=10)

# Hauptbereich: Bild und Diagramm nebeneinander
frame_main = Frame(root)
frame_main.pack(fill=BOTH, expand=True, padx=10, pady=10)

# Bild
frame_image = Frame(frame_main, width=450, height=450)
frame_image.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
lbl_image = Label(frame_image)
lbl_image.pack()

# Balkendiagramm
frame_chart = Frame(frame_main, width=450, height=450)
frame_chart.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

# Ergebnis-Label
lbl_result = Label(root, text="", font=("Arial", 12))
lbl_result.pack(pady=5)

# Button
btn_upload = Button(root, text="Bild hochladen", command=upload_and_analyze, width=20, height=2, font=("Arial", 12))
btn_upload.pack(pady=5)

# Hauptloop starten
root.mainloop()