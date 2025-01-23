from tkinter import *
from tkinter.ttk import Separator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
import subprocess
import os
import threading

# Verzeichnis der Skripte
current_dir = os.path.dirname(os.path.abspath(__file__))

# CSV-Datei leeren
def clear_csv_file():
    with open("emotions_results.csv", "w", newline="") as csvfile:
        csvfile.write("emotion\n")

# Dynamisches Auffinden des Python-Interpreters in der virtuellen Umgebung
def find_python_interpreter():
    possible_envs = [name for name in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, name))]
    for env in possible_envs:
        python_path = os.path.join(current_dir, env, "Scripts", "python.exe")
        if os.path.exists(python_path):
            return python_path
    return "python"  # Fallback auf globalen Python-Interpreter

python_path = find_python_interpreter()

# Funktion zur Erstellung eines Balkendiagramms
def create_bar_chart(frame, emotion_counts):
    fig_bar, ax_bar = plt.subplots(figsize=(5, 4))
    emotion_counts.plot(kind='bar', color='skyblue', ax=ax_bar)
    ax_bar.set_title("Percentage of Detected Emotions (Bar Chart)", fontsize=12)
    ax_bar.set_xlabel("Emotions", fontsize=10)
    ax_bar.set_ylabel("Percentage (%)", fontsize=10)
    ax_bar.set_xticklabels(ax_bar.get_xticklabels(), rotation=45)
    ax_bar.grid(axis='y', linestyle='--', alpha=0.7)

    for i, value in enumerate(emotion_counts):
        ax_bar.text(i, value + 1, f"{value:.1f}%", ha='center', fontsize=8)

    canvas_bar = FigureCanvasTkAgg(fig_bar, master=frame)
    canvas_bar.draw()
    canvas_bar.get_tk_widget().pack(fill=BOTH, expand=True)

# Funktion zur Erstellung eines Kuchendiagramms
def create_pie_chart(frame, emotion_counts):
    fig_pie, ax_pie = plt.subplots(figsize=(5, 4))
    emotion_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['skyblue', 'orange', 'green', 'red', 'purple', 'yellow'], ax=ax_pie)
    ax_pie.set_title("Percentage of Detected Emotions (Pie Chart)", fontsize=14)
    ax_pie.set_ylabel("")  # Entfernt das Standard-Y-Label

    canvas_pie = FigureCanvasTkAgg(fig_pie, master=frame)
    canvas_pie.draw()
    canvas_pie.get_tk_widget().pack(fill=BOTH, expand=True)

# Funktion zur Darstellung der Diagramme
def show_emotion_analysis():
    try:
        # CSV-Datei laden
        df = pd.read_csv("emotions_results.csv")

        # Häufigkeit der Emotionen zählen und in Prozentsätze umwandeln
        emotion_counts = df['emotion'].value_counts(normalize=True) * 100  # Prozentuale Häufigkeit

        # Zuvor vorhandene Widgets im Grafik-Bereich entfernen
        for widget in graphics_area.winfo_children():
            widget.destroy()

        # Linker Bereich: Balkendiagramm
        left_frame = Frame(graphics_area, bg="white")
        left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
        create_bar_chart(left_frame, emotion_counts)

        # Rechter Bereich: Kuchendiagramm
        right_frame = Frame(graphics_area, bg="white")
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=5, pady=5)
        create_pie_chart(right_frame, emotion_counts)

        # Sobald die Diagramme erfolgreich erstellt wurden, die Nachricht entfernen
        if resize_message_label.winfo_ismapped():
            resize_message_label.grid_forget()

    except FileNotFoundError:
        # Nachricht anzeigen, wenn keine Datei gefunden wird
        error_label = Label(graphics_area, text="No data available. Please run the detection first.", fg="red", font=("Helvetica", 12))
        error_label.pack(fill=BOTH, expand=True)

# Funktion zur Überprüfung der Fenstergröße
def check_window_size():
    window_width = frame.winfo_width()

    # Wenn das Fenster zu klein ist, die Nachricht anzeigen
    if window_width < 1000:
        resize_message_label.config(text="Widen the frame to see the results.")
        if not resize_message_label.winfo_ismapped():
            resize_message_label.grid(row=3, column=0, columnspan=4, pady=10, sticky="nsew")
    else:
        # Wenn das Fenster groß genug ist, entfernen wir die Nachricht
        if resize_message_label.winfo_ismapped():
            resize_message_label.grid_forget()

    # Wiederhole die Überprüfung alle 100 ms
    frame.after(100, check_window_size)

# Hauptfenster erstellen
frame = Tk()



def open_sub_gui(script_name, executing_text):
    def run_sub_gui():
        try:
            # CSV-Datei leeren, bevor das Sub-GUI gestartet wird
            clear_csv_file()

            # Setze den Status-Text und aktualisiere die GUI
            clicked.config(text=executing_text, fg="green")
            frame.update()  # GUI sofort aktualisieren

            # Verzögerung von 1 Sekunde, bevor das Hauptfenster versteckt wird
            def hide_main_gui():
                frame.withdraw()  # Versteckt das Hauptfenster

                # Sub-GUI starten
                process = subprocess.Popen([python_path, script_name], cwd=current_dir)

                # Warten, bis das Sub-GUI beendet ist
                process.wait()

                # Wenn Sub-GUI beendet wird, Hauptfenster wieder sichtbar machen
                frame.deiconify()  # Haupt-GUI wieder anzeigen
                clicked.config(text="Start the emotion recognition", fg="firebrick")
                frame.state('zoomed')  # Maximiert das Fenster
                show_emotion_analysis()  # Emotionen nach Beendigung analysieren

            # 1 Sekunde warten, bevor das Hauptfenster ausgeblendet wird
            frame.after(1000, hide_main_gui)  # 1000ms = 1 Sekunde

        except Exception as e:
            # Fehlerbehandlung
            clicked.config(text=f"Error: {e}", fg="red")
            frame.deiconify()

    # Starten des Sub-Skripts im Hintergrund als Thread
    thread = threading.Thread(target=run_sub_gui)
    thread.start()

def button_action():
    selected_mode = mode.get()
    if selected_mode == "Modus":
        clicked.config(text="Please select a mode first!", fg="red")  # Hinweis, falls kein Modus gewählt wurde
    elif selected_mode == "Static":
        open_sub_gui("EmotionDetectionGUI.py", "Executing Static emotion recognition...")
    elif selected_mode == "Real-Time":
        open_sub_gui("EmotionDetectionRealTime.py", "Executing Real-Time emotion recognition...")

def exit_to_main_gui():
    # CSV-Datei leeren, bevor das Hauptfenster geschlossen wird
    clear_csv_file()
    # Schließt die Haupt-GUI
    frame.quit()

frame.title("Emotion Detection - Controller")

# Maximieren des Fensters
frame.state('zoomed')  # Maximiert das Fenster auf die Bildschirmgröße

# Mindestgröße des Fensters setzen
frame.minsize(600, 400)

# Maximale Größe des Fensters setzen
frame.maxsize(1600, 1200)

# Responsivität aktivieren
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)
frame.grid_columnconfigure(3, weight=1)
frame.grid_rowconfigure(0, weight=0)
frame.grid_rowconfigure(1, weight=0)
frame.grid_rowconfigure(2, weight=0)
frame.grid_rowconfigure(3, weight=4)
frame.grid_rowconfigure(4, weight=0)

# Modus-Auswahl (Dropdown)
mode = StringVar(value="Modus")
options = ["Static", "Real-Time"]

option_menu = OptionMenu(frame, mode, *options)
option_menu.config(
    width=12,
    font=("Arial", 12, "bold"),
    bg="lightblue",
    fg="black",
    activebackground="blue",
    activeforeground="white"
)
option_menu.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

# Start-Button
start = Button(
    frame,
    text="Start",
    command=button_action,
    width=10,
    height=2,
    bg="lime",
    fg="darkgreen",
    font=("Arial", 12, "bold"),
    relief="raised",
    bd=5,
)
start.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

# Clicked-Label
clicked = Label(
    frame,
    text="Start the emotion recognition",
    font=("Arial", 12),
    fg="firebrick"
)
clicked.grid(row=1, column=0, columnspan=4, pady=5, sticky="n")

# Trennlinie
separator = Separator(frame, orient="horizontal")
separator.grid(row=2, column=0, columnspan=4, sticky="ew", pady=5)

# Platz für Auswertungsgrafiken
graphics_area = Frame(frame, bg="white")
graphics_area.grid(row=3, column=0, columnspan=4, pady=20, sticky="nsew")

placeholder_label = Label(graphics_area, text="Hier werden Auswertungsgrafiken angezeigt", font=("Helvetica", 10), fg="gray")
placeholder_label.pack(fill=BOTH, expand=True)

# Nachricht, die angezeigt wird, wenn das Fenster zu klein ist
resize_message_label = Label(frame, text="Widen the frame to see the results.", fg="red", font=("Arial", 12))
resize_message_label.grid(row=3, column=0, columnspan=4, pady=10, sticky="nsew")
resize_message_label.grid_forget()  # Verstecke die Nachricht zu Beginn
check_window_size()

# Exit-Button
exit = Button(frame, text="Exit", command=exit_to_main_gui, bg="red", fg="white", width=10, height=2)
exit.grid(row=4, column=0, sticky="sw", padx=10, pady=20)

# Überprüfe die Fenstergröße regelmäßig
frame.after(1000, check_window_size)  # Überprüfe alle 1 Sekunde die Fenstergröße

frame.mainloop()
