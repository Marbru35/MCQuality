"""
Static Emotion Detection GUI

This script allows users to upload an image, analyze the emotions in it using the DeepFace library,
and display the dominant emotion along with a bar chart of emotion probabilities.
The interface is built using Tkinter.
"""

from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from deepface import DeepFace
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def start_gui():
    """
    Launches the GUI for static emotion detection.
    The interface provides options to upload an image, analyze its emotions, and display the results.
    """
    
    def upload_and_analyze():
        """
        Handles the upload and emotion analysis of an image.
        It uses the DeepFace library to analyze the uploaded image and displays
        the dominant emotion along with a bar chart of emotion probabilities.
        """
        # Open a file dialog for image selection
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if not file_path:
            lbl_result.config(text="No file selected.", fg="red")
            return

        try:
            # Analyze the emotions in the image using DeepFace
            analysis = DeepFace.analyze(img_path=file_path, actions=['emotion'])
            emotions = analysis[0]['emotion']
            dominant_emotion = analysis[0]['dominant_emotion']

            # Display the dominant emotion as a status label
            lbl_result.config(text=f"Dominant Emotion: {dominant_emotion}", fg="green")

            # Open and resize the uploaded image
            img = Image.open(file_path)

            # Define the maximum size for display
            max_size = (450, 450)
            img.thumbnail(max_size)

            # Convert the image to a format compatible with Tkinter
            img_tk = ImageTk.PhotoImage(img)
            lbl_image.config(image=img_tk)
            lbl_image.image = img_tk

            # Create a bar chart for emotion probabilities
            figure = plt.Figure(figsize=(6, 5), dpi=100)
            ax = figure.add_subplot(111)
            ax.bar(emotions.keys(), emotions.values(), color='skyblue')
            ax.set_ylim(0, 100)
            ax.set_xlabel("Emotions", fontsize=12)
            ax.set_ylabel("Probability (%)", fontsize=12)
            ax.tick_params(axis='x', rotation=45, labelsize=10)
            ax.tick_params(axis='y', labelsize=10)

            plt.tight_layout()

            # Clear any existing charts in the frame and display the new one
            for widget in frame_chart.winfo_children():
                widget.destroy()
            canvas = FigureCanvasTkAgg(figure, master=frame_chart)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=BOTH, expand=True, pady=0)

        except Exception as e:
            lbl_result.config(text=f"Error during analysis: {e}", fg="red")

    def exit_to_main_gui():
        """
        Closes the current GUI and exits the application.
        """
        root.quit()
        root.destroy()

    # Initialize the main Tkinter window
    root = Tk()
    root.title("Static Emotion Detection")
    root.state('zoomed')
    root.configure(bg="white")

    # Add a title label
    lbl_title = Label(root, text="Upload and Analyze an Image", font=("Arial", 16))
    lbl_title.pack(pady=10)

    # Main frame for displaying the image and chart
    frame_main = Frame(root)
    frame_main.pack(fill=BOTH, expand=True, padx=10, pady=10)

    # Frame for displaying the uploaded image
    frame_image = Frame(frame_main, width=450, height=450)
    frame_image.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
    lbl_image = Label(frame_image)
    lbl_image.pack()

    # Frame for displaying the emotion bar chart
    frame_chart = Frame(frame_main, width=450, height=450)
    frame_chart.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

    # Label for displaying the dominant emotion or status messages
    lbl_result = Label(root, text="", font=("Arial", 12))
    lbl_result.pack(pady=5)

    # Button for uploading an image and analyzing emotions
    btn_upload = Button(root, text="Upload Image", command=upload_and_analyze, width=20, height=2, font=("Arial", 12))
    btn_upload.pack(pady=5)

    # Frame for the Exit button at the bottom
    frame_exit = Frame(root, bg="white") 
    frame_exit.pack(side=BOTTOM, fill=X, padx=10, pady=10)

    # Exit button to close the application
    btn_exit = Button(frame_exit, text="Exit", command=exit_to_main_gui, width=10, height=2, font=("Arial", 12), bg="red", fg="white")
    btn_exit.pack(anchor="w")

    # Start the Tkinter main loop
    root.mainloop()

# Launch the application when the script is run
if __name__ == "__main__":
    start_gui()