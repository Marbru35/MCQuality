"""
Main GUI for Emotion Detection

This script serves as the central GUI to select between static image-based
emotion detection and real-time emotion detection via webcam.
"""

from tkinter import *
from tkinter.ttk import Separator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
import subprocess
import os
import threading

# Directory paths for detection scripts and results
current_dir = os.path.dirname(os.path.abspath(__file__))
detection_dir = os.path.join(current_dir, "detection")
results_dir = os.path.join(current_dir, "results")
csv_path = os.path.join(results_dir, "emotions_results.csv")

def clear_csv_file():
    """
    Clears the CSV file to reset stored emotions.
    This ensures that each new session starts with a clean dataset.
    """
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)  # Create results directory if it does not exist
    with open(csv_path, "w", newline="") as csvfile:
        csvfile.write("time,dominant_emotion,angry,disgust,fear,happy,sad,surprise,neutral\n")

def find_python_interpreter():
    """
    Finds the appropriate Python interpreter in the virtual environment.
    If no virtual environment is detected, it falls back to the system's Python interpreter.
    """
    possible_envs = [name for name in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, name))]
    for env in possible_envs:
        python_path = os.path.join(current_dir, env, "Scripts", "python.exe")
        if os.path.exists(python_path):
            return python_path
    return "python"  # Default to global Python interpreter if none is found

python_path = find_python_interpreter()

# Color map for charts
COLOR_MAP = {
    "fear": "purple", "neutral": "skyblue", "surprise": "yellow",
    "happy": "green", "sad": "orange", "angry": "red", "disgust": "pink"
}

def create_bar_chart(frame, emotion_counts):
    """
    Generates a bar chart displaying the percentage distribution of dominant emotions.
    
    Parameters:
    - frame: The Tkinter frame where the chart will be displayed.
    - emotion_counts: A Pandas Series containing emotion labels and their respective percentages.
    """
    colors = [COLOR_MAP[emotion] for emotion in emotion_counts.index]

    fig_bar, ax_bar = plt.subplots(figsize=(5, 4))
    emotion_counts.plot(kind='bar', color=colors, ax=ax_bar)
    ax_bar.set_title("Percentage of Dominant Emotions (Bar Chart)", fontsize=10)
    ax_bar.set_xlabel("Emotions", fontsize=10)
    ax_bar.set_ylabel("Percentage (%)", fontsize=10)
    ax_bar.set_xticklabels(ax_bar.get_xticklabels(), rotation=0, fontsize=9)
    ax_bar.grid(axis='y', linestyle='--', alpha=0.7)

    # Display emotion percentage above bars
    for i, value in enumerate(emotion_counts):
        ax_bar.text(i, value + 1, f"{value:.1f}%", ha='center', fontsize=7)

    canvas_bar = FigureCanvasTkAgg(fig_bar, master=frame)
    canvas_bar.draw()
    canvas_bar.get_tk_widget().pack(fill=BOTH, expand=True)

def create_time_based_line_chart(frame, emotions_data):
    """
    Generates a time-based line chart displaying emotion intensity over time.
    Includes a hover effect to emphasize selected lines.

    Parameters:
    - frame: The Tkinter frame where the chart will be displayed.
    - emotions_data: A Pandas DataFrame containing time and emotion intensity values.
    """
    if emotions_data.empty:
        print("No data available for line chart.")
        return

    fig_line, ax_line = plt.subplots(figsize=(6, 5))

    def smooth(values, window_size=5):
        """Applies a moving average smoothing to the data."""
        return pd.Series(values).rolling(window=window_size, min_periods=1).mean()

    normalized_time = [x / (len(emotions_data) - 1) for x in range(len(emotions_data))]

    lines = {}
    for emotion in COLOR_MAP.keys():
        if emotion in emotions_data.columns:
            smoothed_values = smooth(emotions_data[emotion])
            line, = ax_line.plot(
                normalized_time,
                smoothed_values,
                label=emotion,
                color=COLOR_MAP[emotion],
                linestyle='-',
                linewidth=1,
                alpha=0.7
            )
            lines[emotion] = line

    ax_line.set_title("Emotion Intensity Over Time", fontsize=10)
    ax_line.set_xlabel("Time")
    ax_line.set_ylabel("Intensity", fontsize=10)
    ax_line.grid(axis='y', linestyle='--', alpha=0.5)
    ax_line.set_xticks([])

    legend = ax_line.legend(title="Emotions", loc='upper left', fontsize=9)
    legend_items = legend.get_lines()
    legend_mapping = {legend_line: emotion for emotion, legend_line in zip(lines.keys(), legend_items)}

    for legend_line in legend_items:
        legend_line.set_linewidth(2.5)

    def on_hover(event):
        """Hover effect to highlight the selected emotion."""
        hovered = False
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

        if not hovered and event.inaxes == ax_line:
            for emotion, line in lines.items():
                if line.contains(event)[0]:
                    line.set_alpha(1.0)
                    line.set_linewidth(2)
                    hovered = True
                else:
                    line.set_alpha(0.1)
                    line.set_linewidth(1)

        if not hovered:
            for line in lines.values():
                line.set_alpha(0.7)
                line.set_linewidth(1)

        fig_line.canvas.draw_idle()

    fig_line.canvas.mpl_connect('motion_notify_event', on_hover)

    canvas_line = FigureCanvasTkAgg(fig_line, master=frame)
    canvas_line.draw()
    canvas_line.get_tk_widget().pack(fill=BOTH, expand=True)

def show_emotion_analysis():
    """
    Reads emotion analysis data from CSV and updates the GUI with visualizations.
    Displays a bar chart for dominant emotions and a time-based line chart for intensity trends.
    """
    try:
        emotions_data = pd.read_csv(csv_path)
        emotion_counts = emotions_data['dominant_emotion'].value_counts(normalize=True) * 100

        for widget in graphics_area.winfo_children():
            widget.destroy()

        left_frame = Frame(graphics_area, bg="white")
        left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
        create_bar_chart(left_frame, emotion_counts)

        right_frame = Frame(graphics_area, bg="white")
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=5, pady=5)
        create_time_based_line_chart(right_frame, emotions_data)

        if resize_message_label.winfo_ismapped():
            resize_message_label.grid_forget()

    except FileNotFoundError:
        error_label = Label(graphics_area, text="No data available. Please run the detection first.", fg="red", font=("Helvetica", 12))
        error_label.pack(fill=BOTH, expand=True)

def open_sub_gui(script_name, executing_text):
    """
    Opens the selected sub-GUI for emotion detection.

    Parameters:
    - script_name: Name of the Python script to execute.
    - executing_text: Status message to display while execution is in progress.
    """
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
    """
    Handles user selection for emotion detection mode.
    Initiates either static image analysis or real-time detection.
    """
    selected_mode = mode.get()
    if selected_mode == "Modus":
        clicked.config(text="Please select a mode first!", fg="red")
    elif selected_mode == "Static":
        open_sub_gui("emotion_detection_static.py", "Executing Static emotion recognition...")
    elif selected_mode == "Real-Time":
        open_sub_gui("emotion_detection_realtime.py", "Executing Real-Time emotion recognition...")

def exit_to_main_gui():
    """Exits the main GUI and clears the CSV file."""
    clear_csv_file()
    frame.quit()

# Initialize GUI
frame = Tk()
frame.title("Emotion Detection - Controller")
frame.state('zoomed')
frame.minsize(600, 400)
frame.maxsize(1600, 1200)

frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)
frame.grid_columnconfigure(3, weight=1)
frame.grid_rowconfigure(3, weight=4)

mode = StringVar(value="Modus")
options = ["Static", "Real-Time"]

option_menu = OptionMenu(frame, mode, *options)
option_menu.config(width=12, font=("Arial", 12, "bold"), bg="lightblue", fg="black", activebackground="blue", activeforeground="white")
option_menu.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

start = Button(frame, text="Start", command=button_action, width=10, height=2, bg="lime", fg="darkgreen", font=("Arial", 12, "bold"))
start.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

clicked = Label(frame, text="Start the emotion recognition", font=("Arial", 12), fg="firebrick")
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

frame.mainloop()