import cv2
import time
import datetime
import numpy

def detectMovement(A, B):
	if A is None:
		return
		
	C = A-B
	C = C/255
	
	deviation = C.sum()/(C.size)
	
	#print(deviation)
	
	if deviation > 0.15:
		return True
			
	
video = cv2.VideoCapture("kamer.mp4")

lastFrame = None

framesPerSecond = 20
frameTime = 1/framesPerSecond

oldTime = time.time()



lines = []

while(video.isOpened()):

	newTime = time.time()
	
	elapsedTime = newTime - oldTime
	
	if elapsedTime > frameTime:
		result, frame = video.read()
	
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		
		movementDetected = detectMovement(lastFrame, frame)
		if movementDetected:
			current_time = datetime.datetime.now().strftime('%H:%M:%S')
			print("Movement detected", current_time)
			lines.append(current_time)
		
		lastFrame = frame
		
		cv2.imshow('frame', frame)
		
		oldTime = time.time()
			
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

file = open("output.txt","w+")
for i in range(len(lines)):
	file.write("%s\n" % lines[i])
file.close()
		
video.release()
cv2.destroyAllWindows()
	

	
