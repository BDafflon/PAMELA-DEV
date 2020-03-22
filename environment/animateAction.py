from helper.vector2D import Vector2D


class AnimateAction:
	def __init__(self):
		self.body = None
		self.move = Vector2D(0.0,0.0)
		self.velocity = Vector2D(0.0,0.0)
		self.rotatoin = Vector2D(0.0,0.0)

	def __init__(self,b,m,r):
		self.body = b
		self.move=m
		self.rotatoin = r

	def toString(self):
		return "move :"+str(self.move.toString())