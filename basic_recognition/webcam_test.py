import cv2

def v4l_pipeline(
	camera_id=1,
	capture_width=640,
	capture_height=480,
	display_width=640,
	display_height=480,
	framerate=30,
	# flip_method=0
):
	return (
		"v4l2src device=/dev/video%d ! "
		"video/x-raw, width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
		# "nvvidconv ! "
		# "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
		"videoconvert ! "
		"video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGR ! appsink"
		% (
            camera_id,
            capture_width,
            capture_height,
            framerate,
            # flip_method,
            display_width,
            display_height,
        )
	)

def show_camera():
    window_title = "v4l Camera"

    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    print(v4l_pipeline(camera_id=1))
    video_capture = cv2.VideoCapture(v4l_pipeline(camera_id=1), cv2.CAP_GSTREAMER)
    if video_capture.isOpened():
        try:
            window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
            while True:
                ret_val, frame = video_capture.read()
                # Check to see if the user closed the window
                # Under GTK+ (Jetson Default), WND_PROP_VISIBLE does not work correctly. Under Qt it does
                # GTK - Substitute WND_PROP_AUTOSIZE to detect if window has been closed by user
                if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
                    cv2.imshow(window_title, frame)
                else:
                    break 
                keyCode = cv2.waitKey(10) & 0xFF
                # Stop the program on the ESC key or 'q'
                if keyCode == 27 or keyCode == ord('q'):
                    break
        finally:
            video_capture.release()
            cv2.destroyAllWindows()
    else:
        print("Error: Unable to open camera")


if __name__ == "__main__":
    show_camera()