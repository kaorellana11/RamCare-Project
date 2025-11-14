import customtkinter as ctk
import login_backend as back

FONT_SIZE = 20
FONT_FAMILY = "Lucida Console"

def setFont(element, size=FONT_SIZE, family=FONT_FAMILY):
    element.cget("font").configure(size=size, family=family)

class LoggedInScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.master = master

        top_label = ctk.CTkLabel(self, text= "Logged In", fg_color="transparent", bg_color="#3b8ed0")
        top_label.grid(row = 0, column = 0, sticky="ew")
        setFont(top_label)

        border = ctk.CTkFrame(self, height=2, fg_color="black")
        border.grid(row=1, column=0, sticky="ew")
        
        self.info_label = ctk.CTkLabel(self, text="test", fg_color="transparent")
        self.info_label.grid(row=2, column=0, pady=(75, 0))
        setFont(self.info_label)

        self.log_out_button = ctk.CTkButton(self, text="Log Out", border_width=2, border_color="black", command=self.log_out)
        self.log_out_button.grid(row=3, column=0, pady=(75, 0))
        setFont(self.log_out_button)
    
    def log_out(self):
        if self.master.log_in_screen.remember_check.get() == 1:
            self.master.log_in_screen.remember_check.deselect()
            back.set_remember_false()
        self.master.log_in_screen.tkraise()

class LogInScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.master = master
        self.input_boxes = []

        top_label = ctk.CTkLabel(self, text= "Log In", fg_color="transparent", bg_color="#3b8ed0")
        top_label.grid(row = 0, column = 0, sticky="ew")
        setFont(top_label)

        border = ctk.CTkFrame(self, height=2, fg_color="black")
        border.grid(row=1, column=0, sticky="ew")

        username_label = ctk.CTkLabel(self, text="Username")
        username_label.grid(row=2, column=0, pady=(75, 0))
        setFont(username_label)

        username_input = ctk.CTkTextbox(self, height=35, border_color="black", border_width=2)
        username_input.grid(row=3, column=0)
        self.input_boxes.append(username_input)

        password_label = ctk.CTkLabel(self, text="Password")
        password_label.grid(row=4, column=0, pady=(100, 0))
        setFont(password_label)

        password_input = ctk.CTkTextbox(self, height=35, border_color="black", border_width=2)
        password_input.grid(row=5, column=0)
        self.input_boxes.append(password_input)

        forgot_password_button = ctk.CTkButton(self, text="Forgot Password?", text_color="blue", fg_color="transparent",hover=False, command=self.forgot_password)
        forgot_password_button.grid(row=6, column=0, pady=(10, 0))
        setFont(forgot_password_button, size=14)

        self.remember_check = ctk.CTkCheckBox(self ,text="Remember Me")
        self.remember_check.grid(row=7, column=0, pady=(10, 0))
        setFont(self.remember_check, size=14)

        self.log_in_button = ctk.CTkButton(self, text="Log In", border_width=2, border_color="black", corner_radius=10, command=self.log_in)
        self.log_in_button.grid(row=8, column=0, pady=(10, 0))
        setFont(self.log_in_button, size=14)

        self.wrong_password_label = ctk.CTkLabel(self, text="Incorrect Username or Password!", text_color="red")
        self.wrong_password_label.grid(row=9, column=0, pady=(10, 0))
        setFont(self.wrong_password_label)
        self.wrong_password_label.grid_remove()

    def forgot_password(self):
        pass

    def log_in(self):
        credentials = []
        for box in self.input_boxes:
            credentials.append(box.get("0.0", "end-1c"))
            
        if back.is_password(*credentials):
            self.wrong_password_label.grid_remove()
            self.master.security_screen.user_name = credentials[0]
            self.master.security_screen.tkraise()

            for box in self.input_boxes:
                box.delete("0.0", "end-1c")
        else:
            self.wrong_password_label.grid()

class SecurityQuestionScreen(ctk.CTkFrame):
    def __init__(self, master, questions):
        super().__init__(master)
        self.master = master
        self.grid_columnconfigure(0, weight=1)
        self.user_name = "" #to be filled by LogInScreen
        top_label = ctk.CTkLabel(self, text= "Log In", fg_color="transparent", bg_color="#3b8ed0")
        top_label.grid(row = 0, column = 0, sticky="ew")
        setFont(top_label)

        border = ctk.CTkFrame(self, height=2, fg_color="black")
        border.grid(row=1, column=0, sticky="ew", pady=(0, 75))

        cur_row = 2
        self.input_boxes = []
        for question in questions:
            question_label = ctk.CTkLabel(self, text=question)
            question_label.grid(row=cur_row, column=0)
            setFont(question_label)
            cur_row += 1
            question_box = ctk.CTkTextbox(self, height=35, width=400, border_color="black", border_width=2)
            question_box.grid(row=cur_row, column=0, pady=(0, 50))
            self.input_boxes.append(question_box)
            cur_row += 1
        self.log_in_button = ctk.CTkButton(self, text="Log In", border_width=2, border_color="black", corner_radius=10, command=self.log_in)
        self.log_in_button.grid(row=cur_row, column=0, pady=(10, 0))
        setFont(self.log_in_button, size=14)
        cur_row += 1

        self.wrong_password_label = ctk.CTkLabel(self, text="Incorrect Username or Password!", text_color="red")
        self.wrong_password_label.grid(row=cur_row, column=0, pady=(10, 0))
        setFont(self.wrong_password_label)
        self.wrong_password_label.grid_remove()

    def log_in(self):
        sec_params = [self.user_name]
        for box in self.input_boxes:
            sec_params.append(box.get("0.0", "end-1c"))
        if back.is_security(*sec_params):
            self.wrong_password_label.grid_remove()
            self.master.logged_in_screen.info_label.configure(text="Logged in as " + str(self.user_name) + ".")

            if self.master.log_in_screen.remember_check.get() == 1:
                back.set_remember_true(self.user_name)
            
            for box in self.input_boxes:
                box.delete("0.0", "end-1c")
                
            self.master.logged_in_screen.tkraise()
        else:
            self.wrong_password_label.grid()
    
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("light")
        self.title("RamCare")
        self.geometry("1280x720")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.logged_in_screen = LoggedInScreen(self)
        self.logged_in_screen.grid(row=0, column=0, sticky="nsew")

        self.security_screen = SecurityQuestionScreen(self, ["What city were you born in?", "What is your aunt's middle name?", "Where did you first attend school?"])
        self.security_screen.grid(row=0, column=0, sticky="nsew")
    
        self.log_in_screen = LogInScreen(self)
        self.log_in_screen.grid(row=0, column=0, sticky="nsew")

        self.protocol("WM_DELETE_WINDOW", self.closed)
        
        user_name = back.remember_me()
        if (user_name != False): 
            self.log_in_screen.remember_check.select()
            self.logged_in_screen.info_label.configure(text="Logged in as " + str(user_name) + ".")
            self.logged_in_screen.tkraise()

    def closed(self):
        back.connection_obj.close()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()