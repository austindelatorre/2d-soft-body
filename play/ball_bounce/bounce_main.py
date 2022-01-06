from vector_2d import Vector as vec 
import numpy as np
import cv2 as cv

Y_MAX = 10
Y_MIN = 0

X_MIN = 0
X_MAX = 10

Y_ACC = 10

TIME = 10

DT = 0.1


ball = (vec(5,5), vec(0,0))

class Ball:

	def __init__(self, pos = vec(), vel = vec()):
		self.pos = pos
		self.vel = vel

	def update(self, dt):
		print(TIME)



ball = Ball()
ball.update(10)





img = np.zeros((10, 10, 3), np.uint8)

# cv.circle(img, np.array(obj.xy), 100, (0,0,255), -1)

pi = cv.imwrite("results.jpeg", img)
