import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ctk.set_appearance_mode("light")
        self.title("RamCare Test")
        self.geometry("1280x720")
        
        self.input_boxes = []

        #labels
        name_label = ctk.CTkLabel(self, text="Name",anchor="w")
        name_label.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="w")

        name_box = ctk.CTkTextbox(self, corner_radius=6, height=40)
        name_box.grid(row=0, column=1, padx=(10, 0), pady=(20, 0), sticky="nw")
        self.input_boxes.append(name_box)

        blood_type_label = ctk.CTkLabel(self, text="Blood Type",anchor="w")
        blood_type_label.grid(row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="w")

        blood_type_box = ctk.CTkTextbox(self, corner_radius=6, height=40)
        blood_type_box.grid(row=1, column=1, padx=(10, 0), pady=(20, 0), sticky="nw")  
        self.input_boxes.append(blood_type_box)

        meds_label = ctk.CTkLabel(self, text="Medications",anchor="w")
        meds_label.grid(row=2, column=0, padx=(20, 0), pady=(20, 0), sticky="w")

        meds_box = ctk.CTkTextbox(self, corner_radius=6, height=40)
        meds_box.grid(row=2, column=1, padx=(10, 0), pady=(20, 0), sticky="nw")   
        self.input_boxes.append(meds_box) 

        dob_label = ctk.CTkLabel(self, text="Date of Birth",anchor="w")
        dob_label.grid(row=3, column=0, padx=(20, 0), pady=(20, 0), sticky="w")

        dob_box = ctk.CTkTextbox(self, corner_radius=6, height=40)
        dob_box.grid(row=3, column=1, padx=(10, 0), pady=(20, 0), sticky="nw")  
        self.input_boxes.append(dob_box)

        email_label = ctk.CTkLabel(self, text="Email",anchor="w")
        email_label.grid(row=4, column=0, padx=(20, 0), pady=(20, 0), sticky="w")

        email_box = ctk.CTkTextbox(self, corner_radius=6, height=40)
        email_box.grid(row=4, column=1, padx=(10, 0), pady=(20, 0), sticky="nw")
        self.input_boxes.append(email_box)

        phone_number_label = ctk.CTkLabel(self, text="Phone Number",anchor="w")
        phone_number_label.grid(row=5, column=0, padx=(20, 0), pady=(20, 0), sticky="w")

        phone_number_box = ctk.CTkTextbox(self, corner_radius=6, height=40)
        phone_number_box.grid(row=5, column=1, padx=(10, 0), pady=(20, 0), sticky="nw")
        self.input_boxes.append(phone_number_box)

        submit_button = ctk.CTkButton(self, text="Submit", command=self.button_callback)
        submit_button.grid(row=6, column=0, padx=(20, 0), pady=(20, 0), sticky="w")
        
    def button_callback(self):
        patient_arr = []
        for box in self.input_boxes:
            patient_arr.append(box.get("0.0", "end-1c"))
        return patient_arr
        

app = App()
app.mainloop()