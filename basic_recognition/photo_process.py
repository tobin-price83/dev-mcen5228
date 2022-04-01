import argparse
import os
import numpy as np
import cv2
import face_recognition
from PIL import Image

# parser information
parser = argparse.ArgumentParser(description='Crop photos for effient face recognition training.')
parser.add_argument("-s","--source", help = "filepath of source photo", required = False)
parser.add_argument("-f","--folder", help = "directory of source photos", required = False)
parser.add_argument("-o","--output", help = "filepath of output folder", required = False, default = "./export")
parser.add_argument("-m","--margin", help = "additional margin of crop around detected face", required = False, default = 0)
parser.add_argument("-a","--append", help = "append a suffix to filename", required = False, default = "")


def process_photo(source_path,output_path,margin=0):
	print("Importing: %s" %(source_path))
	image = Image.open(source_path)
	# image = face_recognition.load_image_file(source_path)

	# Resize image to a smaller target
	(width, height) = image.size
	# image_newsize = (640,480)
	image_newsize = image.size
	(width_new, height_new) = image_newsize
	small_image = image.resize(image_newsize)

	# How much image was reduced by
	scale_width = width/width_new
	scale_height= height/height_new
	print("Scaling factors: %d, %d" %(scale_width,scale_height))

	# Convert to array for face_recognition
	small_RGB = np.asarray(small_image)
	
	# Detect face bounds
	print("Finding face bounds...")
	face_location = face_recognition.face_locations(small_RGB, number_of_times_to_upsample=0, model='cnn')
	# face_location = face_recognition.face_locations(small_RGB)
	(top, right, bottom, left) = face_location[0]

	# Scale bounding box for original image size
	top *= scale_height
	right *= scale_width
	bottom *= scale_height
	left *= scale_width

	# convert to exportable format and crop
	# print("Converting image...")
	# pil_image = Image.fromarray(image)
	crop_image = image.crop((left-margin, top-margin, right+margin, bottom+margin))

	# save cropped image
	print("Saving cropped image...")

	save_photo(crop_image,output_path)

	print("Successfully saved to %s" %(output_path))



def save_photo(image,output_path):
	output_dir = os.path.dirname(output_path)

	isExist = os.path.exists(output_dir)

	if not isExist:
		print("Output directory %s does not exist. Generating..." %(output_dir))
		os.makedirs(output_dir)
		print("Created %s" %(output_dir))

	image.save(output_path)


if __name__ == '__main__':

	args = parser.parse_args()

	suffix = str(args.append)

	# Process single photo
	if args.source:
		
		# Get file path info
		source_path = str(args.source)
		filename = os.path.basename(source_path)
		(base,ext) = os.path.splitext(filename)

		# Check if file exists
		isExist = os.path.exists(source_path)

		if isExist:
			# Process photo
			process_photo(source_path=source_path,output_path=(str(args.output) + "/" + base + suffix + ext),margin=int(args.margin))
		else:
			ValueError("Error: Source file does not exist!")

	# Loop through and process all photos in folder
	if args.folder:

		# Get directory path
		folder_path = str(args.folder)
		output_path = str(args.output)

		# Check if source folder exists
		isExist = os.path.exists(folder_path)

		if isExist:
			# List of all files in source folder
			files = (file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file)))
			
			# Loop all file paths
			for file in files:
				(base,ext) = os.path.splitext(file)
				process_photo(source_path=(folder_path + "/" + file), output_path=(output_path + "/" + base + suffix + ext),margin=int(args.margin))
		else:
			ValueError("Error: Source directory does not exist!")