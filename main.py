import cv2
import time
import datetime
import numpy

def calculateFrameDifference(A, B):
	if A is None:
		return
		
	C = A-B
	C = C/255
	
	deviation = C.sum()/(C.size)
	
	#print(deviation)
	
	if deviation > 0.15:
		print("Movement detected", datetime.datetime.now().time())
			
	
video = cv2.VideoCapture("kamer.mp4")

lastFrame = None

framesPerSecond = 20
frameTime = 1/framesPerSecond

oldTime = time.time()


while(video.isOpened()):

	newTime = time.time()
	
	elapsedTime = newTime - oldTime
	
	if elapsedTime > frameTime:
		result, frame = video.read()
	
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		
		calculateFrameDifference(lastFrame, frame)
		lastFrame = frame
			
		cv2.imshow('frame', frame)
		
		oldTime = time.time()
			
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

video.release()
cv2.destroyAllWindows()
	

	
