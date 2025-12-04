import customtkinter as ctk
import dosage_backend as back

FONT_SIZE = 20
FONT_FAMILY = "Lucida Console"
username = ""

def setFont(element, size=FONT_SIZE, family=FONT_FAMILY):
    element.cget("font").configure(size=size, family=family)

class UserFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid_columnconfigure(0, weight=1)
        self.configure(border_width=2, border_color="black")

        self.username_label = ctk.CTkLabel(self, text="Username:\n")
        self.username_label.grid(row=0, column=0, pady=(20, 0))
        setFont(self.username_label)

        self.name_label = ctk.CTkLabel(self, text="Name:\nREPLACEME")
        self.name_label.grid(row=1, column=0, pady=(20, 0))
        setFont(self.name_label)

        self.provider_label = ctk.CTkLabel(self, text="Provider:\nRamCare Health")
        self.provider_label.grid(row=2, column=0, pady=(20, 0))
        setFont(self.provider_label)

class InfoBox(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid_columnconfigure(0, weight=1)
        self.configure(border_width=2, border_color="black")

        self.meds_label = ctk.CTkLabel(self)
        self.meds_label.grid(row=0, column=0, pady=(20, 0))
        setFont(self.meds_label)

class TestUserLogInScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.grid_columnconfigure(0, weight=1)

        label = ctk.CTkLabel(self, text="Test User Log In")
        setFont(label)
        label.grid(row=0, column=0)

        john = ctk.CTkButton(self, text="John Doe", border_width=2,command=self.john_login)
        setFont(john)
        john.grid(row=1, column=0, pady=(300, 20))

        jane = ctk.CTkButton(self, text="Jane Doe", border_width=2, command=self.jane_login)
        setFont(jane)
        jane.grid(row=2, column=0)

    def dashboard_raise(self):
        self.master.dashboard.user_frame.username_label.configure(text="Username:\n" + username)
        self.master.dashboard.user_frame.name_label.configure(text="Name:\n" + back.get_name(username))
        self.master.dashboard.user_frame.provider_label.configure(text="Provider:\n" + back.get_provider(username))

        dose_str = "Doses Due:\n"
        if (back.get_dosage(username)):
            dose_str += "None"
            self.master.dashboard.confirm_dosage_button.configure(state="disabled")
            self.master.dashboard.missed_dosage_button.configure(state="disabled")
        else:
            dose_str += '\n'.join(back.get_medications(username))
        self.master.dashboard.info_box.meds_label.configure(text=dose_str)
        self.master.dashboard.tkraise()

    def john_login(self):
        global username 
        username = "testuser1"
        self.dashboard_raise()
    def jane_login(self):
        global username
        username = "testuser2"
        self.dashboard_raise()
    
class DosageConfirmPopup(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__()
        self.title("Dosage Confirmation")
        self.geometry("400x300")
        self.grid_columnconfigure(0, weight=1)
        self.master = master

        label = ctk.CTkLabel(self, text="Dosage Confirmed")
        label.grid(row=0, column=0, pady=30)
        setFont(label)

        button = ctk.CTkButton(self, text="Okay", border_width=2, command=self.closed)
        button.grid(row=1, column=0)
        setFont(button)

        self.protocol("WM_DELETE_WINDOW", self.closed)

    def closed(self):
        back.confirm_dosage(username)
        self.master.missed_dosage_button.configure(state="disabled")
        self.master.confirm_dosage_button.configure(state="disabled")
        self.master.info_box.meds_label.configure(text="Doses Due:\nNone")
        self.destroy()

class DosageMissedPopup(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__()
        self.title("Missed Dose Confirmed")
        self.geometry("400x300")
        self.grid_columnconfigure(0, weight=1)
        self.master = master

        label = ctk.CTkLabel(self, text=("Your provider has \nbeen notified of \nyour missed dose."))
        label.grid(row=0, column=0, pady=30)
        setFont(label)
        button = ctk.CTkButton(self, text="Okay", border_width=2, command=self.closed)
        button.grid(row=1, column=0)
        setFont(button)

        self.protocol("WM_DELETE_WINDOW", self.closed)

    def closed(self):
        self.master.master.dashboard.missed_dosage_button.configure(state="disabled")
        self.master.master.dashboard.confirm_dosage_button.configure(state="disabled")
        self.master.master.dashboard.info_box.meds_label.configure(text="Doses Due:\nNone")
        self.destroy()
        

class MissedDoseScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid_columnconfigure((0, 1), weight=1)
        self.checkboxes = []
        self.back_button = None
        self.confirm_button = None
        
    def populate_checkboxes(self):
        medication_list = back.get_medications(username)
        cur_row = 0

        label = ctk.CTkLabel(self, text="Select which medications were missed.")
        label.grid(row=cur_row, column=0, columnspan=2, pady=(20, 100))
        setFont(label)

        cur_row += 1
        for medication in medication_list:
            self.checkboxes.append(ctk.CTkCheckBox(self, text=medication))
            self.checkboxes[-1].grid(row=cur_row, column=0, columnspan=2, pady=(20, 0))
            setFont(self.checkboxes[-1])
            cur_row += 1 

        self.back_button = ctk.CTkButton(self, text="Back", border_width=2, command=self.back)
        setFont(self.back_button)
        self.back_button.grid(row=cur_row, column=0, sticky="e", padx=(0, 10), pady=(40, 0))

        self.confirm_button = ctk.CTkButton(self, text="Confirm", border_width=2, command=self.confirm)
        setFont(self.confirm_button)
        self.confirm_button.grid(row=cur_row, column=1, sticky="w", padx=(10, 0), pady=(40, 0))

        self.confirm_window = None

    def back(self):
        self.master.dashboard.tkraise()
        for box in self.checkboxes:
            box.destroy()
        self.back_button.destroy()
        self.confirm_button.destroy()

    def confirm(self):
        missed_meds = []
        for box in self.checkboxes:
            if box.get() == 1:
                missed_meds.append(box.cget("text"))
        if len(missed_meds) > 0:
            self.back()
            if self.confirm_window is None or not self.confirm_window.winfo_exists():
                self.confirm_window = DosageMissedPopup(self)
        self.after(200, self.confirm_window.focus())


class DashboardScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.grid_columnconfigure((0, 1), weight=2)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.confirm_dosage_button = ctk.CTkButton(self, text="Confirm All Doses As Taken", border_width=2, corner_radius=20, height=80, command=self.confirm_dose)
        self.confirm_dosage_button.grid(row=0, column=0, sticky="ew", pady=(20, 0), padx=(20, 0))
        setFont(self.confirm_dosage_button)

        self.missed_dosage_button = ctk.CTkButton(self, text="Missed A Dose", border_width=2, corner_radius=20, height=80, command=self.missed_dose)
        self.missed_dosage_button.grid(row=1, column=0, sticky="ew", pady=(20, 0), padx=(20, 0))
        setFont(self.missed_dosage_button)

        self.info_box = InfoBox(self)
        self.info_box.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=(20, 0), pady=20)

        self.user_frame = UserFrame(self)
        self.user_frame.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=20, pady=20)

        self.confirm_window = None

    def confirm_dose(self):
        if self.confirm_window is None or not self.confirm_window.winfo_exists():
            self.confirm_window = DosageConfirmPopup(self)
        self.after(200, self.confirm_window.focus())
    def missed_dose(self):
        self.master.missed_dose.populate_checkboxes()
        self.master.missed_dose.tkraise()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("light")
        self.title("RamCare")
        self.geometry("1280x720")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.missed_dose = MissedDoseScreen(self)
        self.missed_dose.grid(row=0, column=0, sticky="nsew")

        self.dashboard = DashboardScreen(self)
        self.dashboard.grid(row=0, column=0, sticky="nsew")

        self.test_user_login = TestUserLogInScreen(self)
        self.test_user_login.grid(row=0, column=0, sticky="nsew")

        self.protocol("WM_DELETE_WINDOW", self.closed)

    def closed(self):
        back.connection_obj.close()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()