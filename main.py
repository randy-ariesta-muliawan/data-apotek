import sys
import tkinter as tk
from tkinter import messagebox

from settings import Settings
from appPage import AppPage
from loginPage import LoginPage

class Window(tk.Tk):

	def __init__(self, App):
		self.app = App
		self.settings = App.settings

		super().__init__()
		self.title(self.settings.title)
		self.geometry(self.settings.screen)
		self.resizable(0,0)

		self.create_menu()
		self.create_container()

		self.pages = {}
		self.create_appPage()
		self.create_loginPage()


	def create_container(self):
		self.container = tk.Frame(self)
		self.container.pack(fill="both", expand=True)

	def create_appPage(self):
		self.pages["appPage"] = AppPage(self.container, self.app)


	def create_menu(self):
		self.menu_bar = tk.Menu(self)
		self.configure(menu=self.menu_bar)

		self.file_menu = tk.Menu(self.menu_bar, tearoff=False)
		self.file_menu.add_command(label="New Contact", command = self.add_new)
		self.file_menu.add_command(label="Exit", command=self.exit)

		self.help_menu = tk.Menu(self.menu_bar, tearoff=False)
		self.help_menu.add_command(label="About")

		self.menu_bar.add_cascade(label='File', menu=self.file_menu)
		self.menu_bar.add_cascade(label='Help', menu=self.help_menu)

	def add_new(self):
		self.pages['appPage'].clicked_add_new_btn()


	def exit(self):
		respond = messagebox.askyesno("Keluar...", "Apa kamu yakin ingin menutup program ini?")
		if respond:
			sys.exit()


	def create_container(self):
		self.container = tk.Frame(self)
		self.container.pack(fill="both", expand=True)

	def create_appPage(self):
		self.pages["appPage"] = AppPage(self.container, self.app)

	def create_loginPage(self):
		self.pages['loginPage'] = LoginPage(self.container, self.app)


	def change_page(self, page):
		page = self.pages[page]
		page.tkraise()

	


class ObatApp:

	def __init__(self):
		self.settings = Settings()
		self.window = Window(self)
		

	def run(self):
		self.window.mainloop()

if __name__ == '__main__':
	myObatApp = ObatApp()
	myObatApp.run()