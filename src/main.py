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

# Detection Verzeichnis
detection_dir = os.path.join(current_dir, "detection")

# CSV Verzeichnis
results_dir = os.path.join(current_dir, "results")
csv_path = os.path.join(results_dir, "emotions_results.csv")

# CSV-Datei leeren
def clear_csv_file():
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)  # Ergebnisse-Ordner erstellen, falls er nicht existiert
    with open(csv_path, "w", newline="") as csvfile:
        csvfile.write("time,dominant_emotion,angry,disgust,fear,happy,sad,surprise,neutral\n")

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
    color_map = {
        "fear": "purple",
        "neutral": "skyblue",
        "surprise": "yellow",
        "happy": "green",
        "sad": "orange",
        "angry": "red",
        "disgust": "pink"
    }

    colors = [color_map[emotion] for emotion in emotion_counts.index]

    fig_bar, ax_bar = plt.subplots(figsize=(5, 4))
    emotion_counts.plot(kind='bar', color=colors, ax=ax_bar)
    ax_bar.set_title("Percentage of Dominant Emotions (Bar Chart)", fontsize=10)
    ax_bar.set_xlabel("Emotions", fontsize=10)
    ax_bar.set_ylabel("Percentage (%)", fontsize=10)
    ax_bar.set_xticklabels(ax_bar.get_xticklabels(), rotation=0, fontsize=9)
    ax_bar.grid(axis='y', linestyle='--', alpha=0.7)

    for i, value in enumerate(emotion_counts):
        ax_bar.text(i, value + 1, f"{value:.1f}%", ha='center', fontsize=7)

    canvas_bar = FigureCanvasTkAgg(fig_bar, master=frame)
    canvas_bar.draw()
    canvas_bar.get_tk_widget().pack(fill=BOTH, expand=True)

# Funktion zur Erstellung einer zeitbasierten Liniengrafik
def create_time_based_line_chart(frame, emotions_data):
    if emotions_data.empty:
        print("Keine Daten für die Liniengrafik vorhanden.")
        return

    fig_line, ax_line = plt.subplots(figsize=(6, 5))

    # Definiere Farben für Emotionen
    color_map = {
        "fear": "purple",
        "neutral": "skyblue",
        "surprise": "yellow",
        "happy": "green",
        "sad": "orange",
        "angry": "red",
        "disgust": "pink"
    }

    # Glättungsfunktion (Moving Average)
    def smooth(values, window_size=5):
        return pd.Series(values).rolling(window=window_size, min_periods=1).mean()

    # Normalisierung der Zeitachse
    normalized_time = [x / (len(emotions_data) - 1) for x in range(len(emotions_data))]

    # Emotionen plotten und Linien speichern
    lines = {}
    for emotion in color_map.keys():
        if emotion in emotions_data.columns:
            smoothed_values = smooth(emotions_data[emotion])
            line, = ax_line.plot(
                normalized_time,         # Normalisierte Zeitachse
                smoothed_values,         # Y-Werte: Intensität
                label=emotion,
                color=color_map[emotion],
                linestyle='-',           # Keine Marker
                linewidth=1,             # Dünnere Linien
                alpha=0.7                # Transparenz für bessere Sichtbarkeit
            )
            lines[emotion] = line

    # Titel und Achsenbeschriftungen
    ax_line.set_title("Emotion Intensity Over Time", fontsize=10)
    ax_line.set_xlabel("Time")
    ax_line.set_ylabel("Intensity", fontsize=10)
    ax_line.grid(axis='y', linestyle='--', alpha=0.5)

    # Entferne die X-Ticks (Zeitstempel unwichtig)
    ax_line.set_xticks([])

    # Erstelle die Legende
    legend = ax_line.legend(title="Emotions", loc='upper left', fontsize=9)
    legend_items = legend.get_lines()  # Erhalte die Legendenlinien
    legend_mapping = {legend_line: emotion for emotion, legend_line in zip(lines.keys(), legend_items)}

    # Setze die Linienbreite in der Legende
    for legend_line in legend_items:
        legend_line.set_linewidth(2.5)  # Dickere Linien in der Legende

    # Interaktive Funktion für das Hover-Event
    def on_hover(event):
        hovered = False

        # Prüfen, ob der Mauszeiger über einer Legende schwebt
        for legend_line in legend_items:
            if legend_line.contains(event)[0]:
                hovered = True
                emotion = legend_mapping[legend_line]
                for emo, line in lines.items():
                    if emo == emotion:
                        line.set_alpha(1.0)
                        line.set_linewidth(2)
                    else:
                        line.set_alpha(0.1)
                        line.set_linewidth(1)
                break

        # Prüfen, ob der Mauszeiger über einer Linie schwebt und gerade nicht auf der Legende ist
        if not hovered and event.inaxes == ax_line:
            for emotion, line in lines.items():
                if line.contains(event)[0]:
                    line.set_alpha(1.0)
                    line.set_linewidth(2)
                    hovered = True
                else:
                    line.set_alpha(0.1)
                    line.set_linewidth(1)

        # Wenn keine Linie oder Legende hervorgehoben ist, alles zurücksetzen
        if not hovered:
            for line in lines.values():
                line.set_alpha(0.7)
                line.set_linewidth(1)

        fig_line.canvas.draw_idle()  # Neu zeichnen

    # Event mit der Figure verbinden
    fig_line.canvas.mpl_connect('motion_notify_event', on_hover)

    canvas_line = FigureCanvasTkAgg(fig_line, master=frame)
    canvas_line.draw()
    canvas_line.get_tk_widget().pack(fill=BOTH, expand=True)

# Funktion zur Darstellung der Diagramme
# Funktion zur Darstellung der Diagramme
def show_emotion_analysis():
    try:
        # Aktualisierter Pfad: CSV-Datei aus dem neuen "results"-Ordner laden
        emotions_data = pd.read_csv(csv_path)

        # Häufigkeit der dominanten Emotionen in Prozent umrechnen
        emotion_counts = emotions_data['dominant_emotion'].value_counts(normalize=True) * 100

        # Zuvor vorhandene Widgets im Grafik-Bereich entfernen
        for widget in graphics_area.winfo_children():
            widget.destroy()

        # Linker Bereich: Balkendiagramm
        left_frame = Frame(graphics_area, bg="white")
        left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
        create_bar_chart(left_frame, emotion_counts)

        # Rechter Bereich: Zeitbasierte Liniengrafik
        right_frame = Frame(graphics_area, bg="white")
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=5, pady=5)
        create_time_based_line_chart(right_frame, emotions_data)

        # Nachricht entfernen, wenn Diagramme erstellt wurden
        if resize_message_label.winfo_ismapped():
            resize_message_label.grid_forget()

    except FileNotFoundError:
        # Fehlerbehandlung, falls die CSV-Datei nicht existiert
        error_label = Label(graphics_area, text="No data available. Please run the detection first.", fg="red", font=("Helvetica", 12))
        error_label.pack(fill=BOTH, expand=True)

# Funktion zur Überprüfung der Fenstergröße
def check_window_size():
    window_width = frame.winfo_width()

    if window_width < 1000:
        resize_message_label.config(text="Widen the frame to see the results.")
        if not resize_message_label.winfo_ismapped():
            resize_message_label.grid(row=3, column=0, columnspan=4, pady=10, sticky="nsew")
    else:
        if resize_message_label.winfo_ismapped():
            resize_message_label.grid_forget()

    frame.after(100, check_window_size)

# Hauptfenster erstellen
frame = Tk()

def open_sub_gui(script_name, executing_text):
    def run_sub_gui():
        try:
            clear_csv_file()
            clicked.config(text=executing_text, fg="green")
            frame.update()

            def hide_main_gui():
                frame.withdraw()
                script_path = os.path.join(detection_dir, script_name)
                process = subprocess.Popen([python_path, script_path], cwd=current_dir)
                process.wait()
                frame.deiconify()
                clicked.config(text="Start the emotion recognition", fg="firebrick")
                frame.state('zoomed')
                show_emotion_analysis()

            frame.after(1000, hide_main_gui)

        except Exception as e:
            clicked.config(text=f"Error: {e}", fg="red")
            frame.deiconify()

    thread = threading.Thread(target=run_sub_gui)
    thread.start()

def button_action():
    selected_mode = mode.get()
    if selected_mode == "Modus":
        clicked.config(text="Please select a mode first!", fg="red")
    elif selected_mode == "Static":
        open_sub_gui("emotion_detection_static.py", "Executing Static emotion recognition...")
    elif selected_mode == "Real-Time":
        open_sub_gui("emotion_detection_realtime.py", "Executing Real-Time emotion recognition...")

def exit_to_main_gui():
    clear_csv_file()
    frame.quit()

frame.title("Emotion Detection - Controller")

frame.state('zoomed')
frame.minsize(600, 400)
frame.maxsize(1600, 1200)

frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)
frame.grid_columnconfigure(3, weight=1)
frame.grid_rowconfigure(0, weight=0)
frame.grid_rowconfigure(1, weight=0)
frame.grid_rowconfigure(2, weight=0)
frame.grid_rowconfigure(3, weight=4)
frame.grid_rowconfigure(4, weight=0)

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

clicked = Label(
    frame,
    text="Start the emotion recognition",
    font=("Arial", 12),
    fg="firebrick"
)
clicked.grid(row=1, column=0, columnspan=4, pady=5, sticky="n")

separator = Separator(frame, orient="horizontal")
separator.grid(row=2, column=0, columnspan=4, sticky="ew", pady=5)

graphics_area = Frame(frame, bg="white")
graphics_area.grid(row=3, column=0, columnspan=4, pady=10, sticky="nsew")

resize_message_label = Label(frame, text="Widen the frame to see the results.", fg="red", font=("Arial", 12))
resize_message_label.grid(row=3, column=0, columnspan=4, pady=10, sticky="nsew")
resize_message_label.grid_forget()

exit = Button(frame, text="Exit", command=exit_to_main_gui, bg="red", fg="white", width=10, height=1)
exit.grid(row=4, column=0, sticky="sw", padx=5, pady=5)

frame.after(1000, check_window_size)
frame.mainloop()
