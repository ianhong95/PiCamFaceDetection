import picamera
from picamera.array import PiRGBArray
from time import sleep
import cv2
from i2c_servo import i2cServo


def faceDetection():

	for frame in camera.capture_continuous(output, format="bgr", use_video_port=True):

		image = frame.array
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		faces = faceCascade.detectMultiScale(gray, 1.1, 4)

		for (x, y, w, h) in faces:
			image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)

		cv2.imshow("Image", image)

		if faces is not tuple():
			face_center = (x + w/2, y + h/2)
		else:
			face_center = vid_center

		if cv2.waitKey(1) & 0xFF == ord("q"):
			break

		output.truncate(0)

		print(face_center)

		return face_center


def main():
	fc = faceDetection()

	# Calculate positional differences between  center of video and position of face
	newPanAngle = abs(vid_center[0] - fc[0]) * x_multiplier
	newTiltAngle = abs(vid_center[1] - fc[1]) * y_multiplier

	# Face is directly to the right of the center
	if fc[0] - vid_center[0] > x_tol and abs(fc[1] - vid_center[1]) < y_tol:
		panServo.moveCW(newPanAngle)

	# Face is directly to the left of the center
	elif fc[0] - vid_center[0] < -x_tol and abs(fc[1] - vid_center[1]) < y_tol:
		panServo.moveCCW(newPanAngle)

	# Face is directly above the center
	elif  fc[1] - vid_center[1] < -y_tol and abs(fc[0] - vid_center[0]) < x_tol:
		tiltServo.moveCCW(newTiltAngle)

	# Face is directly below the center
	elif fc[1] - vid_center[1] > y_tol and abs(fc[0] - vid_center[0]) < x_tol:
		tiltServo.moveCW(newTiltAngle)

	# Face is at top left
	elif fc[0] - vid_center[0] < -x_tol and fc[1] - vid_center[1] < -y_tol:
		panServo.moveCCW(newPanAngle)
		tiltServo.moveCCW(newTiltAngle)

	# Face is at bottom left
	elif fc[0] - vid_center[0] < -x_tol and fc[1] - vid_center[1] > y_tol:
		panServo.moveCCW(newPanAngle)
		tiltServo.moveCW(newTiltAngle)

	# Face is at top right
	elif fc[0] - vid_center[0] > x_tol and fc[1] - vid_center[1] < -y_tol:
		panServo.moveCW(newPanAngle)
		tiltServo.moveCCW(newTiltAngle)

	# Face is at bottom right
	elif fc[0] - vid_center[0] > x_tol and fc[1] - vid_center[1] > y_tol:
		panServo.moveCW(newPanAngle)
		tiltServo.moveCW(newTiltAngle)

if __name__ == "__main__":

	x_tol = 5	# Tolerance for centering in the x-direction
	y_tol = 2	# Tolerance for centering in the y-direction

	x_multiplier = 0.3		# Multiplier to relate resolution to motor rotation (degrees of rotation per pixel)
	y_multiplier = 0.2		# Multiplier to relate resolution to motor rotation (degrees of rotation per pixel)

	# Initiate instance of PiCamera
	camera = picamera.PiCamera()

	# Define face detection model
	faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

	# Camera settings
	camera.resolution = (192, 128)
	camera.framerate = 15
	output = PiRGBArray(camera, size=camera.resolution)

	# Define center coordinates of video stream
	vid_center = (camera.resolution[0]/2, camera.resolution[1]/2)

	# Create instances of i2c servos
	tiltServo = i2cServo(2, defaultAngle=100, lowerLim=90, upperLim=140)
	panServo = i2cServo(0, defaultAngle=90, lowerLim=30, upperLim = 150)

	while(True):
		main()

cv2.destroyAllWindows()
