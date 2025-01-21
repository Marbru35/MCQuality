from tkinter import *
from tkinter.ttk import Separator
import subprocess
import os
import threading

# Verzeichnis der Skripte
current_dir = os.path.dirname(os.path.abspath(__file__))

# Dynamisches Auffinden des Python-Interpreters in der virtuellen Umgebung
def find_python_interpreter():
    possible_envs = [name for name in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, name))]
    for env in possible_envs:
        python_path = os.path.join(current_dir, env, "Scripts", "python.exe")  # Für Windows
        if os.path.exists(python_path):
            return python_path
    return "python"  # Fallback auf globalen Python-Interpreter

python_path = find_python_interpreter()

# Hauptfenster erstellen
frame = Tk()

def open_sub_gui(script_name, executing_text):
    def run_sub_gui():
        try:
            # Setze den Status-Text und aktualisiere die GUI
            clicked.config(text=executing_text, fg="green")
            frame.update()  # GUI sofort aktualisieren

            # Verzögerung von 1 Sekunde, bevor das Hauptfenster versteckt wird
            def hide_main_gui():
                frame.withdraw()  # Versteckt das Hauptfenster

                # Sub-GUI starten
                process = subprocess.Popen([python_path, script_name], cwd=current_dir)

                # Warten, bis das Sub-GUI-Skript beendet ist
                process.wait()

                # Wenn Sub-GUI beendet wird, Hauptfenster wieder sichtbar machen
                frame.deiconify()  # Haupt-GUI wieder anzeigen
                clicked.config(text="Start the emotion recognition", fg="firebrick")
                frame.state('zoomed')  # Maximiert das Fenster

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
    # Schließt die Haupt-GUI
    frame.quit()

frame.title("Emotion Detection - Controller")

# Maximieren des Fensters
frame.state('zoomed')  # Maximiert das Fenster auf die Bildschirmgröße

# Responsivität aktivieren
frame.grid_columnconfigure(0, weight=1)  # Platz links
frame.grid_columnconfigure(1, weight=1)  # Dropdown-Button
frame.grid_columnconfigure(2, weight=1)  # Start-Button
frame.grid_columnconfigure(3, weight=1)  # Platz rechts
frame.grid_rowconfigure(0, weight=0)     # Zeile für Buttons
frame.grid_rowconfigure(1, weight=0)     # Zeile für Clicked-Label
frame.grid_rowconfigure(2, weight=0)     # Zeile für Trennlinie
frame.grid_rowconfigure(3, weight=3)     # Zeile für Auswertungsgrafiken (größerer Platz)
frame.grid_rowconfigure(4, weight=0)     # Zeile für Exit und Hinweise

# Modus-Auswahl (Dropdown)
mode = StringVar(value="Modus")  # Standardwert
options = ["Static", "Real-Time"]

option_menu = OptionMenu(frame, mode, *options)
option_menu.config(
    width=12,
    font=("Arial", 12, "bold"),  # Schriftart fett
    bg="lightblue",  # Hintergrundfarbe des Dropdowns
    fg="black",       # Schriftfarbe des Dropdowns
    activebackground="blue",  # Hintergrundfarbe beim Hover
    activeforeground="white"  # Schriftfarbe beim Hover
)
option_menu.grid(row=0, column=1, padx=10, pady=10, sticky="ew")  # Zentriert über Spaltengewicht

# Start-Button
start = Button(
    frame,
    text="Start",
    command=button_action,
    width=10,
    height=2,
    bg="lime",
    fg="darkgreen",
    font=("Arial", 12, "bold"),  # Statische Größe
    relief="raised",
    bd=5,
)
start.grid(row=0, column=2, padx=10, pady=10, sticky="ew")  # Rechts daneben, ebenfalls zentriert

# Clicked-Label (unterhalb der Buttons)
clicked = Label(
    frame,
    text="Start the emotion recognition",
    font=("Arial", 12),  # Schriftgröße
    fg="firebrick"  # Schriftfarbe
)
clicked.grid(row=1, column=0, columnspan=4, pady=5, sticky="n")  # Zentriert unter den Buttons

# Trennlinie weiter nach oben verschieben
separator = Separator(frame, orient="horizontal")
separator.grid(row=2, column=0, columnspan=4, sticky="ew", pady=5)  # Trennlinie über gesamte Breite (weniger Padding)

# Platz für Auswertungsgrafiken
graphics_label = Label(frame, text="Hier werden Auswertungsgrafiken angezeigt", font=("Helvetica", 10), fg="gray")
graphics_label.grid(row=3, column=0, columnspan=4, pady=20, sticky="nsew")  # Mittig und flexibel

# Exit-Button unten links (größerer Exit-Button)
exit = Button(frame, text="Exit", command=exit_to_main_gui, bg="red", fg="white", width=15, height=3)
exit.grid(row=4, column=0, sticky="sw", padx=10, pady=20)  # Unten links

frame.mainloop()
