class Scaler():
	
	def __init__(self, current_screen_size):
		reference_size = (1080, 2214)
		
		self.factor_x = current_screen_size[0] / reference_size[0]
		self.factor_y = current_screen_size[1] / reference_size[1]
	
	def scaler(self, sx, sy, image_size):
		image_x, image_y = image_size
		
		image_size_x = image_x * min(self.factor_x, self.factor_y) * sx
		image_size_y = image_y * min(self.factor_y, self.factor_x) * sy
		
		return round(image_size_x), round(image_size_y)