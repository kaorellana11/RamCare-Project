import customtkinter as ctk
import ramcare_backend as back
from ramcare_backend import Patient

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

#A frame that contains the information of many patients
class PatientTable(ctk.CTkScrollableFrame):
    #Master: a CTk Object where the PatientTable will be displayed
    #Title: Title of the table
    #Patients: An array of all patient objects that will be displayed in the table
    def __init__(self, master, patients):
        super().__init__(master)
        self.master = master
        self.grid_columnconfigure(0, weight=1)
        self.radio_var = ctk.StringVar(value="")

        #Constants below define the max string length of each respective label, except DOB since it has a constant length
        #Check length when editing values
        self.NAME_LENGTH = 24
        self.BLOOD_TYPE_LENGTH = 70
        self.EMAIL_LENGTH = 40
        self.medicines_LENGTH = 30
        self.rows = []
        self.populate_table(patients)

    def populate_table(self, patients):
        #destroy any rows containing previous objects
        for row in self.rows:
            row.destroy()
        self.rows = [] #clear rows array

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
            
            #Creates a string to be placed on the table in the medicines slot, then truncates it
            medicines_str = ""
            if len(patient.medicines) == 1:
                medicines_str = patient.medicines[0]
            else:
                for med in patient.medicines:
                    medicines_str += med + ", "
            medicines_str = truncate_label(medicines_str, self.medicines_LENGTH)

            medicines = ctk.CTkLabel(row_frame, text=medicines_str, corner_radius=20, anchor="w", width=300)
            medicines.grid(row=index, column=2, padx=(10, 0), pady=10, sticky="w")
            medicines.cget("font").configure(size=FONT_SIZE, family=FONT_FAMILY)

            dob = ctk.CTkLabel(row_frame, text=patient.dob, corner_radius=20, anchor="w")
            dob.grid(row=index, column=3, padx=(10, 0), pady=10, sticky="w")
            dob.cget("font").configure(size=FONT_SIZE, family=FONT_FAMILY)

            email_str = truncate_label(patient.email, self.EMAIL_LENGTH)
            email = ctk.CTkLabel(row_frame, text=email_str, corner_radius=20, anchor="w", width=360)
            email.grid(row=index, column=4, padx=10, pady=10, sticky="w")
            email.cget("font").configure(size=FONT_SIZE, family=FONT_FAMILY)

            self.rows.append(row_frame)

            index += 1

class TableScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid_columnconfigure((3, 4), weight=1)
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=1)
        self.page_num = 0
        
        patients = back.fetch_rows(0)
        #patients = [Patient(name, blood_type, meds, dob, email, number) for 
        #            name, blood_type, meds, dob, email, number in 
        #            [("John Doe", "AB+", ["None"], "01/01/2000", "john.doe@gmail.com", "123-456-7890"),
        #             ("Longname Johnson", "A+", ["Talimogene Laherparepvec"], "01/01/2000", "longname.johnson.2000@gmail.com", "123-456-7890")]]
        self.table = PatientTable(self, patients)
        self.table.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="nsew", columnspan=5)

        self.create_patient_button = ctk.CTkButton(self, text="Create Patient",command=self.create_patient)
        self.create_patient_button.grid(row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="nw")
        self.create_patient_button.cget("font").configure(family=FONT_FAMILY, size=FONT_SIZE)

        self.edit_patient_button = ctk.CTkButton(self, text="Edit Patient",command=self.edit_patient)
        self.edit_patient_button.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nw")
        self.edit_patient_button.cget("font").configure(family=FONT_FAMILY, size=FONT_SIZE)

        self.delete_patient_button = ctk.CTkButton(self, text="Delete Patient",command=self.delete_patient)
        self.delete_patient_button.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nw")
        self.delete_patient_button.cget("font").configure(family=FONT_FAMILY, size=FONT_SIZE)

        self.prev_page_button = ctk.CTkButton(self, text="Prev Page", command=self.prev_page)
        self.prev_page_button.grid(row=1, column=3, padx=(20, 0), pady=(20, 0), sticky="ne")

        self.next_page_button = ctk.CTkButton(self, text="Next Page", command=self.next_page)
        self.next_page_button.grid(row = 1, column = 4, padx=20, pady=(20, 0), sticky="ne")

    def create_patient(self):
        raise_screen(self.master.edit_screen)
        self.master.edit_screen.set_button_command("create")

    def edit_patient(self):
        raise_screen(self.master.edit_screen)
        self.master.edit_screen.set_button_command("edit")
    
    def delete_patient(self):
        pass

    def next_page(self):
        pass
    
    def prev_page(self):
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

        medicines_label = ctk.CTkLabel(self, text="Medications",anchor="w")
        medicines_label.grid(row=2, column=0, padx=(20, 0), pady=(20, 0), sticky="w")

        medicines_box = ctk.CTkTextbox(self, corner_radius=6, height=40)
        medicines_box.grid(row=2, column=1, padx=(10, 0), pady=(20, 0), sticky="nw")   
        self.input_boxes.append(medicines_box) 

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

        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.edit_patient)
        self.submit_button.grid(row=6, column=0, padx=(20, 0), pady=(20, 0), sticky="w")

    def set_button_command(self, command_name):
        if (command_name == "edit"):
            self.submit_button.configure(command=self.edit_patient)
        elif (command_name == "create"):
            self.submit_button.configure(command=self.create_patient)

    def edit_patient(self):
        patient_arr = []
        for box in self.input_boxes:
            patient_arr.append(box.get("0.0", "end-1c"))
            box.delete("0.0", "end-1c")
        raise_screen(self.master.table_screen)
        print(patient_arr)

    def create_patient(self):
        raise_screen(self.master.table_screen)   

#The root of all the screens in the app.  
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("light")
        self.title("RamCare")
        self.geometry("1280x720")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        back.create_table()
        
        self.table_screen = TableScreen(self)
        self.table_screen.grid(row=0, column=0, sticky="nsew")

        self.edit_screen = EditScreen(self)
        self.edit_screen.grid(row=0, column=0, sticky="nsew")
        
        self.table_screen.tkraise()

        self.protocol("WM_DELETE_WINDOW", self.closed)
    
    def closed(self):
        back.connection_obj.close()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()