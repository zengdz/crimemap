
class MockDBHelper:
	def connect(self, database="crimemap"):
		pass
	def get_all_inputs(self):
		return []
	def add_input(self, data):
		pass
	def clear_all(self):
		pass
	def add_record(self, category, date, latitude, longitude, description):
		pass
	def get_all_records(self):
		return [{ 'latitude': 23.1157,
			'longitude': 113.3009,
			'date': "2000-01-01",
			'category': "mugging",
			'description': "mock description" }]

	