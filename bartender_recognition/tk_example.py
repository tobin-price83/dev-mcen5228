# Import required Libraries
from tkinter import *
from PIL import Image, ImageTk
import cv2
import video_pipeline

# Create an instance of TKinter Window or frame
win = Tk()

# Set the size of the window
win.geometry("700x350")  # Create a Label to capture the Video frames
label = Label(win)
label.grid(row=0, column=0)
video_capture = cv2.VideoCapture(video_pipeline.gstreamer_pipeline(flip_method=2, frameskip=4), cv2.CAP_GSTREAMER)
# cap = cv2.VideoCapture(0)
ret, cap =video_capture.read()

# Define function to show frame


def show_frames():
    # Get the latest frame and convert into Image
    # cv2image=cv2.cvtColor(cap, cv2.COLOR_BGR2RGB)
    img=Image.fromarray(cap)

    # Convert image to PhotoImage
    imgtk=ImageTk.PhotoImage(image = img)
    label.imgtk=imgtk
    label.configure(image = imgtk)


# Repeat after an interval to capture continiously
label.after(20, show_frames)

show_frames()
win.mainloop()
