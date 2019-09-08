import cv2
import time
import datetime
import numpy

#time data dictionary
data = {}

def detectMovement(A, B):
	if A is None:
		return
	
	C = abs(A-B)
	C = C/255
	
	deviation = C.sum()/(C.size)
	
	
	if deviation > 0.45:
		print(deviation)

		return True

def saveEntry(entry):
	if entry in data:
		data[entry] += 1
	else:
		data[entry] = 0
		
def rescale(frame):
	#get the webcam size
	height, width = frame.shape

	#prepare the crop
	scale = 5
	centerX,centerY=int(height/2),int(width/2)
	radiusX,radiusY= int(scale*height/100),int(scale*width/100)

	minX,maxX=centerX-radiusX,centerX+radiusX
	minY,maxY=centerY-radiusY,centerY+radiusY

	cropped = frame[minX:maxX, minY:maxY]
	resized_cropped = cv2.resize(cropped, (width, height)) 
	
	return resized_cropped
		
#video = cv2.VideoCapture("kamer.mp4")
video = cv2.VideoCapture(0)

length = video.get(cv2.CAP_PROP_FRAME_COUNT)
print(length)

lastFrame = None

framesPerSecond = 24.3
frameTime = 1/framesPerSecond

oldTime = time.time()

oldFrameTime = time.time()
newFrameTime = time.time()

frames = 0

while(video.isOpened()):

	newFrameTime = time.time()

	frameElapsedTime = newFrameTime - oldFrameTime
	if frameElapsedTime > 1:
		oldFrameTime = time.time()
		
		entry = datetime.datetime.now().strftime('%H:%M:%S')
		if not entry in data:
			data[entry] = 0			
		
		frames = 0
		
	newTime = time.time()
	

	
	elapsedTime = newTime - oldTime
	
	if elapsedTime > frameTime:
		result, frame = video.read()
		
		if result == 0:
			break
	
		
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		

		frame = rescale(frame)
		frame = cv2.GaussianBlur(frame,(0,0),cv2.BORDER_DEFAULT)

		
		movementDetected = detectMovement(lastFrame, frame)
		if movementDetected:
			current_time = datetime.datetime.now().strftime('%H:%M:%S')
			print("Movement detected", current_time)
			saveEntry(current_time)
		
		
		lastFrame = frame
			
		cv2.imshow('frame', frame)
		
		oldTime = time.time()
			
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
		
	frames += 1

file = open("output.txt","w+")

sorted_keys = sorted(data.keys())
for key in sorted_keys:
	file.write("%s;%s\n" % (key, data[key]))

file.close()
		
video.release()
cv2.destroyAllWindows()
	

	
