import customtkinter as ctk

FONT_SIZE = 20
FONT_FAMILY = "Lucida Console"

def setFont(element, size=FONT_SIZE, family=FONT_FAMILY):
    element.cget("font").configure(size=size, family=family)

class LogInScreen(ctk.CTkFrame):
    #note: you need 8 rows total
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)

        top_label = ctk.CTkLabel(self, text= "Log In", fg_color="transparent", bg_color="#3b8ed0")
        top_label.grid(row = 0, column = 0, sticky="ew")
        setFont(top_label)

        border = ctk.CTkFrame(self, height=2, fg_color="black")
        border.grid(row=1, column=0, sticky="ew")

        username_label = ctk.CTkLabel(self, text="Username")
        username_label.grid(row=2, column=0, pady=(75, 0))
        setFont(username_label)

        self.username_input = ctk.CTkTextbox(self, height=35, border_color="black", border_width=2)
        self.username_input.grid(row=3, column=0)

        password_label = ctk.CTkLabel(self, text="Password")
        password_label.grid(row=4, column=0, pady=(100, 0))
        setFont(password_label)

        self.password_input = ctk.CTkTextbox(self, height=35, border_color="black", border_width=2)
        self.password_input.grid(row=5, column=0)

        forgot_password_button = ctk.CTkButton(self, text="Forgot Password?", text_color="blue", fg_color="transparent",hover=False, command=self.forgot_password)
        forgot_password_button.grid(row=6, column=0, pady=(10, 0))
        setFont(forgot_password_button, size=14)

        self.remember_check = ctk.CTkCheckBox(self ,text="Remember Me")
        self.remember_check.grid(row=7, column=0, pady=(10, 0))
        setFont(self.remember_check, size=14)

        self.log_in_button = ctk.CTkButton(self, text="Log In", border_width=2, border_color="black", corner_radius=10)
        self.log_in_button.grid(row=8, column=0, pady=(10, 0))
        setFont(self.log_in_button, size=14)

    def forgot_password(self):
        pass

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("light")
        self.title("RamCare")
        self.geometry("1280x720")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.log_in_screen = LogInScreen(self)
        self.log_in_screen.grid(row=0, column=0, sticky="nsew")

        self.protocol("WM_DELETE_WINDOW", self.closed)
        
    def closed(self):
        #back.connection_obj.close()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()