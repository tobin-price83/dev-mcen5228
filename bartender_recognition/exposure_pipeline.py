### Return strings for calling camera pipelines

# Default: HQ Raspberry Pi Camera
def gstreamer_pipeline(
	sensor_id=0,
	capture_width=1920,
	capture_height=1080,
	display_width=640,
	display_height=360,
	framerate=60,
	frameskip=1,
	flip_method=0,
	exposure_compensation=0.0,
):
	return (
	"nvarguscamerasrc sensor-id=%d, exposurecompensation=%f !"
	"video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/%d ! "
	"nvvidconv flip-method=%d ! "
	"video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
	"videoconvert ! "
	"video/x-raw, format=(string)BGR ! appsink"
	% (
	sensor_id,
	exposure_compensation,
	capture_width,
	capture_height,
	framerate,
	frameskip,
	flip_method,
	display_width,
	display_height,
	)
	)

# Default: Logitech c390 Webcamera
def v4l_pipeline(
	camera_id=1,
	capture_width=640,
	capture_height=480,
	display_width=640,
	display_height=480,
	framerate=30,
	frameskip=1,
):
	return (
		"v4l2src device=/dev/video%d ! "
		"video/x-raw, width=(int)%d, height=(int)%d, framerate=(fraction)%d/%d ! "
		"videoconvert ! "
		"video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGR ! appsink"
		% (
            camera_id,
            capture_width,
            capture_height,
            framerate,
            frameskip,
            display_width,
            display_height,
        )
	)

