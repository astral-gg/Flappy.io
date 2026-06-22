class Scaler():
	
	def __init__(self, current_screen_size):
		reference_size = (1080, 2214)
		
		self.factor_x = max(1, current_screen_size[0] / reference_size[0])
		self.factor_y = max(1, current_screen_size[1] / reference_size[1])
	
	def scaler(self, sx, sy, image_size):
		image_x, image_y = image_size
		
		image_size_x = image_x * self.factor_x * sx
		image_size_y = image_y * self.factor_y * sy
		
		return round(image_size_x), round(image_size_y)