
from json import load, dump


class Settings:

	def __init__(self):


		self.title = "Apotek"



		base = 50
		ratio = (16, 9)
		self.width = base*ratio[0]
		self.height = base*ratio[1]
		self.screen = f"{self.width}x{self.height}+500+500"


		self.logo = 'img/download.jpg'
		
		self.logo_path = "img/download.jpg"
		

		self.obat = None
		self.load_data_from_json()

		self.users_path = "data/users.json"


	def load_data_from_json(self):
		with open("data/nama.json", "r") as file_json:
			self.obat = load(file_json)

	def save_data_to_json(self):
		with open("data/nama.json", "w") as file_json:
			dump(self.obat, file_json)

	def load_data(self, path):
		with open(path, "r") as json_data:
			data = load(json_data)
		return data


	def login(self, username, password):
		users = self.load_data(self.users_path)
		if username in users:
			if password == users[username]["password"]:
				return True
		else:
			return False