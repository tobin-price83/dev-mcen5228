import platform
import cv2
import numpy as np
import face_recognition
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread

class VideoRecognition(QThread):
	known_face_encodings = []
	known_face_metadata = []

	face_locations = []
	face_encodings = []

	def running_on_jetson_nano():
		return platform.machine() == "aarch64"

	def clear_faces():
		known_face_encodings.clear()
		known_face_metadata.clear()

	def register_new_face(face_encoding,face_index,face_image):
		known_face_encodings.append(face_encoding)
		known_face_metadata.append({
			"face_index": face_index,
			"face_image": face_image
			})

	def lookup_known_face(face_encoding):
		metadata = None

		if len(known_face_encodings) == 0:
			return metadata

		face_distances = face_recognition.face_distance(
		known_face_encodings, 
		face_encoding
		)

		best_match_index = np.argmin(face_distances)

		if face_distances[best_match_index] < 0.6:
			metadata = known_face_metadata[best_match_index]

		return metadata

	def scale_coordinates(face_location):
		# unpack coordinates
		(top, right, bottom, left) = face_locations

		# scale to original dimensions
		top *= 2
		right *= 2
		bottom *= 2
		left *= 2

		return (top, right, bottom, left)

	def preview_frame(frame):
		# label all faces in frame
		face_names = []
		index = 0
		for face_location, face_encoding in zip(face_locations, face_encodings):

			index += 1
			face_names.append("Face " + str(index))

		# Display live capture preview
		for face_location, label in zip(face_locations, face_names):
			# print("Found face!")
			# Scale back up face locations since the frame we detected in was scaled to 1/2 size
			(top, right, bottom, left) = scale_coordinates(face_location)

			# Draw a box around the face
			cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

			# Draw a label with a name below the face
			cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
			font = cv2.FONT_HERSHEY_DUPLEX
			cv2.putText(frame, label, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


	def capture_faces(frame,face_locations,face_encodings,margin=0):
		# loop through and save faces in photo
		print("Number of faces:",len(face_locations))
		index = 0
		for (top, right, bottom, left), face_encoding in zip(face_locations,face_encodings):
			# resize crop bounds
			top *= 2
			right *=2
			bottom *=2
			left *= 2

			# add margin around crop area
			top -= margin
			right += margin
			bottom += margin
			left += margin

			# crop to face
			face_frame = frame[top:bottom, left:right]
			face_frame = cv2.resize(face_frame,(150,150))

			# add to instance of known faces
			index += 1
			register_new_face(face_encoding,index,face_frame)
			print("Face",index,"saved")

	def find_faces(frame):
		face_locations = []

		# Resize frame of video to 1/2 size for faster face recognition processing
		small_frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)

		# Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
		rgb_small_frame = small_frame[:, :, ::-1]
		
		# locate faces in frame
		face_locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample=0, model='cnn')
		face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)







	# def capture_mode(margin=0):
	# 	# Initialize loop variables
	# 	print("Starting capture_mode")
	# 	window_title = "Position faces for photo capture"
	# 	model = 'hog'

	# 	# Clear face encodings from previous instance
	# 	print("Clearing face encodings...")
	# 	known_face_encodings.clear()
	# 	known_face_metadata.clear()

	# 	# start video stream
	# 	if running_on_jetson_nano():
	# 		model = 'cnn'
	# 		video_capture = cv2.VideoCapture(gstreamer_pipeline(flip_method=2),cv2.CAP_GSTREAMER)
	# 	else:
	# 		video_capture= cv2.VideoCapture(0)

	# 	print("Using model:",model)

	# 	if video_capture.isOpened():
	# 		try:
	# 			window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
	# 			# Identify faces in photo for capture
	# 			face_locations = []
	# 			process_this_frame = True
	# 			print("Starting loop...")
	# 			while True:
	# 				# grab frame of video
	# 				ret, frame = video_capture.read()

	# 				# Resize frame of video to 1/2 size for faster face recognition processing
	# 				small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

	# 				# Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
	# 				rgb_small_frame = small_frame[:, :, ::-1]

	# 				if process_this_frame:
	# 					# Find all the faces and face encodings in the current frame of video
	# 					face_locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample=0, model=model)
	# 					face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

	# 					# label all faces in frame
	# 					face_names = []
	# 					index = 0
	# 					for face_location, face_encoding in zip(face_locations, face_encodings):

	# 						index += 1
	# 						face_names.append("Face " + str(index))

	# 				process_this_frame = not process_this_frame

	# 				# Display live capture preview
	# 				for (top, right, bottom, left), label in zip(face_locations, face_names):
	# 					# print("Found face!")
	# 					# Scale back up face locations since the frame we detected in was scaled to 1/4 size
	# 					top *= 2
	# 					right *= 2
	# 					bottom *= 2
	# 					left *= 2

	# 					# Draw a box around the face
	# 					cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

	# 					# Draw a label with a name below the face
	# 					cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
	# 					font = cv2.FONT_HERSHEY_DUPLEX
	# 					cv2.putText(frame, label, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

	# 				# Display the resulting image
	# 				if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
	# 					cv2.imshow(window_title, frame)
	# 				else:
	# 					# quit loop if window is forcibly closed
	# 				 	break

	# 				keyCode = cv2.waitKey(10) & 0xFF
	# 				# Hit 'space' on the keyboard to capture photos!
	# 				if keyCode == 32:
	# 					print("capturing photo...")
	# 					capture_faces(frame,face_locations,face_encodings,margin)
	# 					break

	# 				# Hit 'q' on the keyboard to quit!
	# 				if keyCode == ord('q'):
	# 					print("exiting loop...")
	# 					break

	# 			# save photos from capture
	# 		finally:
	# 			print("Closing capture_mode...")
	# 			video_capture.release()
	# 			cv2.destroyAllWindows()
	# 	else:
	# 		print("Error: Unable to open camera")


	# def live_video():

	# 	print("starting live_video")
	# 	window_title = "Live Video"
	# 	break_cond = False
	# 	model = 'hog'

	# 	# initialize camera stream
	# 	if running_on_jetson_nano():
	# 		model = 'cnn'
	# 		video_capture = cv2.VideoCapture(v4l_pipeline(),cv2.CAP_GSTREAMER)
	# 	else:
	# 		video_capture= cv2.VideoCapture(0)

	# 	print("Using model:",model)


	# 	if video_capture.isOpened():
	# 		try:
	# 			window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
	# 			# Identify faces in photo for capture
	# 			face_locations = []
	# 			process_this_frame = True
	# 			print("Starting loop...")
	# 			while True:
	# 				# grab frame of video
	# 				ret, frame = video_capture.read()

	# 				# Resize frame of video to 1/2 size for faster face recognition processing
	# 				small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

	# 				# Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
	# 				rgb_small_frame = small_frame[:, :, ::-1]

	# 				if process_this_frame:
	# 					# Find all the faces and face encodings in the current frame of video
	# 					face_locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample=0, model=model)
	# 					# face_locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample=0, model=model)
	# 					# face_locations = face_recognition.face_locations(rgb_small_frame)
	# 					face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)


	# 					# label all faces in frame
	# 					face_names = []
	# 					for face_location, face_encoding in zip(face_locations, face_encodings):

	# 						metadata = lookup_known_face(face_encoding)

	# 						if metadata is not None:
	# 							face_label = f"Face {int(metadata['face_index'])}"
	# 						else:
	# 							face_label = "Unknown"

	# 						face_names.append(face_label)

	# 				process_this_frame = not process_this_frame

	# 				# Display live capture preview
	# 				for (top, right, bottom, left), label in zip(face_locations, face_names):
	# 					# print("Found face!")
	# 					# Scale back up face locations since the frame we detected in was scaled to 1/4 size
	# 					top *= 2
	# 					right *= 2
	# 					bottom *= 2
	# 					left *= 2

	# 					# Draw a box around the face
	# 					cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

	# 					# Draw a label with a name below the face
	# 					cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
	# 					font = cv2.FONT_HERSHEY_DUPLEX
	# 					cv2.putText(frame, label, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

	# 				# Display the resulting image
	# 				if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
	# 					cv2.imshow(window_title, frame)
	# 				else:
	# 					# quit loop if window is forcibly closed
	# 					break_cond = True
	# 					break

	# 				keyCode = cv2.waitKey(10) & 0xFF
	# 				# Hit 'space' on the keyboard to switch to capture mode!
	# 				if keyCode == 32:
	# 					print("switching to capture mode...")
	# 					# capture_faces(frame,face_locations,face_encodings,margin)
	# 					break

	# 				# Hit 'q' on the keyboard to quit!
	# 				if keyCode == ord('q'):
	# 					print("exiting loop...")
	# 					break_cond = True
	# 					break
	# 		finally:
	# 			print("Closing live_video...")
	# 			video_capture.release()
	# 			cv2.destroyAllWindows()
	# 	else:
	# 			print("Error: Unable to open camera")

	# 	return break_cond



def gstreamer_pipeline(
	sensor_id=0,
	capture_width=1920,
	capture_height=1080,
	display_width=640,
	display_height=360,
	framerate=60,
	flip_method=0,
):
	return (
	"nvarguscamerasrc sensor-id=%d !"
	"video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
	"nvvidconv flip-method=%d ! "
	"video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
	"videoconvert ! "
	"video/x-raw, format=(string)BGR ! appsink"
	% (
	sensor_id,
	capture_width,
	capture_height,
	framerate,
	flip_method,
	display_width,
	display_height,
	)
	)

def v4l_pipeline(
	camera_id=1,
	capture_width=640,
	capture_height=480,
	display_width=640,
	display_height=480,
	framerate=30,
):
	return (
		"v4l2src device=/dev/video%d ! "
		"video/x-raw, width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
		"videoconvert ! "
		"video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGR ! appsink"
		% (
            camera_id,
            capture_width,
            capture_height,
            framerate,
            display_width,
            display_height,
        )
	)