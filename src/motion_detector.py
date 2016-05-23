# import the necessary packages
import argparse
import datetime
import imutils
import time
import cv2
from Queue import *

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
ap.add_argument("-s", "--still", help="path to still frame")
ap.add_argument("-i", "--initial", type=int, default=0, help="frame number for 1st file")
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	camera = cv2.VideoCapture(0)
	time.sleep(0.25)

# otherwise, we are reading from a video file
else:
    camera = cv2.VideoCapture(args["video"])
    length = int(camera.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(camera.get(cv2.CAP_PROP_FPS))
    print "there are " + str(length) + " frames at " + str(fps) + " fps"

# initialize the first frame in the video stream
if args.get("still", None) is None:
	firstFrame = None
else:
	firstFrame = cv2.imread(args["still"])
	firstFrame = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY)
	firstFrame = cv2.GaussianBlur(firstFrame, (21, 21), 0)

frameNum = 0
startAt = args["initial"]
rate = 4
frames = Queue()
# loop over the frames of the video
while True:
	# grab the current frame and initialize the occupied/unoccupied
	# text
	(grabbed, frame) = camera.read()
	#text = "Unoccupied"

	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if not grabbed:
		break

	# resize the frame, convert it to grayscale, and blur it
	#frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	# if the first frame is None, initialize it
	if firstFrame is None:
		firstFrame = gray
		continue

	# compute the absolute difference between the current frame and
	# first frame
	if (frameNum < rate):
		compFrame = firstFrame
	else:
		compFrame = frames.get()
	frameDelta = cv2.absdiff(compFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)
	(_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	cv2.imwrite("rate3/frame%05d.png" % (frameNum+startAt,), thresh)


	frameNum+=1
	if (frameNum % 500) == 0:
		print str(frameNum) + " done"
	frames.put(gray)
	# if the `q` key is pressed, break from the loop
	#if key == ord("q"):
		#break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
