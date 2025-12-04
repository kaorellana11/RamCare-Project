import customtkinter as ctk
import dosage_backend as back

FONT_SIZE = 20
FONT_FAMILY = "Lucida Console"

def setFont(element, size=FONT_SIZE, family=FONT_FAMILY):
    element.cget("font").configure(size=size, family=family)

class UserFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid_columnconfigure(0, weight=1)
        self.configure(border_width=2, border_color="black")

        username_label = ctk.CTkLabel(self, text="Username:\nREPLACEME")
        username_label.grid(row=0, column=0, pady=(20, 0))
        setFont(username_label)

        name_label = ctk.CTkLabel(self, text="Name:\nREPLACEME")
        name_label.grid(row=1, column=0, pady=(20, 0))
        setFont(name_label)

        provider_label = ctk.CTkLabel(self, text="Provider:\nRamCare Health")
        provider_label.grid(row=2, column=0, pady=(20, 0))
        setFont(provider_label)

class InfoBox(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid_columnconfigure(0, weight=1)
        self.configure(border_width=2, border_color="black")

        meds_label = ctk.CTkLabel(self, text="Dose Due Today:\nREPLACEME")
        meds_label.grid(row=0, column=0, pady=(20, 0))
        setFont(meds_label)

        issuer_label = ctk.CTkLabel(self, text="Issued By:\nRamCare Health")
        issuer_label.grid(row=1, column=0, pady=(20, 0))
        setFont(issuer_label)

        date_label = ctk.CTkLabel(self, text="Date:\nREPLACEME")
        date_label.grid(row=2, column=0, pady=(20, 0))
        setFont(date_label)

class DashboardScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.grid_columnconfigure((0, 1), weight=2)
        self.grid_columnconfigure(2, weight=1)
        self.rowconfigure((0, 1), weight=1)

        confirm_dosage_button = ctk.CTkButton(self, text="Confirm Dosage Taken", border_width=2, corner_radius=20, height=80, command=self.confirm_dose)
        confirm_dosage_button.grid(row=0, column=0, sticky="ew", pady=(20, 0), padx=(20, 0))
        setFont(confirm_dosage_button)

        missed_dosage_button = ctk.CTkButton(self, text="Missed A Dose", border_width=2, corner_radius=20, height=80, command=self.missed_dose)
        missed_dosage_button.grid(row=1, column=0, sticky="ew", pady=(20, 0), padx=(20, 0))
        setFont(missed_dosage_button)

        self.info_box = InfoBox(self)
        self.info_box.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=(20, 0), pady=20)

        user_frame = UserFrame(self)
        user_frame.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=20, pady=20)

    def fill_info_box(self):
        pass
    def confirm_dose(self):
        pass
    def missed_dose(self):
        pass
        
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("light")
        self.title("RamCare")
        self.geometry("1280x720")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.dashboard = DashboardScreen(self)
        self.dashboard.grid(row=0, column=0, sticky="nsew")

        self.protocol("WM_DELETE_WINDOW", self.closed)

    def closed(self):
        back.connection_obj.close()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()