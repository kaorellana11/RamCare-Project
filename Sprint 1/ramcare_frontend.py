import customtkinter as ctk

FONT_SIZE = 15
FONT_FAMILY = "Lucida Console"

#Truncates the string to a desired length, leaving an ellipsis at the end
def truncate_label(str, length):
    str = str
    if len(str) > length:
        return str[:length - 3] + "..."
    return str

def raise_screen(screen):
    screen.tkraise()

#Class that holds all the information relating to patients
    #Note that this may become deprecated once database is implemented
class Patient():
    #Name: A String with the patient's name
    #blood_type: A String with the patient's blood type
    #meds: A String Array containing all of the patient's medications
    #dob: A String containing the patients date of birth.
    #     Must be formatted as XX/XX/XXXX
    #email: A String Array containing the patient's email
    def __init__(self, name, blood_type, meds, dob, email):
        self.name = name
        self.blood_type = blood_type
        self.dob = dob
        self.email = email
        self.meds = meds

#A frame that contains the information of many patients
class PatientTable(ctk.CTkScrollableFrame):
    #Master: a CTk Object where the PatientTable will be displayed
    #Title: Title of the table
    #Patients: An array of all patient objects that will be displayed in the table
    def __init__(self, master, patients):
        super().__init__(master)
        
        self.grid_columnconfigure(0, weight=1)
        self.radio_var = ctk.StringVar(value="")

        #Constants below define the max string length of each respective label, except DOB since it has a constant length
        #Check length when editing values
        self.NAME_LENGTH = 24
        self.BLOOD_TYPE_LENGTH = 70
        self.EMAIL_LENGTH = 40
        self.MEDS_LENGTH = 30

        index = 0

        #loop creates separate rows for each patient
            #Note that the way that data is obtained for each patient will be different once database is implemented
            #Rafactoring will be necessary
        for patient in patients:
            
            #Creates a frame for the whole row
            row_frame = ctk.CTkFrame(self, border_width=2, border_color="black")
            row_frame.grid(row=index, column=0, columnspan=6, sticky="nsew", pady=(10, 0))
            row_frame.grid_columnconfigure((0, 2, 4), weight=2)
            row_frame.grid_columnconfigure((1, 3), weight=2)

            name_str = truncate_label(patient.name, self.NAME_LENGTH)
            radio_button = ctk.CTkRadioButton(row_frame, text=name_str, corner_radius=20, value=patient.name, variable=self.radio_var, width=240)
            radio_button.grid(row=index, column=0, padx=(10, 0), pady=10, sticky="w")
            radio_button.cget("font").configure(size=FONT_SIZE, family=FONT_FAMILY)

            blood_type = ctk.CTkLabel(row_frame, text=patient.blood_type, corner_radius=20, anchor="w", width=70)
            blood_type.grid(row=index, column=1, padx=(10, 0), pady=10, sticky="w")
            blood_type.cget("font").configure(size=FONT_SIZE, family=FONT_FAMILY)
            
            #Creates a string to be placed on the table in the meds slot, then truncates it
            meds_str = ""
            if len(patient.meds) == 1:
                meds_str = patient.meds[0]
            else:
                for med in patient.meds:
                    meds_str += med + ", "
            meds_str = truncate_label(meds_str, self.MEDS_LENGTH)

            meds = ctk.CTkLabel(row_frame, text=meds_str, corner_radius=20, anchor="w", width=300)
            meds.grid(row=index, column=2, padx=(10, 0), pady=10, sticky="w")
            meds.cget("font").configure(size=FONT_SIZE, family=FONT_FAMILY)

            dob = ctk.CTkLabel(row_frame, text=patient.dob, corner_radius=20, anchor="w")
            dob.grid(row=index, column=3, padx=(10, 0), pady=10, sticky="w")
            dob.cget("font").configure(size=FONT_SIZE, family=FONT_FAMILY)

            email_str = truncate_label(patient.email, self.EMAIL_LENGTH)
            email = ctk.CTkLabel(row_frame, text=email_str, corner_radius=20, anchor="w", width=360)
            email.grid(row=index, column=4, padx=10, pady=10, sticky="w")
            email.cget("font").configure(size=FONT_SIZE, family=FONT_FAMILY)

            index += 1

class TableScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=1)

        #creates an array of patients by iterating through tuples containing patient info
        #get rid of this once database is implemented
        patients = [Patient(name, blood_type, meds, dob, email) for 
                    name, blood_type, meds, dob, email in 
                    [("John Doe", "AB+", ["None"], "01/01/2000", "john.doe@gmail.com"),
                     ("Longname Johnson", "A+", ["Talimogene Laherparepvec"], "01/01/2000", "longname.johnson.2000@gmail.com")]]
        
        self.table = PatientTable(self, patients)
        self.table.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="nsew", columnspan=4)

        self.create_patient_button = ctk.CTkButton(self, text="Create Patient",command=self.create_patient)
        self.create_patient_button.grid(row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="nw")
        self.create_patient_button.cget("font").configure(family=FONT_FAMILY, size=FONT_SIZE)

        self.edit_patient_button = ctk.CTkButton(self, text="Edit Patient",command=self.edit_patient)
        self.edit_patient_button.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nw")
        self.edit_patient_button.cget("font").configure(family=FONT_FAMILY, size=FONT_SIZE)

        self.delete_patient_button = ctk.CTkButton(self, text="Delete Patient",command=self.delete_patient)
        self.delete_patient_button.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nw")
        self.delete_patient_button.cget("font").configure(family=FONT_FAMILY, size=FONT_SIZE)
    def create_patient(self):
        pass

    def edit_patient(self):
        raise_screen(self.master.edit_screen)
    
    def delete_patient(self):
        pass

class EditScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
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
        raise_screen(self.master.table_screen)
        return patient_arr


#The root of all the screens in the app.  
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("light")
        self.title("RamCare")
        self.geometry("1280x720")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.table_screen = TableScreen(self)
        self.table_screen.grid(row=0, column=0, sticky="nsew")

        self.edit_screen = EditScreen(self)
        self.edit_screen.grid(row=0, column=0, sticky="nsew")
        
        self.table_screen.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()
