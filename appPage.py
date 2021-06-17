import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class AppPage(tk.Frame):

	def __init__(self, parent, App): #self.container, self.app

		self.app = App
		self.settings = App.settings
		self.current_contact = self.settings.obat[0]
		self.last_current_index = 0

		self.update_mode = False
		self.contacts_index = []

		super().__init__(parent) # window.container
		self.grid(row=0, column=0, sticky="nsew")

		parent.grid_rowconfigure(0, weight=1)
		parent.grid_columnconfigure(0, weight=1)

		self.create_left_frame()
		self.create_right_frame()
		self.config_left_and_right_frame()

		


	def create_left_frame(self):
		self.left_frame = tk.Frame(self, bg="white") # 1
		self.left_frame.grid(row=0, column=0, sticky="nsew")

		self.create_left_header()
		self.create_left_content()

	def create_right_frame(self):
		self.right_frame = tk.Frame(self, bg="white", width=2*self.settings.width//3) # 2
		self.right_frame.grid(row=0, column=1, sticky="nsew")

		self.create_right_header()
		self.create_right_content()
		self.create_right_footer()

	def config_left_and_right_frame(self):
		self.grid_columnconfigure(0, weight=1) # 1/3
		self.grid_columnconfigure(1, weight=2) # 2/3
		self.grid_rowconfigure(0, weight=1)

	def create_left_header(self):
		frame_w = self.settings.width//3
		frame_h = self.settings.height

		self.left_header = tk.Frame(self.left_frame, width=frame_w, height=frame_h//5, bg="white")
		self.left_header.pack()

		image = Image.open(self.settings.logo)
		i_w, i_h = image.size
		ratio = i_w/frame_w
		new_size = (int(i_w/ratio), int(i_h/ratio))
		image = image.resize(new_size)
		self.logo = ImageTk.PhotoImage(image)

		self.label_logo = tk.Label(self.left_header, image=self.logo)
		self.label_logo.pack()

		self.searchbox_frame = tk.Frame(self.left_frame, width=frame_w, height=frame_h//20, bg="white")
		self.searchbox_frame.pack(fill="x")

		self.entry_search_var = tk.StringVar()
		self.entry_search = tk.Entry(self.searchbox_frame, bg="white", font=("Arial", 12), textvariable=self.entry_search_var)
		self.entry_search.grid(row=0, column=0, sticky="nsew")

		self.button_search = tk.Button(self.searchbox_frame, bg="white", font=("Arial", 12), text="Find 🔍", command=self.clicked_search_btn)
		self.button_search.grid(row=0, column=1, sticky="nsew")

		self.searchbox_frame.grid_columnconfigure(0, weight=3) # 3/4
		self.searchbox_frame.grid_columnconfigure(1, weight=1) # 1/4


	def create_list_contacts_in_listbox(self):
		contacts = self.settings.obat

		for index in self.contacts_index:
			contact = self.settings.obat[index]
			for numberPhone, detailObat in contact.items():
				fullName = f"{detailObat['f_name']} {detailObat['l_name']}"
				self.contacts_listbox.insert("end", fullName)

	def create_list_full_contacts_in_listbox(self):
		self.contacts_listbox.delete(0, 'end')
		self.contacts_index = []
		counter_index = 0
		contacts = self.settings.obat
		for obat in contacts:
			self.contacts_index.append(counter_index)
			counter_index += 1 # counter_index = counter_index + 1 (update varible)

		self.create_list_contacts_in_listbox()


	def create_left_content(self):
		frame_w = self.settings.width//3
		frame_h = self.settings.height

		self.left_content = tk.Frame(self.left_frame, width=frame_w, height=4*frame_h//5, bg="white")
		self.left_content.pack(fill="x")

		self.contacts_listbox = tk.Listbox(self.left_content, bg="white", fg="black" , height=4*frame_h//5, font=("Arial", 12))
		self.contacts_listbox.pack(side="left", expand=True, fill="both")

		self.create_list_full_contacts_in_listbox()
		
		self.contacts_scroll = tk.Scrollbar(self.left_content)
		self.contacts_scroll.pack(side="right", fill="y")

		self.contacts_listbox.configure(yscrollcommand=self.contacts_scroll.set)
		self.contacts_scroll.configure(command=self.contacts_listbox.yview)

		self.contacts_listbox.bind("<<ListboxSelect>>", self.clicked_item_list_box)


	def clicked_item_list_box(self, event):
		if not self.update_mode:
			selection = event.widget.curselection()
			try:
				item_listbox_index = selection[0]
			except IndexError:
				item_listbox_index = self.last_current_index
			index = self.contacts_index[item_listbox_index]
			self.last_current_index = index
			self.current_contact = self.settings.obat[index]

			for numberPhone, info in self.current_contact.items():
				phone = numberPhone
				fullName = info['f_name']+" "+info['l_name']
				obat = info['obat']
				fungsi = info['fungsi']

			self.fullName_label.configure(text=fullName)
			self.table_info[0][1].configure(text=phone)
			self.table_info[1][1].configure(text=obat)
			self.table_info[2][1].configure(text=fungsi)
		

	def create_right_header(self):
		frame_w = 2*self.settings.width//3
		frame_h = self.settings.height//5

		self.right_header = tk.Frame(self.right_frame, width=frame_w, height=frame_h, bg="white")
		self.right_header.pack(expand=True)
		self.create_detail_right_header()

	def create_detail_right_header(self):
		frame_w = 2*self.settings.width//3
		frame_h = self.settings.height//5

		self.detail_header = tk.Frame(self.right_header, width=frame_w, height=frame_h, bg="white")
		self.detail_header.grid(row=0, column=0, sticky="nsew")

		data = list(self.current_contact.values())[0]
		fullName = f"{data['f_name']} {data['l_name']}"
		self.virt_fullName_image = tk.PhotoImage(width=1, height=1)
		self.fullName_label = tk.Label(self.detail_header, text=fullName, font=("Arial", 26), bg="white", image=self.virt_fullName_image, compound="c", width=frame_w, height=frame_h)
		self.fullName_label.pack()

		self.right_header.grid_columnconfigure(0, weight=1)
		self.right_header.grid_rowconfigure(0, weight=1)

	def create_right_content(self):
		frame_w = 2*self.settings.width//3
		frame_h = 3*(4*self.settings.height//5)//4

		self.right_content = tk.Frame(self.right_frame, width=frame_w, height=frame_h, bg="white")
		self.right_content.pack(expand=True)
		self.create_detail_right_content()

	def create_detail_right_content(self):
		frame_w = 2*self.settings.width//3
		frame_h = 3*(4*self.settings.height//5)//4

		self.detail_content = tk.Frame(self.right_content, width=frame_w, height=frame_h, bg="white")
		self.detail_content.grid(row=0, column=0, sticky="nsew")

		self.table_info = []
		for numberPhone, info in self.current_contact.items():
			info = [
				['Telepon Pembeli :', numberPhone],
				['Nama Obat :', info['obat']],
				['Fungsi :', info['fungsi']]
			]
		rows, columns = len(info), len(info[0])
		for row in range(rows):
			aRow = []
			for column in range(columns):
				label = tk.Label(self.detail_content, text=info[row][column], font=("Arial", 12), bg="white")
				if column == 0:
					sticky = 'e'
				else:
					sticky = 'w'
				label.grid(row=row, column=column, sticky=sticky)
				aRow.append(label)
			self.table_info.append(aRow)


		self.right_content.grid_columnconfigure(0, weight=1)
		self.right_content.grid_rowconfigure(0, weight=1)




	def create_right_footer(self):
		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4

		self.right_footer = tk.Frame(self.right_frame, width=frame_w, height=frame_h, bg="white")
		self.right_footer.pack(expand=True)
		self.create_detail_right_footer()

	def create_detail_right_footer(self):
		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4

		self.detail_footer = tk.Frame(self.right_footer, width=frame_w, height=frame_h, bg="white")
		self.detail_footer.grid(row=0, column=0, sticky="nsew")

		features = ['Update', 'Delete', 'Add New']
		self.buttons_features = []
		for feature in features:
			button = tk.Button(self.detail_footer, text=feature, bg="white", fg="black", font=("Arial", 12, "bold"), bd=0)
			button.grid(row=0, column=features.index(feature), sticky="nsew", padx=10, pady=20)
			self.buttons_features.append(button)
		self.buttons_features[0].configure(command=self.clicked_update_btn)
		self.buttons_features[1].configure(command=self.clicked_delete_btn)
		self.buttons_features[2].configure(command=self.clicked_add_new_btn)

		self.right_footer.grid_columnconfigure(0, weight=1)
		self.right_footer.grid_rowconfigure(0, weight=1)

	def recreate_right_frame(self):
		self.detail_header.destroy()
		self.detail_update_content.destroy()
		self.detail_update_footer.destroy()

		self.create_detail_right_header()
		self.create_detail_right_content()
		self.create_detail_right_footer()

	def clicked_update_btn(self):
		self.update_mode = True

		frame_w = 2*self.settings.width//3
		frame_h = 3*(4*self.settings.height//5)//4

		self.detail_content.destroy()
		self.detail_footer.destroy()

		self.detail_update_content = tk.Frame(self.right_content, width=frame_w, height=frame_h, bg="white")
		self.detail_update_content.grid(row=0, column=0, sticky="nsew")

		self.table_info = []
		for numberPhone, info in self.current_contact.items():
			info = [
				['First Name :', info['f_name']],
				['Last Name :', info['l_name']],
				['Telepon Pembeli :', numberPhone],
				['Nama Obat :', info['obat']],
				['Fungsi :', info['fungsi']]
			]
		self.entry_update_contact_vars = []
		rows, columns = len(info), len(info[0])
		for row in range(rows):
			aRow = []
			for column in range(columns):
				if column == 0:
					label = tk.Label(self.detail_update_content,text=info[row][column], font=("Arial", 12), bg="white")
					sticky = 'e'
					label.grid(row=row, column=column, sticky=sticky)
					aRow.append(label)
				else:
					entry_var = tk.StringVar()
					self.entry_update_contact_vars.append(entry_var)
					entry = tk.Entry(self.detail_update_content,font=("Arial", 12), bg="white", textvariable=self.entry_update_contact_vars[row])
					entry.insert(0, info[row][column])
					sticky = 'w'
					entry.grid(row=row, column=column, sticky=sticky)
					aRow.append(entry)
			self.table_info.append(aRow)


		self.right_content.grid_columnconfigure(0, weight=1)
		self.right_content.grid_rowconfigure(0, weight=1)

		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4

		self.detail_update_footer = tk.Frame(self.right_footer, width=frame_w, height=frame_h, bg="white")
		self.detail_update_footer.grid(row=0, column=0, sticky="nsew")

		features = ['Save', 'Cancel']
		commands = [self.clicked_save_contact_btn, self.clicked_cancel_contact_btn]
		self.buttons_features = []
		for feature in features:
			button = tk.Button(self.detail_update_footer, text=feature, bg="white", fg="black", font=("Arial", 12, "bold"), bd=0, command=commands[features.index(feature)])
			button.grid(row=0, column=features.index(feature), sticky="nsew", padx=10, pady=20)
			self.buttons_features.append(button)
		

		self.right_footer.grid_columnconfigure(0, weight=1)
		self.right_footer.grid_rowconfigure(0, weight=1)

	def clicked_delete_btn(self):
		confirm = messagebox.askyesnocancel("Memproses data...", "Apakah kamu yakin menghapus data ini?")

		if confirm:
			index = self.settings.obat.index(self.current_contact)
			del self.settings.obat[index]
			self.settings.save_data_to_json()
			

		self.create_list_full_contacts_in_listbox()


	def clicked_add_new_btn(self):
		self.update_mode = True
		frame_w = 2*self.settings.width//3
		frame_h = 3*(4*self.settings.height//5)//4 

		self.detail_content.destroy()
		self.detail_footer.destroy()
	

		self.detail_update_content = tk.Frame(self.right_content, width=frame_w, height=frame_h)
		self.detail_update_content.grid(row=0, column=0, sticky="nsew")

		for phoneNumber, info in self.current_contact.items():
			info = [
				["First Name :", info['f_name']],
				["Last Name :", info["l_name"]],
				['Telepon Pembeli :', phoneNumber],
				['Nama Obat :', info['obat']],
				['Fungsi :', info['fungsi']]
			]
		self.table_info = []
		self.entry_update_obat_vars = []

		rows , columns = len(info), len(info[0])
		for row in range(rows):
			aRow = []
			for column in range(columns):
				if column == 0:
					self.label3 = tk.Label(self.detail_update_content, text=info[row][column], font=("Arial", 12))
					aRow.append(self.label3)
					sticky = "e"
					self.label3.grid(row=row, column=column, sticky=sticky)
				else:
					entryVar = tk.StringVar()
					self.entry2 = tk.Entry(self.detail_update_content, font = ("Arial", 12),  textvariable = entryVar)
					self.entry_update_obat_vars.append(entryVar)
					aRow.append(self.entry2)
					sticky = "w"
					self.entry2.grid(row = row, column = column, sticky = sticky)
					
			self.table_info.append(aRow)

		self.right_content.grid_columnconfigure(0, weight=1)
		self.right_content.grid_rowconfigure(0, weight=1)


		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4 

		self.detail_update_footer = tk.Frame(self.right_footer, width=frame_w, height=frame_h)
		self.detail_update_footer.grid(row=0, column=0, sticky="nsew")

		features = ["Save", "Cancel"]
		commands = [self.save_add_new, self.clicked_cancel_contact_btn]

		self.buttons_features = []

		for feature in features:
			index = features.index(feature)
			self.button3 = tk.Button(self.detail_update_footer, text=feature, font=("Arial", 12, "bold"), bd=0, command = commands[index])
			self.button3.grid(row=0, column=features.index(feature), sticky="nsew", padx=20, pady=(0, 10))
			self.buttons_features.append(self.button3)

		self.right_footer.grid_columnconfigure(0, weight=1)
		self.right_footer.grid_rowconfigure(0, weight=1)

	def save_add_new(self):
		self.update_mode = False

		confirm = messagebox.askyesnocancel("Memproses data...", "Apa kamu yakin ingin menyimpan data ini?")

		if confirm:

			data = {
					self.entry_update_obat_vars[2].get() : {
						"f_name" : self.entry_update_obat_vars[0].get(),
						"l_name" : self.entry_update_obat_vars[1].get(),
						"obat" : self.entry_update_obat_vars[3].get(),
						"fungsi" : self.entry_update_obat_vars[4].get()
					}
				}

			self.settings.obat.append(data)
			self.settings.save_data_to_json()
			self.current_contact = self.settings.obat[self.last_current_index]

			self.recreate_right_frame()
			self.contacts_listbox.delete(0, 'end')
			self.create_list_full_contacts_in_listbox()


	def clicked_save_contact_btn(self):
		self.update_mode = False

		confirm = messagebox.askyesnocancel("Memproses data...", "Apakah kamu yakin ingin menyimpan data ini?")

		if confirm:

			f_name = self.entry_update_contact_vars[0].get()
			l_name = self.entry_update_contact_vars[1].get()
			phone = self.entry_update_contact_vars[2].get()
			obat = self.entry_update_contact_vars[3].get()
			fungsi = self.entry_update_contact_vars[4].get()
			
			self.settings.obat[self.last_current_index] = {
				phone : {
					"f_name" : f_name,
					"l_name" : l_name,
					"obat" : obat,
					"fungsi" : fungsi
				}
			}
			self.settings.save_data_to_json()
			self.current_contact = self.settings.obat[self.last_current_index]
			
			self.recreate_right_frame()

			self.contacts_listbox.delete(0, 'end')

			self.create_list_contacts_in_listbox()

	def clicked_cancel_contact_btn(self):
		self.update_mode = False

		self.recreate_right_frame()


	def clicked_search_btn(self):
		item_search = self.entry_search_var.get()
		if item_search :
			apotek = self.settings.obat
			self.contacts_index = []
			counter_index = 0
			for obat in apotek:
				for numberPhone, info in obat.items():
					if item_search in numberPhone:
						self.contacts_index.append(counter_index)
					elif item_search in info['f_name']:
						self.contacts_index.append(counter_index)
					elif item_search in info['l_name']:
						self.contacts_index.append(counter_index)
					# for info_key, info_val in info.items():
					# 	if item_search in info_val:
					# 		self.contacts_index.append(counter_index)
				
				counter_index += 1

			self.contacts_listbox.delete(0, 'end')
			self.create_list_contacts_in_listbox()
		else:
			self.create_list_full_contacts_in_listbox()
















