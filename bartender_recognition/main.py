import gui
import video_recognition

# Global variables
known_face_encodings = []
known_face_metadata = []

video_recognition.capture_mode()
break_cond = video_recognition.live_video()

gui.make_gui()