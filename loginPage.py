import tkinter as tk
from PIL import Image, ImageTk

class LoginPage(tk.Frame):

	def __init__(self, parent, App):
		self.app = App
		self.settings = App.settings

		super().__init__(parent)
		self.configure(bg="white")
		self.grid(row=0, column=0, sticky="nsew")
		parent.grid_rowconfigure(0, weight=1)
		parent.grid_columnconfigure(0, weight=1)

		self.mainFrame = tk.Frame(self, height=self.settings.height, width=self.settings.width, bg="white")
		self.mainFrame.pack(expand=True)

		image = Image.open(self.settings.logo_path)
		image_w, image_h = image.size
		ratio = image_w/self.settings.width


		image = image.resize((int(image_w//ratio//2), int(image_h//ratio//2)))
		self.logo = ImageTk.PhotoImage(image)
		self.label_logo = tk.Label(self.mainFrame, image=self.logo)
		self.label_logo.pack()

		self.label_username = tk.Label(self.mainFrame, text="Username", bg="white", fg="black", font=("Arial", 14, "bold"))
		self.label_username.pack()

		self.var_username = tk.StringVar()
		self.entry_username = tk.Entry(self.mainFrame, font=("Arial", 14, "bold"), textvariable=self.var_username)
		self.entry_username.pack()

		self.label_password = tk.Label(self.mainFrame, text="Password", bg="white", fg="black", font=("Arial", 14, "bold"))
		self.label_password.pack()

		self.var_password = tk.StringVar()
		self.entry_password = tk.Entry(self.mainFrame, font=("Arial", 14, "bold"), show="•", textvariable=self.var_password)
		self.entry_password.pack()

		self.login_btn = tk.Button(self.mainFrame, text="LOGIN", font=("Arial", 14, "bold"), command=lambda:self.auth_login())
		self.login_btn.pack(pady=5)

	def auth_login(self):
		username = self.app.window.pages['loginPage'].var_username.get()
		password = self.app.window.pages['loginPage'].var_password.get()

		granted = self.settings.login(username, password)
		if granted:
			self.app.window.change_page('appPage')