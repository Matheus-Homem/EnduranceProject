class Height:
	_instance = None

	def __new__(cls):
		if cls._instance is None:
			cls._instance = super().__new__(cls)
			cls._instance._value = 800
		return cls._instance

	def reset(self):
		self._value = 800

	def subtract(self, value):
		self._value -= value

	def get(self):
		return self._value