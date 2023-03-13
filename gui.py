from tkinter import *
from selenium import webdriver
from pages import LoginWeb,HomePage
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import openai

frame_styles = {"relief": "groove","bd": 6, "font": ("Arial", 9, "bold")}
msg1 = ""

# Publishes a post on Facebook by software that does everything by itself automatically
def post(email,password):
    option = Options()
    option.add_argument('--disable-notifications')        
    openai.api_key="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"
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options= option)     
    user_email = email
    user_password = password
    login_page = LoginWeb(driver)
    driver.get("http://www.facebook.com")
    login_page.login(user_email,user_password)  
    home_page = HomePage(driver)
    home_page.home_page()
    home_page.post_message(msg1)
# Ai Generates messages by topic and line number
def Ai_msg(sub,line):
    global msg1
    openai.api_key="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"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f'Write me a post about {sub} {line} line long ',
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
    msg1 = response.choices[0].text
    OpenPostWindow() 
# login gui and logic
class LoginPage(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        main_frame = tk.Frame(self, bg="#708090", height=431, width=626)  # this is the background
        main_frame.pack(fill="both", expand="true")
    
        self.geometry("600x300")  # Sets window size to 626w x 431h pixels
        self.resizable(0, 0)  # This prevents any resizing of the screen

        title_styles = {"font": ("Trebuchet MS Bold", 16)}
        text_styles = {"font": ("Verdana", 14),
                       "foreground": "#E1FFFF"}

        frame_login = tk.Frame(main_frame, relief="groove", bd=2)  # this is the frame that holds all the login details and buttons
        frame_login.place(rely=0.30, relx=0.17, height=130, width=400)

        label_title = tk.Label(frame_login, title_styles, text="Login")
        label_title.grid(row=0, column=1, columnspan=1)

        label_user = tk.Label(frame_login, text_styles, text="Username:")
        label_user.grid(row=1, column=0)

        label_pw = tk.Label(frame_login, text_styles, text="Password:")
        label_pw.grid(row=2, column=0)

        entry_user = ttk.Entry(frame_login, width=25, cursor="xterm")
        entry_user.grid(row=1, column=1)

        entry_pw = ttk.Entry(frame_login, width=25, cursor="xterm", show="*")
        entry_pw.grid(row=2, column=1)

        button = ttk.Button(frame_login, text="Login", command=lambda: getlogin())
        button.place(rely=0.70, relx=0.50)

        signup_btn = ttk.Button(frame_login, text="Register", command=lambda: get_signup())
        signup_btn.place(rely=0.70, relx=0.75)

        def get_signup():
            SignupPage()

        def getlogin():
            username = entry_user.get()
            password = entry_pw.get()
            # if your want to run the script as it is set validation = True
            validation = validate(username, password)
            if validation:
                tk.messagebox.showinfo("Login Successful",
                                       f"Welcome {username},to the Ai post")
                root.deiconify()
                top.destroy()
            else:
                tk.messagebox.showerror("Information", "The Username or Password you have entered are incorrect ")

        def validate(username, password):
            # Checks the text file for a username/password combination.
            try:
                with open("credentials.txt", "r") as credentials:
                    for line in credentials:
                        line = line.split(",")
                        if line[1] == username and line[3] == password:
                            return True
                    return False
            except FileNotFoundError:
                return False
# signup gui and logic
class SignupPage(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
 
        main_frame = tk.Frame(self, bg="#708090", height=100, width=350)
        frame_Signup = tk.Frame(main_frame, relief="groove", bd=2)  # this is the frame that holds all the login details and buttons
        frame_Signup.place(rely=0.10, relx=0.10, height=100, width=300)
        # pack_propagate prevents the window resizing to match the widgets
        main_frame.pack_propagate(0)
        main_frame.pack(fill="both", expand="true")

        self.geometry("350x130")
        self.resizable(0, 0)

        self.title("Registration")

        text_styles = {"font": ("Verdana", 10)}

        label_user = tk.Label(frame_Signup, text_styles, text="New Username:")
        label_user.grid(row=1, column=0)

        label_pw = tk.Label(frame_Signup, text_styles, text="New Password:")
        label_pw.grid(row=2, column=0)

        entry_user = ttk.Entry(frame_Signup, width=20, cursor="xterm")
        entry_user.grid(row=1, column=1)

        entry_pw = ttk.Entry(frame_Signup, width=20, cursor="xterm", show="*")
        entry_pw.grid(row=2, column=1)

        button = ttk.Button(frame_Signup, text="Create Account", command=lambda: signup())
        button.grid(row=4, column=1)

        def signup():
            # Creates a text file with the Username and password
            user = entry_user.get()
            pw = entry_pw.get()
            validation = validate_user(user)
            if not validation:
                tk.messagebox.showerror("Information", "That Username already exists")
            else:
                if len(pw) > 3:
                    credentials = open("credentials.txt", "a")
                    credentials.write(f"Username,{user},Password,{pw},\n")
                    credentials.close()
                    tk.messagebox.showinfo("Information", "Your account details have been stored.")
                    SignupPage.destroy(self)

                else:
                    tk.messagebox.showerror("Information", "Your password needs to be longer than 3 values.")

        def validate_user(username):
            # Checks the text file for a username/password combination.
            try:
                with open("credentials.txt", "r") as credentials:
                    for line in credentials:
                        line = line.split(",")
                        if line[1] == username:
                            return False
                return True
            except FileNotFoundError:
                return True
# creates the full app
class MyApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        main_frame = tk.Frame(self, bg="#84CEEB", height=1000, width=600)
        main_frame.pack_propagate(0)
        main_frame.pack(fill="both", expand="true")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        self.resizable(0, 0) #prevents the app from being resized
        # self.geometry("1024x600") fixes the applications size
        self.frames = {}
        frame = Facebook_Post(main_frame, self)
        self.frames[Facebook_Post] = frame
        frame.grid(row=0, column=0, sticky="nsew")
# main gui
class GUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.main_frame = tk.Frame(self, bg="#BEB2A7", height=300, width=580)
        self.main_frame.pack_propagate(0)
        self.main_frame.pack(fill="both", expand="true")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)     
# open the post window 
class OpenPostWindow(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        main_frame = tk.Frame(self)
        main_frame.pack_propagate(0)
        main_frame.pack(fill="both", expand="true")
    
        self.title("Ai post ")
        self.geometry("800x500")
        self.resizable(0, 0)

        message_frame = ttk.LabelFrame(main_frame, text="Ai post ")
        message_frame.pack(expand=True, fill="both")
        
        post_button = ttk.Button(message_frame, text="post",command= lambda:post(email_input.get(),password_input.get()))
        post_button.place(x=400, y=450)
        
        message = tk.Text(message_frame, font=("Verdana", 14))
        message.insert(END,msg1)
        message.pack(side="top")
# all the facebook window gui
class Facebook_Post(GUI): 
    # inherits from the GUI class
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)
        global email_input ,password_input
       
        frame = tk.LabelFrame(self, frame_styles, text="log in to facebook")
        frame.place(rely=0.15, relx=0.07, height=200, width=500)
        
        # this is the frame that holds all the inputs and button 
        
        email=ttk.Label(frame,  text='email')
        email.place(x=10, y=20)
        password=ttk.Label(frame, text='password')
        password.place(x=10, y=50)
        post_sub=ttk.Label(frame, text='what to post about')
        post_sub.place(x=10, y=80)
        line_num=ttk.Label(frame, text='post number of lines')
        line_num.place(x=10, y=110)
  
        email_input =ttk.Entry(frame)
        email_input.place(x=150, y=20)
        password_input=ttk.Entry(frame)
        password_input.place(x=150, y=50)
        post_sub_input=ttk.Entry(frame)
        post_sub_input.place(x=150, y=80)
        line_num_input=ttk.Entry(frame)
        line_num_input.place(x=150, y=110)
        
        msg_text = ttk.Label(frame,text=msg1)
        msg_text.place(x=150,y=140)
        
        msg_button = ttk.Button(frame, text="sohw message",command=lambda:Ai_msg(post_sub_input.get(),line_num_input.get()))
        msg_button.place(x=350, y=150)
   
top = LoginPage()
top.title("Creating posts with Ai - Login Page")
root = MyApp()
root.withdraw()
root.title("Ai post - By liloz@")

root.mainloop()