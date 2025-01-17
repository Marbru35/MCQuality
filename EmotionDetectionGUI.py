from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from deepface import DeepFace
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def start_gui():
    def upload_and_analyze():
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if not file_path:
            lbl_result.config(text="Keine Datei ausgewählt.", fg="red")
            return

        try:
            analysis = DeepFace.analyze(img_path=file_path, actions=['emotion'])
            emotions = analysis[0]['emotion']
            dominant_emotion = analysis[0]['dominant_emotion']

            lbl_result.config(text=f"Dominante Emotion: {dominant_emotion}", fg="green")

            # Bild öffnen und skalieren
            img = Image.open(file_path)

            # Maximale Bildgröße definieren
            max_size = (450, 450)  # Maximale Größe für das Bild

            # Bild skalieren, um in das Fenster zu passen
            img.thumbnail(max_size)

            img_tk = ImageTk.PhotoImage(img)
            lbl_image.config(image=img_tk)
            lbl_image.image = img_tk

            # Erstelle das Balkendiagramm
            figure = plt.Figure(figsize=(6, 5), dpi=100)  # Größere Höhe für die Darstellung
            ax = figure.add_subplot(111)
            ax.bar(emotions.keys(), emotions.values(), color='skyblue')
            ax.set_ylim(0, 100)
            ax.set_xlabel("Emotionen", fontsize=12)
            ax.set_ylabel("Wahrscheinlichkeit (%)", fontsize=12)
            ax.tick_params(axis='x', rotation=45, labelsize=10)
            ax.tick_params(axis='y', labelsize=10)

            # Verhindert das Abschneiden von Achsen und Labels
            plt.tight_layout()

            for widget in frame_chart.winfo_children():
                widget.destroy()
            canvas = FigureCanvasTkAgg(figure, master=frame_chart)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=BOTH, expand=True, pady=0)

        except Exception as e:
            lbl_result.config(text=f"Fehler bei der Analyse: {e}", fg="red")

    def exit_to_main_gui():
        # Schließt die aktuelle GUI und gibt die Kontrolle an die Haupt-GUI zurück
        root.quit()
        root.destroy()  # Sub-GUI Fenster schließen

    # Erstelle die Haupt-GUI für die Emotionserkennung
    root = Tk()
    root.title("Emotionserkennung")
    root.state('zoomed')
    root.configure(bg="white")

    lbl_title = Label(root, text="Bild hochladen und analysieren", font=("Arial", 16))
    lbl_title.pack(pady=10)

    frame_main = Frame(root)
    frame_main.pack(fill=BOTH, expand=True, padx=10, pady=10)

    frame_image = Frame(frame_main, width=450, height=450)
    frame_image.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
    lbl_image = Label(frame_image)
    lbl_image.pack()

    frame_chart = Frame(frame_main, width=450, height=450)
    frame_chart.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

    lbl_result = Label(root, text="", font=("Arial", 12))
    lbl_result.pack(pady=5)

    btn_upload = Button(root, text="Bild hochladen", command=upload_and_analyze, width=20, height=2, font=("Arial", 12))
    btn_upload.pack(pady=5)

    # Exit-Button unten links platzieren
    frame_exit = Frame(root, bg="white")  # Separates Frame für Exit-Button
    frame_exit.pack(side=BOTTOM, fill=X, padx=10, pady=10)

    btn_exit = Button(frame_exit, text="Exit", command=exit_to_main_gui, width=10, height=2, font=("Arial", 12), bg="red", fg="white")
    btn_exit.pack(anchor="w")  # Button linksbündig ausrichten

    root.mainloop()

if __name__ == "__main__":
    start_gui()
