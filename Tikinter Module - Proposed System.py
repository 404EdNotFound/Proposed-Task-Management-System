#Before running the program, please check that all these modules below have been installed before using the program
#All Modules are imported at the beginning of the program
import random, datetime, csv, sqlite3 #All These Modules are useful for randomising temporary variables and managing date and time, files such as CSV and performing SQL Algorihtms in Python when running specific queries
from tkinter import * #This global hotkey * is used to import all sub-modules
from tkinter import messagebox, ttk #These modules are imported explicitally due to the version of Python
from tkinter.filedialog import asksaveasfilename, askopenfilename #Used as a separate module in tkinter for saving to a certain directory
from tkcalendar import DateEntry #Used as a separate module that is used to create the calendar that is used for any date and time involved without any errors
from datetime import datetime #Used to manage date and time
from cryptography.fernet import Fernet #Used to import the fernet module that is used for Encrypting and Decrypting the file

#Creates the Class for Accounts stored in Employees
class employee:
    def __init__(self, firstname, surname): #Initialises the object with relevant attributes and parameters
        self.firstname = firstname
        self.surname = surname
        self.email = ""
        self.password = ""
        self.job = ""
        self.number = 0
        self.letter = ""
        self.ID = ""
        self.access = ""
        self.tempAccount = []
        self.permAccount = []
        self.validity = False
        self.accessValidity = False
        self.access_give = False
        self.employeeFile = "employee_account_details.csv"
        self.encryptedFile = "encrypted_employee_account_details.csv"
        self.sortedFiles = "sorted_employee_details.csv"
        self.key = Fernet.generate_key() #Generates a specific key that is used for the data to be encrypted and decrypted
    
    #Used to check the inputted values for when creating the account
    def account(self):
        #Attempts to retrieve the inputted values within the Exception Handling
        try:
            self.email = Create_emailAddress_Var.get()
            self.password = passwordCreate_Var.get()
        
        except (SyntaxError, ValueError, AttributeError): #Exception Error Raised
            messagebox.showerror("Error", "Email Details have been incorrectly utilised")
        
        else:
            #Validation checks used for the account page
            if "@csmegb.org" not in self.email:
                messagebox.showerror("Error!", "Invalid Email Address")
                self.validity = False
            
            elif self.password.isalnum() == False or self.password == "":
                messagebox.showerror("Error!", "Password needs to have letters and numbers")
                self.validity = False
            
            elif len(self.password) < 6 or len(self.password) > 20:
                messagebox.showerror("Error!", "Password is either too long or too short")
                self.validity = False
            
            else:
                self.validity = True
                #Moves to different methods after the confirmation of the account
                self.Identification()
                self.access_level()
    
    #Used to check the inputted values when signing back in to an existing account
    def retrieve_account(self):
        #Attempts to retrieve the inputted values within the Exception Handling
        try:
            self.email = Retrieve_emailAddress_Var.get()
            self.password = passwordRetrieve_Var.get()
        
        except (SyntaxError, ValueError, AttributeError): #Exception Error Raised
            messagebox.showerror("Error", "Email Details have been incorrectly utilised")
        
        else:
            #Validation checks used for the account page
            if "@csmegb.org" not in self.email:
                messagebox.showerror("Error!", "Invalid Email Address")
                self.validity = False
            
            elif self.password.isalnum() == False:
                messagebox.showerror("Error!", "Password needs to have letters and numbers")
                self.validity = False
            
            elif len(self.password) < 6 or len(self.password) > 20:
                messagebox.showerror("Error!", "Password is either too long or too short")
                self.validity = False
            
            else:
                self.validity = True
    
    #Creates the ID for any created accounts
    def Identification(self):
        self.letter = firstnameVar.get()
        self.number = str(random.randint(100, 999)) #Randomises the integer each time and then casting to a string
        self.letter = self.firstname[0:3] #Extracts the 1st 3 letters in terms of index
        self.ID = (self.letter + self.number).upper() #Concatenates both attributes and later capitalises the ID with the upper function by converting to uppercase (only works with string datatypes)
        messagebox.showinfo("ID Given!", "Your ID is" + " " + self.ID)
    
    #Provides access to the user based on the inputted job role
    def access_level(self):
        self.job = option.get()

        #Checks used for providing access levels
        if self.job in ["Employee", "Senior Manager", "Auditor"]:
            self.access = self.job
            messagebox.showinfo("Result!", "Your Access Level is" + " " + self.access)
            self.access_give = True
            self.accessValidity = True
        
        else:
            messagebox.showerror("Error!", "Invalid Job Role")
            self.access_give = False
            self.accessValidity = False

    #Stores all contents of attributes in an array
    def array(self):
        if self.ID != "" and self.firstname != "" and self.surname != "" and self.password != "" and self.access != "": #Used only if all attrbiutes aren't blank
            #All attributes are stored under a temporary array
            self.tempAccount.append(self.ID)
            self.tempAccount.append(self.firstname)
            self.tempAccount.append(self.surname)
            self.tempAccount.append(self.email)
            self.tempAccount.append(self.password)
            self.tempAccount.append(self.access)

            self.permAccount.append(self.tempAccount) #Then later stored in an permament array
            self.tempAccount = [] #Clears all contents in an temporary array so that it doesn't cause mass confusion with massive ammounts of data
            
            self.permAccount.sort(key = lambda x:x[0]) #Sorts the data with the sort function and through a lambda expression with a specific key
            print(self.permAccount)
    
    #A Method that is used to write the current contents that are inputted by the user into a chosen CSV file, this is used to separate each field with commas and views them as individual field
    def write_to_file(self):
        #Exception Handling used to open the file
        try:
            file = open(self.employeeFile, "a")
        
        except FileNotFoundError: #Exception Error Raised
            messagebox.showerror("Error!", "File Cannot Open")
        
        else:
            #Writes all contents into the file and seprates each field with a , as its a CSV
            file.write(self.ID + "," + self.firstname + "," + self.surname + "," + self.email + "," + self.password + ","  + self.access)
            file.write("\n") #New Line is written after the record has been added
            file.close()
    
    def encryptFile(self): #Example of Encryption to File through Symmeric Encryption, this uses a specific key that is being used through Fernet and a key file that is used to Encrypt this specific file
        with open("file.key", "wb") as file: #A key is used as a way to encrypt the data from the CSV file into an encrypted file
            file.write(self.key)

        with open("file.key", "rb") as file:
            self.key = file.read() #Used to retrieve the key used to encrypt the file
        
        fernet = Fernet(self.key) #Used to encrypt the file with this particular key

        with open(self.employeeFile, "rb") as file:
            original = file.read() #reads the original file
        
        encrypted = fernet.encrypt(original)

        with open(self.encryptedFile, "wb") as encrypted_file:
            encrypted_file.write(encrypted) #Writes all the encyrpted content within the file
    
    def read_from_file(self):
        #Exception Handling used to open the file
        try:
            file = open(self.employeeFile, "r")
        
        except FileNotFoundError: #Exception Error Raised
            messagebox.showerror("Error!", "File Cannot Open")
        
        else:
            csv.reader(file) #Used as a reader for the file
            file.close()
    
    def decryptFile(self): #Example of Decryption from File through Symmeric Encryption, this uses a specific key that is being used through Fernet and a key file that is used to decrypt this specific file
        fernet = Fernet(self.key)

        with open(self.encryptedFile, "rb") as file:
            encrypted = file.read()
        
        decrypted = fernet.decrypt(encrypted)

        with open(self.employeeFile, "wb") as file:
            file.write(decrypted)

    #Used as a method to sort the task details that are completely applicable to the user without fail
    def sort_fields(self):
        self.permAccount = [] #Uses an Empty Array that is defined for the fields to be sorted wherever possible

        with open(self.employeeFile, "r") as file: #Opens the file in readmode
            reader = csv.reader(file) #A reader is used within the CSV file to read each field
            for i in reader:
                self.permAccount.append(i) #Inserts all record details within an array
        
        self.permAccount.sort(key=lambda x:x[0]) #A Lambda Expression is used here to sort all the releevant fields wherever necessary

        with open(self.sortedFiles, "w", newline = "") as file:
            writer = csv.writer(file)
            writer.writerows(self.permAccount) #All rows are appended to the file based on the array
            print(self.permAccount)

#Creates the Class for any Task that the user creates themselves    
class Task:
    def __init__(self, employeeID, firstName, surname): #initialises the class with relevant attributes and parameters #employeeID, firstName, surname
        self.employeeID = employeeID
        self.firstName = firstName
        self.surname = surname
        self.taskName = ""
        self.taskID = ""
        self.startDate = ""
        self.endDate = ""
        self.start_date_obj = ""
        self.end_date_obj = ""
        self.priority = ""
        self.status = ""
        self.projectName = ""
        self.date_format = ""
        self.checkValidity = False
        self.tempArray = []
        self.taskArray = []
        self.taskFile = "taskDetails.csv"
        self.task_details = "task_details.csv"
        self.sortedFiles = "sortedTaskDetails.csv"
        self.encrypted_task_file = "encrypted_taskDetails.csv"
        self.key = Fernet.generate_key()
    
    #Creates the task
    def inputValues(self):
        self.taskName = taskName_Var.get()
        self.startDate = startDate_Var.get()
        self.endDate = endDate_Var.get()
        self.priority = priority_Var.get()
        self.status = status_Var.get()
        self.projectName = projectName_Var.get()

        if self.projectName == "":
            self.projectName = "None"

        self.date_format = "%d/%m/%Y"

    def taskCreation_checks(self):
        days_apart = 0 #Local Variable assigned to check the range between start and end dates

        #Error Exception Handling used for converting the inputted date into a date format
        try:
            self.start_date_obj = datetime.strptime(self.startDate, self.date_format)
            self.end_date_obj = datetime.strptime(self.endDate, self.date_format)
        
        except (ValueError, AttributeError): #Value Error when the process catches the input at this value
            messagebox.showerror("Error!", "Cannot Convert both the Start and End date perfectly")
            self.checkValidity = False
        
        else:
            messagebox.showinfo("Result!", "Converted Start and End Date perfectly")
            days_apart = self.end_date_obj - self.start_date_obj #Caluclates the range between the start and end date

            if days_apart.days < 0:
                messagebox.showerror("Error!", "Start Date is greater than End Date, Impossible!")
                self.checkValidity = False
            
            else:
                #Checking all inputs of the data through a process of checks
                if len(self.taskName) <= 3 and len(self.taskName) >= 1:
                    messagebox.showerror("Error!", "Invalid Task")
                    self.checkValidity = False
                
                elif self.projectName != "" and len(self.projectName) <= 3:
                    messagebox.showerror("Error!", "Invalid Project Name")
                    self.checkValidity = False
                
                elif self.startDate == "" and self.endDate == "":
                    messagebox.showerror("Error!", "Both Start and End Date Fields Must be filled")
                    self.checkValidity = False
                
                elif self.priority == "":
                    messagebox.showerror("Error!", "The Priority needs to be filled!")
                    self.checkValidity = False
                
                elif self.status == "":
                    messagebox.showerror("Error!", "The Status needs to be filled!")
                    self.checkValidity = False
                
                elif (self.startDate == "" and self.endDate != "") or (self.startDate != "" and self.endDate == ""):
                    messagebox.showerror("Error!", "One of these Start and End Date Fields must be filled")
                    self.checkValidity = False
                
                elif self.priority not in ["Critical", "High", "Medium", "Low"]:
                    messagebox.showerror("Error!", "Invalid Priority")
                    self.checkValidity = False
                
                elif self.status not in ["Completed", "Currently Working", "Incomplete"]:
                    messagebox.showerror("Error!", "Invalid Status")
                    self.checkValidity = False
                
                else:
                    messagebox.showinfo("Result!", "All These Fields are filled")
                    self.checkValidity = True
                    self.ID()

    #Creates the ID for the Task     
    def ID(self):
        self.number = str(random.randint(100, 999)) #Randomises the number each time and then casting to string
        self.letter = self.taskName[0:3] #Extracts the 1st 3 letters through indexing
        self.taskID = (self.letter + self.number).upper() #Concatenates the string

    #Stores all contents into in array
    def array(self):
        if self.taskID == "" and self.taskName == "" and self.startDate == "" and self.endDate == "" and self.priority == "" and self.status == "":
            pass

        else: #Starts with a temporary array
            self.tempArray.append(self.employeeID)
            self.tempArray.append(self.taskID)
            self.tempArray.append(self.taskName)
            self.tempArray.append(self.startDate)
            self.tempArray.append(self.endDate)
            self.tempArray.append(self.priority)
            self.tempArray.append(self.status)
            self.tempArray.append(self.projectName)

            self.taskArray.append(self.tempArray) #Then converted into a permanent array
            self.tempArray = []

            self.taskArray.sort(key = lambda x:x[0])
            print(self.taskArray)

    #A Method that is used to write the current contents that are inputted by the user into a chosen CSV file, this is used to separate each field with commas and views them as individual field
    def write_to_file(self):
        #Exception Handling is used here to make sure that the file can be opened perfectly without fail
        try:
            file = open(self.task_details, "a") #Opened in Append Mode
        
        #Catches the error when raising a particular error
        except (AttributeError, FileNotFoundError):
            messagebox.showerror("Error!", "File Cannot Open")
            quit()
        
        else:
            file.write(self.employeeID + "," + self.taskID + "," + self.taskName + "," + self.startDate + "," + self.endDate + "," + self.priority + "," + self.status + "," + self.projectName) #Separator is used here
            file.write("\n")
            file.close()
            #Writes all the details as commits to the CSV file without closing any specific details

    def encryptFile(self): #Example of Encryption to File through Symmeric Encryption, this uses a specific key that is being used through Fernet and a key file that is used to Encrypt this specific file
        with open("file.key", "wb") as file: #A key is used as a way to encrypt the data from the CSV file into an encrypted file
            file.write(self.key)

        with open("file.key", "rb") as file:
            self.key = file.read()
        
        fernet = Fernet(self.key)

        with open(self.task_details, "rb") as file:
            original = file.read()
        
        encrypted = fernet.encrypt(original)

        with open(self.encrypted_task_file, "wb") as encrypted_file:
            encrypted_file.write(encrypted)

    def read_from_file(self):
        try:
            file = open(self.task_details, "r")
        
        except FileNotFoundError:
            messagebox.showerror("Error!", "File Cannot Open")
        
        else:
            csv.reader(file)
            file.close()

    def decryptFile(self): #Example of Decryption from File through Symmeric Encryption, this uses a specific key that is being used through Fernet and a key file that is used to decrypt this specific file
        fernet = Fernet(self.key)

        with open(self.encrypted_task_file, "rb") as file:
            encrypted = file.read()
        
        decrypted = fernet.decrypt(encrypted)

        with open(self.task_details, "wb") as file:
            file.write(decrypted)

    #Used as a method to sort the task details that are completely applicable to the user without fail
    def sort_fields(self):
        self.taskArray = [] #Uses an Empty Array that is defined for the fields to be sorted wherever possible

        with open(self.task_details, "r") as file: #Opens the file in readmode
            reader = csv.reader(file) #A reader is used within the CSV file to read each field
            for i in reader:
                self.taskArray.append(i) #Inserts all record details within an array
        
        self.taskArray.sort(key=lambda x:x[0]) #A Lambda Expression is used here to sort all the releevant fields wherever necessary

        with open(self.sortedFiles, "w", newline = "") as file:
            writer = csv.writer(file)
            writer.writerows(self.taskArray) #All rows are appended to the file based on the array

#Used to create the auditor class for those in an auditor access level
class Auditor:
    def __init__(self, firstName, surname): #Initiates all attrbiutes and the class with parameters to pass through
        self.firstName = firstName
        self.surname = surname
        self.text = ""
        self.ID = ""
        self.tempArray = []
        self.permArray = []
        self.filepath = ""
        self.key = Fernet.generate_key()
        self.practice_encrypted_auditor_details = "encrypted_auditor_all_details.csv"
        self.check = False
    
    def get_variables(self):
        self.text = text.get("1.0", END) #Takes in the data from the text sub module
        self.ID = ID_Create
    
    def text_checks(self):
        if self.text != "":
            messagebox.showinfo("Result!", "Valid Information")
            self.check = True
            self.array()
        
        else:
            messagebox.showerror("Error!", "Please write something (Not the word 'something') within the text box.")
            self.check = False

    def open_file(self):
        self.filepath = askopenfilename(filetypes = [("CSV Files", "*.csv"), ("All Files", "*.*")]) #askopenfilename is a dialog from the tkinter.filedialog module which displays a file open dialog and stores the file path to the variable
        if not self.filepath: #Used to check if the button pressed isn't open meaning that the filepath doesn't contain any data and returns without executing any code
            return
        text.delete("1.0", END) #the text is deleted

        input_file = open(self.filepath, mode="r", encoding="utf-8") #UTF 8 is a standard encoding tool
        text_file = input_file.read() #Reads the textfile by opening the selected file
        text.insert(END, text_file) #Assigns string to csv,edit with insert which adds string
        input_file.close()

    def save_file(self):
        self.filepath = asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]) #asksaveasfilename is a dialog from the tkinter.filedialog module which displays a file open dialog and stores the file path to the variable for the user to save their file
        if not self.filepath:
            return
        
        with open(self.filepath, mode="w", encoding="utf-8") as output_file: #UTF 8 is a standard encoding tool
            text_file = text.get("1.0", END) #Receives the information within the textbox
            output_file.write(text_file) #Writes the textbox into the textfile
        self.encryptFile()
    
    def encryptFile(self): #Example of Encryption to File through Symmeric Encryption, this uses a specific key that is being used through Fernet and a key file that is used to Encrypt this specific file
        with open("file.key", "wb") as file: #A key is used as a way to encrypt the data from the CSV file into an encrypted file
            file.write(self.key)

        with open("file.key", "rb") as file:
            self.key = file.read()
        
        fernet = Fernet(self.key)

        with open(self.filepath, "rb") as file:
            original = file.read()
        
        encrypted = fernet.encrypt(original)

        with open(self.practice_encrypted_auditor_details, "wb") as encrypted_file:
            encrypted_file.write(encrypted)
    
    def decryptFile(self): #Example of Decryption from File through Symmeric Encryption, this uses a specific key that is being used through Fernet and a key file that is used to decrypt this specific file
        fernet = Fernet(self.key)

        with open(self.practice_encrypted_auditor_details, "rb") as file:
            encrypted = file.read()
        
        decrypted = fernet.decrypt(encrypted)

        with open(self.filepath, "wb") as file:
            file.write(decrypted)

    #Appends all contents in the temporary array
    def array(self):
        self.tempArray.append(self.ID)
        self.tempArray.append(self.firstName)
        self.tempArray.append(self.surname)
        self.tempArray.append(self.text)
        
        self.permArray.append(self.tempArray) #Later converted into an permament array
        self.permArray.sort(key = lambda x:x[0])
        self.tempArray = []
        print(self.permArray)

class Project:
    def __init__(self):
        self.create_project_name = ""
        self.view_project_name = ""
        self.projectID = ""
        self.startDate = ""
        self.endDate = ""
        self.date_format = ""
        self.start_date_obj = ""
        self.end_date_obj = ""
        self.letter = ""
        self.number = ""
        self.status = ""
        self.checkValidity = False
        self.tempArray = []
        self.projectArray = []
        self.key = Fernet.generate_key()
        self.practice_project_file = "practice_project_details.csv"
        self.practice_encrypted_project_file = "encrypted_practice_project_details.csv"
        self.projectFile = "projectFile.csv"
        self.encrypted_projectFile = "encrypted_project_details.csv"
        self.sorted_project_files = "sorted_project_details.csv"
    
    #Takes in the inputted values from the user
    def inputValues(self):
        self.create_project_name = create_project_Var.get()
        self.view_project_name = viewProject_Var.get()
        self.startDate = start_Date_Var.get()
        self.endDate = end_Date_Var.get()
        self.status = project_status_Var.get()

        self.date_format = "%d/%m/%Y" #Date is written in a specific format wherever necessary
    
    def project_create_checks(self):
        days_apart = 0 #Local Variable assigned for checking the range between start and end date

        #Error Exception Handling is used for converting the date
        try:
            self.start_date_obj = datetime.strptime(self.startDate, self.date_format)
            self.end_date_obj = datetime.strptime(self.endDate, self.date_format)

        except ValueError: #Catches the error when the wrong type of value is inputted
            messagebox.showerror("Error!", "Cannot Convert both Start and End Date to the right date format.")
            self.checkValidity = False
        
        else:
            messagebox.showinfo("Result!", "Perfectly converted both Start and End Date.")
            days_apart = self.end_date_obj - self.start_date_obj

            if days_apart.days < 0:
                messagebox.showerror("Error!", "Start Date is greater than End Date, Impossible!")
                self.checkValidity = False
            
            else:
                if len(self.create_project_name) <= 3 or len(self.create_project_name) >= 100:
                    messagebox.showerror("Error!", "Project Name is either too long or too short.")
                    self.checkValidity = False
                
                elif self.startDate == self.endDate or self.start_date_obj == self.end_date_obj:
                    messagebox.showerror("Error!", "Project Doesn't Count because of the same deadline.")
                    self.checkValidity = False
                
                else:
                    messagebox.showinfo("Result!", "Valid Project Name and Deadline")
                    self.checkValidity = True
                
    def project_view_checks(self):
        if len(self.view_project_name) <= 3 or len(self.view_project_name) >= 100:
            messagebox.showerror("Error!", "Project Name is either too long or too short.")
            self.checkValidity = False
        
        else:
            messagebox.showinfo("Result!", "Valid Project Name and Deadline")
            self.checkValidity = True

    #Creates the ID
    def Identification(self):
        self.letter = self.create_project_name[0:3] #Extracts the 1st 3 letters of the name
        self.number = random.randint(100, 999) #Randomises an integer
        self.projectID = (self.letter + str(self.number)).upper() #Creates the ID
    
    def array(self):
        self.tempArray.append(self.projectID)
        self.tempArray.append(self.create_project_name)
        self.tempArray.append(self.startDate)
        self.tempArray.append(self.endDate)
        self.tempArray.append(self.status)
        self.tempArray.append(self.start_date_obj.year)
        self.tempArray.append(self.end_date_obj.year)

        self.projectArray.append(self.tempArray)
        self.projectArray.sort(key = lambda x:(x[0], x[-2], x[-1]))
        self.tempArray = []
        print(self.projectArray)

#A Method that is used to write the current contents that are inputted by the user into a chosen CSV file, this is used to separate each field with commas and views them as individual field
    def write_to_file(self):
        try:
            file = open(self.practice_project_file, "a")
        
        except FileNotFoundError:
            messagebox.showerror("Error!", "File Cannot Open")
            quit()
        
        else:
            file.write(self.projectID + "," + self.create_project_name + "," + self.startDate + "," + self.endDate + "," + self.status) #Separator is used here
            file.write("\n")
            file.close()

    def encryptFile(self): #Example of Encryption to File through Symmeric Encryption, this uses a specific key that is being used through Fernet and a key file that is used to Encrypt this specific file
        with open("file.key", "wb") as file: #A key is used as a way to encrypt the data from the CSV file into an encrypted file
            file.write(self.key)

        with open("file.key", "rb") as file:
            self.key = file.read()
        
        fernet = Fernet(self.key)

        with open(self.practice_project_file, "rb") as file:
            original = file.read()
        
        encrypted = fernet.encrypt(original)

        with open(self.practice_encrypted_project_file, "wb") as encrypted_file:
            encrypted_file.write(encrypted)

    def read_from_file(self):
        try:
            file = open(self.practice_project_file, "r")
        
        except FileNotFoundError:
            messagebox.showerror("Error!", "File Cannot Open")
        
        else:
            csv.reader(file)
            file.close()

    def decryptFile(self): #Example of Decryption from File through Symmeric Encryption, this uses a specific key that is being used through Fernet and a key file that is used to decrypt this specific file
        fernet = Fernet(self.key)

        with open(self.practice_encrypted_project_file, "rb") as file:
            encrypted = file.read()
        
        decrypted = fernet.decrypt(encrypted)

        with open(self.practice_project_file, "wb") as file:
            file.write(decrypted)

    #Used as a method to sort the task details that are completely applicable to the user without fail
    def sort_fields(self):
        self.projectArray = [] #Uses an Empty Array that is defined for the fields to be sorted wherever possible

        with open(self.practice_project_file, "r") as file: #Opens the file in readmode
            reader = csv.reader(file) #A reader is used within the CSV file to read each field
            for i in reader:
                self.projectArray.append(i) #Inserts all record details within an array
        
        self.projectArray.sort(key=lambda x:x[0]) #A Lambda Expression is used here to sort all the releevant fields wherever necessary

        with open(self.sorted_project_files, "w", newline = "") as file:
            writer = csv.writer(file)
            writer.writerows(self.projectArray) #All rows are appended to the file based on the array

#Creates a class for storing all bank details
class Bank:
    def __init__(self): #Initialises with the relevant attrbiutes and the class itself
        self.sender_first_name = ""
        self.sender_surname = ""
        self.sender_name = ""
        self.receiver_first_name = ""
        self.receiver_surname = ""
        self.receiver_name = ""
        self.sender_bankName = ""
        self.receiver_bankName = ""
        self.sender_ID = ""
        self.receiver_ID = ""
        self.amount = ""
        self.date = ""
        self.time = ""
        self.date_str = ""
        self.date_format = ""
        self.date_obj = ""
        self.tempArray = []
        self.permArray = []
        self.checkValidity = False
        self.referenceValidity = False
        self.input_check = False
        self.practice_bank_file = "practice_bank_details.csv"
        self.practice_encrypted_bank_file = "practice_encrypted_bank_details.csv"
        self.sortedFiles = "sorted_bank_details.csv"
        self.senderFound = False
        self.receiverFound = False
        self.key = Fernet.generate_key() #Generates a specific key that is used for the data to be encrypted and decrypted

    #Takes in the values that are inputted for the bank page
    def inputValue(self):
        self.sender_first_name = sender_firstName_Var.get()
        self.sender_surname = sender_surname_Var.get()
        self.sender_bankName = sender_bankName_Var.get()

        self.receiver_first_name = receiver_firstName_Var.get()
        self.receiver_surname = receiver_surname_Var.get()
        self.receiver_bankName = receiver_bankName_Var.get()
        
        #Temporary self attributes assigned for later use
        self.sender_name = self.sender_first_name + " " + self.sender_surname
        self.receiver_name = self.receiver_first_name + " " + self.receiver_surname 

        self.amount = transfer_entry.get()

        self.date = date_Var.get()
        self.time = time_Var.get()

        self.date_str = self.date + " " + self.time #Combines the string variable together
        self.date_format = '%d/%m/%Y %I:%M%p' #Specified date format

        if self.sender_ID == "": #Checks if the inputted variable is unknown at the momemnt
            self.sender_ID = "Unknown"
        
        else:
            self.sender_ID = sender_ID_Var.get()
        
        if self.receiver_ID == "": #Checks if the inputted variable is unknown at the momemnt
            self.receiver_ID = "Unknown"
        
        else:
            self.receiver_ID = receiver_ID_Var.get()
            
        #Warnings to fill in the amount transferred and the time
        if self.time == "":
            messagebox.showerror("Error!", "Please remember to fill the time!")
            self.input_check = False
        
        if self.amount == "":
            messagebox.showerror("Error!", "Remember to fill the amount transferred")
            self.input_check = False
        
        else:
            self.input_check = True

    #Makes a number of checks to confirm the inputs from the user
    def bank_checks(self):
        #Exception Handling used to identify and catch errors for converting inputted data into a differnet datatype through casting
        try:
            self.amount = float(self.amount)

        except ValueError: #Exception Error Raised
            messagebox.showerror("Error!", "Cannot convert datatype to float")
            self.checkValidity = False

        else:
            messagebox.showinfo("Amount Transferred: ", self.amount)

        try: #Exception Handling used to identify and catch errors for converting inputted data into a specified format
            self.date_obj = datetime.strptime(self.date_str, self.date_format)
        
        except ValueError: #Exception Error Raised
            messagebox.showerror("Error!", "Cannot convert to Date and Time.")
            self.checkValidity = False
        
        else:
            messagebox.showinfo("Result!", "Converted Date and Time Perfectly.")

        #Validation and Verification Checks done within the program and making sure all checks have successfully been passed
        if self.sender_first_name == "" and self.sender_surname == "" and self.sender_bankName == "":
            messagebox.showerror("Error!", "Please fill all sender information!")
            self.checkValidity = False

        elif self.receiver_first_name == "" and self.receiver_surname == "" and self.receiver_bankName == "":
            messagebox.showerror("Error!", "Please fill all receiver information!")
            self.checkValidity = False
        
        elif (self.sender_name == self.receiver_name) and ((self.sender_bankName == self.receiver_bankName) or (self.sender_bankName != self.receiver_bankName)):
            messagebox.showerror("Error!", "Cannot Transfer transactions to yourself, what were you thinking!!!")
            self.checkValidity = False
        
        elif self.receiver_ID == self.sender_ID and (self.receiver_ID != "Unknown" and self.sender_ID != "Unknown"):
            messagebox.showerror("Error!", "ID cannot be same for both sender and receiver")
            self.checkValidity = False
    
        elif self.sender_ID.isalnum() != True and self.receiver_ID.isalnum() != True:
            messagebox.showerror("Error!", "IDs need to have letters and numbers")
            self.checkValidity = False
        
        elif len(self.sender_bankName) < 4 or len(self.sender_bankName) > 20:
            messagebox.showerror("Error!", "Sender Bank Name shouldn't be too short or too long")
            self.checkValidity = False
        
        elif len(self.receiver_bankName) < 4 or len(self.receiver_bankName) > 20:
            messagebox.showerror("Error!", "Receiver Bank Name shouldn't be too short or too long")
            self.checkValidity = False
        
        else:
            messagebox.showinfo("Result!", "All Fields have been filled")
            self.checkValidity = True
            self.ID_checks()
        
    def ID_checks(self): #Makes use of a Binary Search when searching through the file
        with open("employee_account_details.csv", "r") as accountFile:
            reader = csv.reader(accountFile) #Used as a reader for the csvfile
            sorted_data = sorted(reader, key=lambda x: x[0])
            found = bank_binary_search(sorted_data, self.sender_ID, self.receiver_ID)
            if found == True:
                self.senderFound, self.receiverFound == True, True
                messagebox.showinfo("Result!", "Found both Sender and Receiver ID")
                self.referenceValidity = True

            else:
                messagebox.showerror("Error!", "Cannot Continue with the transfer")

    #Stores all content into a temporary array
    def array(self):
        self.tempArray.append(self.sender_first_name)
        self.tempArray.append(self.sender_surname)
        self.tempArray.append(self.sender_bankName)
        self.tempArray.append(self.sender_ID)
        self.tempArray.append(self.receiver_first_name)
        self.tempArray.append(self.receiver_surname)
        self.tempArray.append(self.receiver_bankName)
        self.tempArray.append(self.receiver_ID)
        self.tempArray.append(self.amount)
        self.tempArray.append(self.date_str)
        self.tempArray.append(self.date_obj.year)
        self.tempArray.append(self.date_obj.hour)
        self.tempArray.append(self.date_obj.minute)

        self.permArray.append(self.tempArray) #Later converted into a permanent one for 2D arrays
        self.permArray.sort(key = lambda x:(x[-3], x[-2], x[-1])) #Uses a column sort based on specific fields
        self.tempArray = []
        print(self.permArray)

    #A Method that is used to write the current contents that are inputted by the user into a chosen CSV file, this is used to separate each field with commas and views them as individual field
    def write_to_file(self):
        #Exception Handling used to open the file
        try:
            file = open(self.practice_bank_file, "a")
        
        except FileNotFoundError: #Exception Error Raised
            messagebox.showerror("Error!", "File Cannot Open")
        
        else:
            #Writes all contents into the file and seprates each field with a , as its a CSV
            file.write(self.sender_first_name + "," + self.sender_surname + "," + self.sender_bankName + "," + self.sender_ID + "," + self.receiver_first_name + "," + self.receiver_surname + "," + self.receiver_bankName + "," + self.receiver_ID + "," + str(self.amount) + "," + self.date_str + "," + str(self.date_obj.year) + "," + str(self.date_obj.hour) + "," + str(self.date_obj.minute)) #Separator is used here
            file.write("\n") #New Line is written after the record has been added
            file.close()

    def encryptFile(self): #Example of Encryption to File through Symmeric Encryption, this uses a specific key that is being used through Fernet and a key file that is used to Encrypt this specific file
        with open("file.key", "wb") as file: #A key is used as a way to encrypt the data from the CSV file into an encrypted file
            file.write(self.key)

        with open("file.key", "rb") as file:
            self.key = file.read() #Used to retrieve the key used to encrypt the file
        
        fernet = Fernet(self.key) #Used to encrypt the file with this particular key

        with open(self.practice_bank_file, "rb") as file:
            original = file.read() #reads the original file
        
        encrypted = fernet.encrypt(original)

        with open(self.practice_encrypted_bank_file, "wb") as encrypted_file:
            encrypted_file.write(encrypted) #Writes all the encyrpted content within the file

    def read_from_file(self):
        #Exception Handling used to open the file
        try:
            file = open(self.practice_bank_file, "r")
        
        except FileNotFoundError: #Exception Error Raised
            messagebox.showerror("Error!", "File Cannot Open")
        
        else:
            csv.reader(file) #Used as a reader for the file
            file.close()

    def decryptFile(self): #Example of Decryption from File through Symmeric Encryption, this uses a specific key that is being used through Fernet and a key file that is used to decrypt this specific file
        fernet = Fernet(self.key)

        with open(self.practice_encrypted_bank_file, "rb") as file:
            encrypted = file.read()
        
        decrypted = fernet.decrypt(encrypted)

        with open(self.practice_bank_file, "wb") as file:
            file.write(decrypted)

    #Used as a method to sort the task details that are completely applicable to the user without fail
    def sort_fields(self):
        self.permArray = [] #Uses an Empty Array that is defined for the fields to be sorted wherever possible

        with open(self.practice_bank_file, "r") as file: #Opens the file in readmode
            reader = csv.reader(file) #A reader is used within the CSV file to read each field
            for i in reader:
                self.permArray.append(i) #Inserts all record details within an array
        
        self.permArray.sort(key=lambda x:x[0]) #A Lambda Expression is used here to sort all the releevant fields wherever necessary

        with open(self.sortedFiles, "w", newline = "") as file:
            writer = csv.writer(file)
            writer.writerows(self.permArray) #All rows are appended to the file based on the array
        print(self.permArray)

#Calls and instantaes the class using 5 distinctive and individual objects
staff = employee("Sample Firstname", "Sample Surname")
task = Task("Sample ID", "Sample First Name", "Sample Last Name")
auditor = Auditor("Sample FirstName", "Sample Last Name")
bank = Bank()
project = Project()

#Efficient way to shift between different screens
def transfer_screen(currentWindow, newWindow):
    currentWindow.destroy()
    newWindow()

#Function Process for managing the input of attributes for the account details
def accountCreation():
    global staff_firstname, staff_surname, ID_Create

    duplicateValidity = True

    if firstnameVar.get() == "" and surnameVar.get() == "" and Create_emailAddress_Var.get() == "" and passwordCreate_Var.get() == "" and option.get() == "": #Checks to see if all attributes are filled
        messagebox.showerror("Error!", "Please fill all the fields in")

    else:
        #Used to replace the string parameters before calling the class and creating the same object
        staff_firstname = firstnameVar.get()
        staff_surname = surnameVar.get()

        #Checks to see if these inputs are the same as the current parameters that were passed when creating the Object
        if staff_firstname != staff.firstname and staff_surname != staff.surname:
            staff.firstname = staff_firstname
            staff.surname = staff_surname

        staff.account() #Runs the procedure of checking inputted data regarding to creating the accounts

        #Linear Search Algorithm that is used for preventing any duplicates
        with open(staff.employeeFile, "r") as file:
            reader = csv.reader(file)
            for item in reader:
                if Create_emailAddress_Var.get() in item and passwordCreate_Var.get() in item:
                    duplicateValidity = True
                    messagebox.showerror("Error!", "Email and Password already exists")
                    break
                
                elif Create_emailAddress_Var.get() in item:
                    duplicateValidity = True
                    messagebox.showerror("Error!", "Email Address already exists")
                    break
                
                elif passwordCreate_Var.get() in item:
                    duplicateValidity = True
                    messagebox.showerror("Error!", "Password Already Exists")
                    break

                else:
                    duplicateValidity = False

        #Checks and Assigns the right Access Level to the user
        if staff.validity == True and staff.accessValidity == True and duplicateValidity == False and staff.access in ["Employee", "Senior Manager", "Auditor"]:
            print("Valid Account")
            messagebox.showinfo("Result!", "Valid Account")
            messagebox.showinfo("Welcome!", "Welcome!" + " " + staff.firstname + " " + staff.surname)

            staff.array()
            staff.write_to_file()
            staff.sort_fields()

            #Uses Symmetric Encryption with 1 key to be able to Encrypt and Decrypt the File
            staff.encryptFile()
            staff.decryptFile()
    
            #Transitions from the account window to the main task window
            accountWindow.destroy() #Destroys the current window
            taskWindow = createTaskWindow()
            taskWindow.mainloop()

    return #returns all contents to the function when accessed within the program

def account_binary_search(data, target_email, target_password): #Binary Search used to find the access level
    start, end = 0, len(data) - 1

    while start <= end:
        mid = (start + end) // 2
        current = data[mid]

        if target_email == current[3] and target_password == current[4]:
            staff.ID, staff.firstname, staff.surname = current[0], current[1], current[2]
            return current[5]  #finds the access level

        elif target_email < current[3] or (target_email == current[3] and target_password < current[4]):
            end = mid - 1

        else:
            start = mid + 1

    return None  #Returns when the access level isn't found

#Used for signing into the account
def accountRetrieve():
    global accountWindow, accessWindow, retrieve_job_role_Var

    #Assigned and Defined Variables
    if Retrieve_emailAddress_Var.get() == "" and passwordRetrieve_Var.get() == "":
        messagebox.showerror("Error!", "All Fields cannot be blank")

    elif (Retrieve_emailAddress_Var.get() == "" and passwordRetrieve_Var.get() != "") or (Retrieve_emailAddress_Var.get() != "" and passwordRetrieve_Var.get() == ""):
        messagebox.showwarning("Warning!", "Only 1 field has been filled")
    
    else:
        staff.retrieve_account()
        
        if staff.validity == True:
            with open(staff.employeeFile, "r") as file:
                reader = csv.reader(file)
                sorted_data = sorted(reader, key=lambda x: (x[3], x[4]))  #Sorts by specific columns like an insertion sort and makes a specific number of shifts wherever necessary
                access_level = account_binary_search(sorted_data, Retrieve_emailAddress_Var.get(), passwordRetrieve_Var.get())

                if access_level != None:
                    messagebox.showinfo("Result!", "Found the Account")
                    staff.access = access_level
                    messagebox.showinfo("Result!", "Your Access is" + " " + str(staff.access))

                    accountWindow.destroy()
                    taskWindow = createTaskWindow()
                    taskWindow.mainloop() 
                
                else:
                    messagebox.showerror("Result!", "Cannot Find the Account") 
        return

#Used to reset the data table to show its original contents
def reset_account_table():
    tableWindow.destroy() #Destorys the window before running the same procedure again
    view_employee_details()

def view_employee_details():
    global table, tableWindow, ID_searchVar, first_searchVar, last_searchVar, accessOption
    employeeConnector = sqlite3.connect('account_details.db') #Used to create a database as a connector when running SQL queries
    #The use of the connect method is for creating a database
    #Runs as either in memory (":memory:"), as a file name ("fileName.db") or an empty string

    employeeCursor = employeeConnector.cursor() #Creates a cursor which is used for manking any commits by creating a database and running such queries within SQL algorithms and queries
    
    #Types of data used in SQLite3 involves text, integer, real, blob or null *Only write this once to create the table and then either remove or comment it afterward
    # employeeCursor.execute("""CREATE TABLE employee ( #Creates the employee data table
    #                        identification text,
    #                        firstName text,
    #                        surname text,
    #                        access text
    # )""") #Uses a Doc String by surrounding the query with speech marks

    #Deletes all contents of the data table before inserting new ones in
    employeeCursor.execute("DELETE from employee")
    employeeConnector.commit()

    #Inserts the specific queries within the file
    with open(staff.employeeFile, "r") as file:
        reader = csv.reader(file)
        for item in reader: 
            employeeCursor.execute("INSERT into employee VALUES (?, ?, ?, ?)", (item[0], item[1], item[2], item[5])) #Iterative approach to insert specific fields into the file, uses ? as place holder and a tuple of values
            employeeConnector.commit()
    employeeConnector.close()

    tableWindow = Tk()
    tableWindow.title("Proposed Task Management System - All Account Details")
    table = ttk.Treeview(tableWindow)
    table["columns"] = ("ID", "First Name", "Surname", "Access")
    columns = ("ID", "First Name", "Surname", "Access")
    data = []

    tableFrame = Frame(tableWindow)

    searchWrapper = LabelFrame(tableFrame, text = "Search")

    ID_Label = Label(searchWrapper, text = "ID")
    ID_searchVar = StringVar()
    ID_searchEntry = Entry(searchWrapper, width = 30, textvariable = ID_searchVar)

    firstName_label = Label(searchWrapper, text = "First Name")
    first_searchVar = StringVar()
    first_searchEntry = Entry(searchWrapper, width = 30, textvariable = first_searchVar)

    surname_label = Label(searchWrapper, text = "Surname")
    last_searchVar = StringVar()
    last_searchEntry = Entry(searchWrapper, width = 30, textvariable = last_searchVar)

    access_label = Label(searchWrapper, text = "Access")
    accessOption = StringVar()
    access_search = OptionMenu(searchWrapper, accessOption, "Senior Manager", "Employee", "Auditor")
    searchButton = Button(searchWrapper, text = "Search!", command = searching)

    functionWrapper = LabelFrame(tableFrame, text = "Buttons")
    resetButton = Button(functionWrapper, text = "Reset!", command = reset_account_table)

    buttonWrapper = LabelFrame(tableFrame, text = "Transitions!")
    buttonFrame = Frame(buttonWrapper)
    accountButton = Button(buttonFrame, text = "Account Button", command = lambda: transfer_screen(tableWindow, makeAccountwindow))

    if staff.access == "Senior Manager":
        seniorButton = Button(buttonFrame, text = "Senior Manager Page", command = lambda: transfer_screen(tableWindow, seniorManagerPage))
        seniorButton.grid(row = 6, column = 2, padx = 5, pady = 5)

    table.column("#0", width = 0, stretch = NO)
    table.column("ID", anchor = CENTER, width = 100, minwidth = 25)
    table.column("First Name", anchor = CENTER, width = 100, minwidth = 25)
    table.column("Surname", anchor = CENTER, width = 100, minwidth = 25)
    table.column("Access", anchor = CENTER, width = 100, minwidth = 25)

    table.heading("ID", text = "ID")
    table.heading("First Name", text = "First Name")
    table.heading("Surname", text = "Surname")
    table.heading("Access", text = "Access")

    with open(staff.employeeFile, "r") as file:
        count = 0
        reader = csv.reader(file)
        for item in reader:
            table.insert(parent = '', index = "end", iid = count, text = "", values = (item[0], item[1], item[2], item[5]))
            data.append(item)
            count += 1
    
    for column in columns:
        table.heading(column, text=column, command=lambda c=column: on_sort(c, table))
    
    table.grid(row = 0, column = 0, padx = 10, pady = 10)
    tableFrame.grid(row = 1, column = 0, padx = 10, pady = 10)

    searchWrapper.grid(row = 1, column = 0, padx = 10, pady = 10)

    ID_Label.grid(row = 1, column = 0)
    ID_searchEntry.grid(row = 2, column = 0)

    firstName_label.grid(row = 1, column = 1)
    first_searchEntry.grid(row = 2, column = 1)

    surname_label.grid(row = 1, column = 2)
    last_searchEntry.grid(row = 2, column = 2)

    access_label.grid(row = 1, column = 3)
    access_search.grid(row = 2, column = 3)

    searchButton.grid(row = 1, column = 4)

    functionWrapper.grid(row = 3, column = 0, padx = 10, pady = 10)
    resetButton.grid(row = 3, column = 0, padx = 10, pady = 10)

    buttonWrapper.grid(row = 4, column = 0, padx = 10, pady = 10)
    buttonFrame.grid(row = 4, column = 0, padx = 10, pady = 10)
    accountButton.grid(row = 4, column = 1, padx = 10, pady = 10)
    return

def select():
    pass

#Searching Procedure that is used for finding specific fields with the use of SQL
def searching():
    count = 0
    employeeConnector = sqlite3.connect("account_details.db")
    employeeCursor = employeeConnector.cursor()

    if accessOption.get() != "":
        employeeCursor.execute("SELECT * from employee WHERE access=?", (accessOption.get(),))

        items = employeeCursor.fetchall() #Fetches all the particular items based on the query and loaded as a data structure

        table.delete(*table.get_children()) #Deletes all the contents before inserting the values

        for item in items:
            table.insert(parent = '', index = "end", iid = count, text = "", values = item)
            count += 1
    
    if ID_searchVar.get() != "":
        employeeCursor.execute("SELECT * from employee WHERE identification=?", (ID_searchVar.get(),))

        items = employeeCursor.fetchall() #Fetches all the particular items based on the query and loaded as a data structure

        table.delete(*table.get_children()) #Deletes all the contents before inserting the values

        for item in items:
            table.insert(parent = '', index = "end", iid = count, text = "", values = item)
            count += 1

    if first_searchVar.get() != "":
        employeeCursor.execute("SELECT * from employee WHERE firstName=?", (first_searchVar.get(),))

        items = employeeCursor.fetchall()

        table.delete(*table.get_children()) #Deletes all the contents before inserting the values

        for item in items:
            table.insert(parent = '', index = "end", iid = count, text = "", values = item)
            count += 1

    if last_searchVar.get() != "":
        employeeCursor.execute("SELECT * from employee WHERE surname=?", (last_searchVar.get(),))

        items = employeeCursor.fetchall()

        table.delete(*table.get_children()) #Deletes all the contents before inserting the values

        for item in items:
            table.insert(parent = '', index = "end", iid = count, text = "", values = item)
            count += 1

    employeeConnector.commit()
    employeeConnector.close()

#This is a sort example that will subject to change or stay the same, this makes use of the lambda function that is used to sort such relevant data, this uses a complex algorithm that is like Insertion Sort but also incorperates the idea of sorting into different fields that are chosen by the user in Ascending and Descending Order
def sortFunction(tree, column, descending):
    data = [(tree.set(item, column), item) for item in tree.get_children("")]
    data.sort(reverse=descending)
    for index, (val, item) in enumerate(data):
        tree.move(item, '', index)

def on_sort(column, table):
    sort_column = table.heading(column)["text"]
    if "↑" in sort_column:
        sortFunction(table, column, False)
        table.heading(column, text=(column + " ↓"))
    else:
        sortFunction(table, column, True)
        table.heading(column, text=(column + " ↑"))

def makeAccountwindow():
    global accountWindow, firstnameVar, surnameVar, Create_emailAddress_Var, passwordCreate_Var, option, Retrieve_emailAddress_Var, passwordRetrieve_Var, ID_retrieve_Var

    accountWindow = Tk()
    accountWindow.title("Task Management System - Account Page")
    tab = ttk.Notebook(accountWindow)
    tab.grid(row = 0, column = 0)

    frame = Frame(accountWindow, background = "Black")
    createAccount = Frame(tab, background = "Black")
    signIn = Frame(tab, background = "Black")
    buttonFrame = Frame(accountWindow)
    
    tab.add(createAccount, text = "Create Account")
    tab.add(signIn, text = "Sign in")

    account_heading = Label(createAccount, text = "Account Page", background = "Black", foreground = "White", font = ("Arial", 40, "bold", "underline"))

    firstName = Label(createAccount, text = "First Name: ", background = "Black", foreground = "White", font = ("Arial", 20, "bold"))
    firstnameVar = StringVar()
    firstname_entry = Entry(createAccount, width = 30, textvariable = firstnameVar)

    surname = Label(createAccount, text = "Surname: ", background = "Black", foreground = "White", font = ("Arial", 20, "bold"))
    surnameVar = StringVar()
    surname_entry = Entry(createAccount, width = 30, textvariable = surnameVar)

    Create_emailAddress = Label(createAccount, text = "Email Address: ", background = "Black", foreground = "White", font = ("Arial", 20, "bold"))
    Create_emailAddress_Var = StringVar()
    Create_emailAddress_entry = Entry(createAccount, width = 30, textvariable = Create_emailAddress_Var)

    passwordCreate = Label(createAccount, text = "Password: ", background = "Black", foreground = "White", font = ("Arial", 20, "bold"))
    passwordCreate_Var = StringVar()
    passwordCreate_entry = Entry(createAccount, width = 30, textvariable = passwordCreate_Var)

    job_role = Label(createAccount, text = "Job Role: ", background = "Black", foreground = "White", font = ("Arial", 20, "bold"))
    option = StringVar()
    drop = OptionMenu(createAccount, option, "Employee", "Senior Manager", "Auditor")

    create_account_button = Button(createAccount, text = "Create Account", background = "White", foreground = "Black", command = accountCreation)
    quitButton = Button(buttonFrame, text = "Click Here to Exit from the System", command = lambda: quit())
    tableButton = Button(buttonFrame, text = "View Table", command = lambda: transfer_screen(accountWindow, view_employee_details))

    frame.grid(row = 0, column = 0)
    account_heading.grid(row = 1, column = 0, padx = 10, pady = 10)

    firstName.grid(row = 2, column = 0)
    firstname_entry.grid(row = 3, column = 0, padx = 10, pady = 10)

    surname.grid(row = 4, column = 0) 
    surname_entry.grid(row = 5, column = 0, padx = 10, pady = 10)

    Create_emailAddress.grid(row = 6, column = 0)
    Create_emailAddress_entry.grid(row = 7, column = 0, padx = 10, pady = 10)

    passwordCreate.grid(row = 8, column = 0)
    passwordCreate_entry.grid(row = 9, column = 0, padx = 10, pady = 10)

    job_role.grid(row = 10, column = 0)
    drop.grid(row = 11, column = 0, padx = 10, pady = 10)

    create_account_button.grid(row = 12, column = 0, padx = 10, pady = 10)

    buttonFrame.grid(row = 13, column = 0)
    quitButton.grid(row = 14, column = 0)
    tableButton.grid(row = 14, column = 1)

    signIn_heading = Label(signIn, text = "Login Page", background = "Black", foreground = "White", font = ("Arial", 40, "bold", "underline"))
    
    Retrieve_emailAddress = Label(signIn, text = "Email Address", background = "Black", foreground = "White", font = ("Arial", 20, "bold"))
    Retrieve_emailAddress_Var = StringVar()
    Retrieve_emailAddress_entry = Entry(signIn, width = 30, textvariable = Retrieve_emailAddress_Var)

    passwordRetrieve = Label(signIn, text = "Password", background = "Black", foreground = "White", font = ("Arial", 20, "bold"))
    passwordRetrieve_Var = StringVar()
    passwordRetrieve_entry = Entry(signIn, width = 30, textvariable = passwordRetrieve_Var)

    retrieve_account_button = Button(signIn, text = "Sign In", background = "White", foreground = "Black", command = accountRetrieve)

    signIn_heading.grid(row = 0, column = 0)

    Retrieve_emailAddress.grid(row = 1, column = 0)
    Retrieve_emailAddress_entry.grid(row = 2, column = 0, padx = 10, pady = 10)

    passwordRetrieve.grid(row = 3, column = 0)
    passwordRetrieve_entry.grid(row = 4, column = 0, padx = 10, pady = 10)

    retrieve_account_button.grid(row = 5, column = 0, padx = 10, pady = 10)
    return accountWindow

#Used to log the user out of the system and back into the account page
def logOutScreen():
    answer = messagebox.askyesno("Logging out!", "Do you wish to Log out?")

    if answer == True:
        currentWindow.destroy()
        makeAccountwindow()

#Binary Search Algorithm used to find the project / task name
def prescence_binary_search(data, target_attribute): #Binary Search used to find the project / task details whilst assing parameters
    start, end = 0, len(data) - 1

    while start <= end:
        mid = (start + end) // 2
        current = data[mid]

        if target_attribute == current[1]:
            messagebox.showinfo("Result!", "Found the Name")
            return True  #finds the project Name if returned True

        elif target_attribute < current[1]:
            end = mid - 1

        else:
            start = mid + 1

#Used to perform such validation and verification techniques within the Task Page
def taskPage():
    found = False
    duplicateValidity = True

    if taskName_Var.get() == "" and priority_Var.get() == "" and status_Var.get() == "": #Checks if relevant fields have been filled
        messagebox.showerror("Error!", "Please fill these fields in, the last field is just an option.")

    else:
        #Used to replace the string parameters before calling the class and creating the same object
        task_ID = staff.ID
        task_firstname = staff.firstname
        task_surname = staff.surname

        #Checks to see if these inputs are the same as the current parameters that were passed when creating the Object
        if task_firstname != task.firstName and task_surname != task.surname and task_ID != task.employeeID:
            task.firsName = task_firstname
            task.surname = task_surname
            task.employeeID = task_ID
            
        task.inputValues() #Takes in the Input Values
        task.taskCreation_checks() #Takes in the Validation and Verification checks to be used on such data

        #Currently a Linear Search algorithm (hopefully change to binary search with a sorted data in the textfile)
        try:
            file = open(task.task_details, "r")

        except (AttributeError, FileNotFoundError):
            messagebox.showerror("Error!, File Cannot Open")

        else: #Slow Linear Search Algorithm is used here to check the input of the task name
            with open(task.task_details, "r") as file:
                reader = csv.reader(file)
                for item in reader:
                    if taskName_Var.get() in item:
                        duplicateValidity = True
                        messagebox.showerror("Error!", "Task Name already exists")
                        break

                    else:
                        duplicateValidity = False

        #Exception Handling is used to try and open the file and to identify and catch the errors which shouldn't cause the program to Crash
        if task.checkValidity == True: 
            try:
                view_project_file = open(project.practice_project_file, "r")
            
            except FileNotFoundError:
                messagebox.showerror("Error!", "Cannot Open File")
            
            else:
                reader = csv.reader(view_project_file)
                sorted_data = sorted(reader, key=lambda x: x[1])  #Sorts by specific columns like an insertion sort and makes a specific number of shifts wherever necessary
                found = prescence_binary_search(sorted_data, projectName_Var.get())
            
            if found == True:
                messagebox.showinfo("Result!", "Found the Project and No Dupliates")
        
            elif task.projectName == "None" or task.projectName == "":
                pass
                found = True

            else:
                messagebox.showerror("Error!", "Cannot Find Project")

        #Checks if the condition meets the final part of the array which sees if all relevant conditions are met with logical operators  
        if (task.checkValidity == True and duplicateValidity == False and task.projectName != "" and found == True) or (task.checkValidity == True and duplicateValidity == False and task.projectName == "" and found == True):
            task.array()
            task.write_to_file()
            task.sort_fields()
            task.encryptFile()
            task.decryptFile()
    return

#Resetting the interface which refreshes the interface before starting again
def resetButton(table, window):
    table.destroy()
    window()

#Views All of the Data like a Database Management System can be viewed by different users, they are able to search through the data instantly
def view_task_details():
    global table, task_table, searchInput, employeeID_input, employeeID_Var, taskName_input, taskName_Var, start_date_input, startDate_Var, end_date_input, endDate_Var, priority_input, priority_entry_input, priority_Var, status_input, status_entry_input, status_Var, projectName_input, taskID, completeCount, completedTasks, incompleteCount, incompletedTasks, currently_working_count, currently_working_Tasks
    taskConnector = sqlite3.connect('task_information.db') #Used to create a database as a connector when running SQL queries
    #The use of the connect method is for creating a database
    #Runs as either in memory (":memory:"), as a file name ("fileName.db") or an empty string

    taskCursor = taskConnector.cursor() #Creates a cursor which is used for making any commits by creating a database and running such quieries within SQL algorithms and queries
    
    #Types of data used in SQLite3 involves text, integer, real, blob or null *Only write this once to create the table and then either remove or comment it afterwards
    #Creates the task data table
    # taskCursor.execute("""CREATE TABLE task_details (
    #                 employee_identification text,
    #                 task_identification text,
    #                 taskName text,
    #                 startDate text,
    #                 endDate text,
    #                 priors text,
    #                 statusInfo text,
    #                 projectName text
    # )""") #Uses a Doc String by surrounding the query with speech marks

    #Deletes all contents of the data table before inserting new ones in
    taskCursor.execute("DELETE from task_details")
    taskConnector.commit()

    #Inserts the specific queries within the file
    with open(task.task_details, "r") as file:
        reader = csv.reader(file)
        for item in reader: 
            taskCursor.execute("INSERT into task_details VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7])) #Iterative approach to insert specific fields into the file, uses ? as place holder and a tuple of values
            taskConnector.commit()
    taskConnector.close()

    completeCount = 0 
    incompleteCount = 0 
    currently_working_count = 0 
    taskID = ""

    task_table = Tk() 
    task_table.title("Task Data Table") 

    table = ttk.Treeview(task_table) 
    table["columns"] = ("Employee ID", "Task ID", "Task Name", "Start Date", "End Date", "Priority", "Status", "Project Name") #Determines the Columns 
    columns = ("Employee ID", "Task ID", "Task Name", "Start Date", "End Date", "Priority", "Status", "Project Name") 
    taskData = [] #Appends all this in a data 

    #Attrbuted Frames and Buttons are created 
    task_table_frame = Frame(task_table) 
    buttonFrame = Frame(task_table) 

    searchWrapper = LabelFrame(task_table_frame, text = "Search") 
    searchLabel = Label(searchWrapper, text = "Employee ID: ", font = ("Arial", 10, "bold")) 
    searchInput = StringVar() 
    searchEntry = Entry(searchWrapper, width = 25, textvariable = searchInput) 
    searchButton = Button(searchWrapper, text = "Search", command = searchFunction) 

    statisticsWrapper = LabelFrame(task_table_frame, text = "Statistics") 
    completedTasks = Label(statisticsWrapper, text = ("Tasks Completed: " + str(completeCount)), font = ("Arial", 10, "bold")) 
    incompletedTasks = Label(statisticsWrapper, text = ("Tasks Incompleted: " + str(incompleteCount)), font = ("Arial", 10, "bold")) 
    currently_working_Tasks = Label(statisticsWrapper, text = ("Tasks Currently in Progress: " + str(currently_working_count)), font = ("Arial", 10, "bold")) 

    functionWrapper = LabelFrame(task_table_frame, text = "Function Buttons")     
    reset_button = Button(functionWrapper, text = "Reset", command = lambda: resetButton(task_table, view_task_details)) 

    buttonWrapper = LabelFrame(task_table_frame, text = "Buttons") 
    select_button = Button(buttonWrapper, text = "Select Field", command = task_select_field) 
    update_button = Button(buttonWrapper, text = "Update Field", command = task_update_field) 
    insert_button = Button(buttonWrapper, text = "Insert Field", command = task_insert_field)
    save_button = Button(buttonWrapper, text = "Save Details", command = save_file)
    load_button = Button(buttonWrapper, text = "Load Details", command = open_file)

    transitionWrapper = LabelFrame(buttonFrame, text = "Transitions!") 
    task_button = Button(transitionWrapper, text = "Task Page", command = lambda: transfer_screen(task_table, createTaskWindow)) 

    if staff.access == "Senior Manager":
        seniorButton = Button(buttonFrame, text = "Senior Manager Page", command = lambda: transfer_screen(task_table, seniorManagerPage))
        seniorButton.grid(row = 6, column = 2, padx = 5, pady = 5)

    inputWrapper = LabelFrame(task_table_frame, text = "Inputs")

    employeeID = Label(inputWrapper, text = "Employee ID", font = ("Arial", 10, "bold"))
    employeeID_Var = StringVar()
    employeeID_input = Entry(inputWrapper, width = 25, textvariable = employeeID_Var)

    taskName = Label(inputWrapper, text = "Task Name", font = ("Arial", 10, "bold")) 
    taskName_Var = StringVar() 
    taskName_input = Entry(inputWrapper, width = 25, textvariable = taskName_Var) 

    start_date = Label(inputWrapper, text = "Start Date", font = ("Arial", 10, "bold")) 
    startDate_Var = StringVar() 
    start_date_input = DateEntry(inputWrapper, width = 25, textvariable = startDate_Var, date_pattern = "dd/mm/yyyy") 

    end_date = Label(inputWrapper, text = "End Date", font = ("Arial", 10, "bold")) 
    endDate_Var = StringVar() 
    end_date_input = DateEntry(inputWrapper, width = 25, textvariable = endDate_Var, date_pattern = "dd/mm/yyyy") 

    priority = Label(inputWrapper, text = "Priority", font = ("Arial", 10, "bold")) 
    priority_Var = StringVar() 
    priority_input = OptionMenu(inputWrapper, priority_Var, "Critical", "High", "Medium", "Low") 
    priority_entry_input = Entry(inputWrapper, width = 25, textvariable = priority_Var)

    status = Label(inputWrapper, text = "Status", font = ("Arial", 10, "bold")) 
    status_Var = StringVar() 
    status_input = OptionMenu(inputWrapper, status_Var, "Completed", "Currently Working", "Incomplete") 
    status_entry_input = Entry(inputWrapper, width = 25, textvariable = status_Var)

    projectName = Label(inputWrapper, text = "Project Name", font = ("Arial", 10, "bold")) 
    projectName_Var = StringVar() 
    projectName_input = Entry(inputWrapper, width = 25, textvariable = projectName_Var)

    #Columns are defined here with a position and width attribute, this must match the tuples in teh columns otherwise this can produce in errors wherever necessary 
    table.column("#0", width = 0, stretch = NO) 
    table.column("Employee ID", width = 100, minwidth = 25, anchor = W) 
    table.column("Task ID", width = 100, minwidth = 25, anchor = W) 
    table.column("Task Name", width = 100, minwidth = 25, anchor = W) 
    table.column("Start Date", width = 100, minwidth = 25, anchor = W) 
    table.column("End Date", width = 100, minwidth = 25, anchor = W) 
    table.column("Priority", width = 100, minwidth = 25, anchor = W) 
    table.column("Status", width = 100, minwidth = 25, anchor = W) 
    table.column("Project Name", width = 100, minwidth = 25, anchor = W) 

    #Creates the headings that are based on the columns 
    table.heading("Employee ID", text = "Employee ID")
    table.heading("Task ID", text = "Task ID") 
    table.heading("Task Name", text = "Task Name") 
    table.heading("Start Date", text = "Start Date") 
    table.heading("End Date", text = "End Date") 
    table.heading("Priority", text = "Priority") 
    table.heading("Status", text = "Status") 
    table.heading("Project Name", text = "Project Name") 

    try: 
        file = open(task.task_details, "r") 

    except (AttributeError, FileNotFoundError): 
        messagebox.showerror("Error!", "Cannot Open the File") 

    else:
        with open(task.task_details, "r") as file: 
            count = 0 
            reader = csv.reader(file) 
            for item in reader: 
                table.insert(parent = '', index = "end", iid = count, text = "", values = item) #Inserts all the Fields from the relevant textfile in a linear approach taskData.append(item) 
                count += 1 

                if item[-2] == "Completed": 
                    completeCount += 1 

                elif item[-2] == "Incomplete": 
                    incompleteCount += 1 

                elif item[-2] == "Currently Working": 
                    currently_working_count += 1 

            for column in columns: 
                table.heading(column, text=column, command=lambda c=column: on_sort(c, table)) #Sorts the columns based on the headings that are used to sort the data table 

    completedTasks.config(text = ("Tasks Completed: " + str(completeCount))) 
    incompletedTasks.config(text = ("Tasks Incompleted: " + str(incompleteCount))) 
    currently_working_Tasks.config(text = ("Tasks Currently in Progress: " + str(currently_working_count))) 

    #Places all the fields together with the grid function for a more accurate placing 
    table.grid(row = 0, column = 0, padx = 5, pady = 5) 
    task_table_frame.grid(row = 1, column = 0, padx = 5, pady = 5) 

    searchWrapper.grid(row = 1, column = 0, padx = 5, pady = 5) 
    searchLabel.grid(row = 1, column = 0, padx = 5, pady = 5) 
    searchEntry.grid(row = 1, column = 1, padx = 5, pady = 5) 
    searchButton.grid(row = 1, column = 2, padx = 5, pady = 5) 

    statisticsWrapper.grid(row = 2, column = 0, padx = 5, pady = 5) 
    completedTasks.grid(row = 2, column = 0, padx = 5, pady = 5) 
    incompletedTasks.grid(row = 2, column = 1, padx = 5, pady = 5) 
    currently_working_Tasks.grid(row = 2, column = 2, padx = 5, pady = 5) 

    functionWrapper.grid(row = 3, column = 0, padx = 5, pady = 5) 
    reset_button.grid(row = 3, column = 1, padx = 5, pady = 5) 

    inputWrapper.grid(row = 4, column = 0, padx = 5, pady = 5)

    employeeID.grid(row = 4, column = 0)
    employeeID_input.grid(row = 5, column = 0)

    taskName.grid(row = 4, column = 1) 
    taskName_input.grid(row = 5, column = 1)

    start_date.grid(row = 4, column = 2) 
    start_date_input.grid(row = 5, column = 2) 

    end_date.grid(row = 4, column = 3) 
    end_date_input.grid(row = 5, column = 3) 

    priority.grid(row = 4, column = 4) 
    priority_input.grid(row = 5, column = 4)

    status.grid(row = 4, column = 5) 
    status_input.grid(row = 5, column = 5) 

    projectName.grid(row = 4, column = 6) 
    projectName_input.grid(row = 5, column = 6) 

    buttonFrame.grid(row = 6, column = 0) 
    transitionWrapper.grid(row = 6, column = 0) 
    task_button.grid(row = 6, column = 1) 

    buttonWrapper.grid(row = 7, column = 0, padx = 5, pady = 5) 
    select_button.grid(row = 7, column = 1, padx = 5, pady = 5) 
    update_button.grid(row = 7, column = 2, padx = 5, pady = 5) 
    insert_button.grid(row = 7, column = 3, padx = 5, pady = 5)
    save_button.grid(row = 7, column = 4, padx = 5, pady = 5)
    load_button.grid(row = 7, column = 5, padx = 5, pady = 5)
    return

def task_select_field(): 
    global taskID, employeeID
    taskID = "" 
    employeeID_input.delete(0, END)
    taskName_input.delete(0, END) 
    start_date_input.delete(0, END) 
    end_date_input.delete(0, END)
    priority_entry_input.delete(0, END)
    status_entry_input.delete(0, END)
    projectName_input.delete(0, END) 

    #selecting the record number 
    selected = table.focus() 

    #selecting the value 
    values = table.item(selected, 'values') #Passes 2 different parameters for the item to be selected, the number of records and the text 

    if values == "": 
        messagebox.showwarning("Warning", "No record has been selected.") 

    #Outputting the values to the box 
    else:
        employeeID_input.insert(0, values[0])
        taskID = values[1] 
        taskName_input.insert(0, values[2]) 
        start_date_input.insert(0, values[3]) 
        end_date_input.insert(0, values[4]) 
        priority_entry_input.insert(0, values[5]) 
        status_entry_input.insert(0, values[6]) 
        projectName_input.insert(0, values[7]) 

def task_update_field(): 
    selected = table.focus()
    values = table.item(selected, text = "", values = (employeeID_input.get(), taskID, taskName_input.get(), start_date_input.get(), end_date_input.get(), priority_Var.get(), status_Var.get(), projectName_input.get())) 

    employeeID_input.delete(0, END)
    taskName_input.delete(0, END) 
    start_date_input.delete(0, END) 
    end_date_input.delete(0, END)
    priority_entry_input.delete(0, END)
    status_entry_input.delete(0, END)
    projectName_input.delete(0, END)  

    with open(task.task_details, "w", newline = "") as task_details:
        writer = csv.writer(task_details)

        for item_id in table.get_children():
            value = table.item(item_id, 'values')
            writer.writerow(value)

def task_insert_field():
    local_count = len(table.get_children())
    employeeID = staff.ID
    task.inputValues()
    task.taskCreation_checks()

    if task.checkValidity == True:
        table.insert(parent = '', index = "end", iid = local_count, text = "", values = (employeeID, task.taskID, taskName_input.get(), start_date_input.get(), end_date_input.get(), priority_Var.get(), status_Var.get(), task.projectName))
        local_count += 1

        taskName_input.delete(0, END) 
        start_date_input.delete(0, END)
        end_date_input.delete(0, END)
        priority_entry_input.delete(0, END)
        status_entry_input.delete(0, END)
        projectName_input.delete(0, END) 

def save_file():
    filepath = asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]) #asksaveasfilename is a dialog from the tkinter.filedialog module which displays a file open dialog and stores the file path to the variable for the user to save their file
    if not filepath:
        return
    
    with open(filepath, mode="w", encoding="utf-8", newline = "") as output_file: #UTF 8 is a standard encoding tool
        writer = csv.writer(output_file)

        for item_id in table.get_children():
            value = table.item(item_id, 'values')
            writer.writerow(value)

def open_file():
    count = 0
    completeCount = 0 
    incompleteCount = 0 
    currently_working_count = 0 
    filepath = askopenfilename(filetypes = [("CSV Files", "*.csv"), ("All Files", "*.*")]) #askopenfilename is a dialog from the tkinter.filedialog module which displays a file open dialog and stores the file path to the variable
    if not filepath: #Used to check if the button pressed isn't open meaning that the filepath doesn't contain any data and returns without executing any code
        return
    table.delete(*table.get_children())

    with open(filepath, mode="r", encoding="utf-8") as input_file: #UTF 8 is a standard encoding tool
        reader = csv.reader(input_file)

        for item in reader:
            table.insert(parent = '', index = "end", iid = count, text = "", values = item)
            count += 1

            if item[-2] == "Completed":
                completeCount += 1

            if item[-2] == "Incomplete":
                incompleteCount += 1

            if item[-2] == "Currently Working":
                currently_working_count += 1

    completedTasks.config(text = ("Tasks Completed: " + str(completeCount))) 
    incompletedTasks.config(text = ("Tasks Incompleted: " + str(incompleteCount))) 
    currently_working_Tasks.config(text = ("Tasks Currently in Progress: " + str(currently_working_count))) 

def searchFunction():
    count = 0
    taskConnector = sqlite3.connect('task_information.db')
    taskCursor = taskConnector.cursor()

    if status_Var.get() != "":
        taskCursor.execute("SELECT * from task_details WHERE statusInfo=?", (status_Var.get(),))

        items = taskCursor.fetchall() #Fetches all the particular items based on the query and loaded as a data structure

        table.delete(*table.get_children()) #Deletes all the contents before inserting the values

        for item in items:
            table.insert(parent = '', index = "end", iid = count, text = "", values = item)
            count += 1

    if priority_Var.get() != "":
        taskCursor.execute("SELECT * from task_details WHERE priors=?", (priority_Var.get(),))

        items = taskCursor.fetchall() #Fetches all the particular items based on the query and loaded as a data structure

        table.delete(*table.get_children()) #Deletes all the contents before inserting the values

        for item in items:
            table.insert(parent = '', index = "end", iid = count, text = "", values = item)
            count += 1

    if searchInput.get() != "":
        taskCursor.execute("SELECT * from task_details WHERE employee_identification=?", (searchInput.get(),))

        items = taskCursor.fetchall() #Fetches all the particular items based on the query and loaded as a data structure

        table.delete(*table.get_children()) #Deletes all the contents before inserting the values

        for item in items:
            table.insert(parent = '', index = "end", iid = count, text = "", values = item)
            count += 1
    
    taskConnector.commit()
    taskConnector.close()

#Creates the main task page and window that is for the main page
def createTaskWindow():
    global currentWindow, taskWindow, buttonFrame, taskName_Var, startDate_Var, endDate_Var, priority_Var, status_Var, projectName_Var, project_name #Globalises the Variables involved in the system
    taskWindow = Tk() #Creates the window
    taskWindow.title("Task Management System - Task Page") #Adds the Caption of the window as the Title of the window
    currentWindow = taskWindow

    #Creates the icon widgets such as frames, labels and entry inputs and text
    taskFrame = Frame(taskWindow, background = "Black")
    task_heading = Label(taskFrame, background = "Black", foreground = "White", text = "Task Page", font = ("Arial", 40, "bold", "underline"))

    taskName = Label(taskFrame, text = "Task Name: ", background = "Black", foreground = "White", font = ("Arial", 20, "bold"))
    taskName_Var = StringVar()
    name = Entry(taskFrame, textvariable = taskName_Var)

    startDate = Label(taskFrame, text = "Start Date: ", background = "Black", foreground = "White", font = ("Arial", 20, "bold"))
    startDate_Var = StringVar()
    start = DateEntry(taskFrame, width = 30, textvariable = startDate_Var, date_pattern = "dd/mm/yyyy")

    endDate = Label(taskFrame, text = "End Date: ", background = "Black", foreground = "White", font = ("Arial", 20, "bold"))
    endDate_Var = StringVar()
    end = DateEntry(taskFrame, width = 30, textvariable = endDate_Var, date_pattern = "dd/mm/yyyy")

    priority = Label(taskFrame, text = "Priority: ", background = "Black", foreground = "White", font = ("Arial", 20, "bold"))
    priority_Var = StringVar()
    prior = OptionMenu(taskFrame, priority_Var, "Low", "Medium", "High", "Critical")

    status = Label(taskFrame, text = "Status ", background = "Black", foreground = "White", font = ("Arial", 20, "bold"))
    status_Var = StringVar()
    state = OptionMenu(taskFrame, status_Var, "Incomplete", "Currently Working", "Completed")
    #The use of OptionMenu is used as a drop down menu that can be used as a way for users to be able to add different choices of inputs and restricts them of any inputs that are used wherever necessary

    projectName = Label(taskFrame, text = "Project Name:  ", background = "Black", foreground = "White", font = ("Arial", 20, "bold"))
    projectName_Var = StringVar()
    project_name = Entry(taskFrame, width = 30, textvariable = projectName_Var)

    addTask = Button(taskFrame, text="Add Task", command = taskPage)

    buttonFrame = Frame(taskWindow)
    log_out_button = Button(buttonFrame, text = "Log Out", command = logOutScreen)
    bankButton = Button(buttonFrame, text = "Archiving Bank Transfer System", command = lambda: transfer_screen(taskWindow, bankPage))
    projectButton = Button(buttonFrame, text = "Project Screen", command = lambda: transfer_screen(taskWindow, projectPage))
    task_table_button = Button(buttonFrame, text = "View Task Table", command = lambda: transfer_screen(taskWindow, view_task_details))

    if staff.access == "Senior Manager" or staff.access == "Auditor":
        warning = Label(buttonFrame, foreground = "Black", text = "Please remeber to save and close other running windows other than this main window", font = ("Arial", 10, "bold")) #This is used based on the different access levels provided on the screen

    if staff.access == "Senior Manager":
        seniorButton = Button(buttonFrame, text = "Senior Manager Page", command = lambda: transfer_screen(taskWindow, seniorManagerPage))
        seniorButton.grid(row = 4, column = 1, padx = 5, pady = 5)
        warning.grid(row = 4, column = 6, padx = 5, pady = 5)
    
    if staff.access == "Auditor":
        auditorButton = Button(buttonFrame, text = "Auditor Page", command = lambda: transfer_screen(taskWindow, auditorPage))
        auditorButton.grid(row = 4, column = 1, padx = 5, pady = 5)
        warning.grid(row = 4, column = 6, padx = 5, pady = 5)

    #Places the labels and the buttons together with teh use of grid together
    taskFrame.grid(row = 0, column = 0, padx = 5, pady = 5)
    task_heading.grid(row = 1, column = 0, padx = 5, pady = 5)

    taskName.grid(row = 2, column = 0, padx = 5, pady = 5)
    name.grid(row = 3, column = 0, padx = 5, pady = 5)

    startDate.grid(row = 2, column = 1, padx = 5, pady = 5)
    start.grid(row = 3, column = 1, padx = 5, pady = 5)

    endDate.grid(row = 2, column = 2, padx = 5, pady = 5)
    end.grid(row = 3, column = 2, padx = 5, pady = 5)

    priority.grid(row = 2, column = 3, padx = 5, pady = 5)
    prior.grid(row = 3, column = 3, padx = 5, pady = 5)

    status.grid(row = 2, column = 4, padx = 5, pady = 5)
    state.grid(row = 3, column = 4, padx = 5, pady = 5)

    projectName.grid(row = 2, column = 5, padx = 5, pady = 5)
    project_name.grid(row = 3, column = 5, padx = 5, pady = 5)

    addTask.grid(row = 2, column = 6, padx = 5, pady = 5)

    buttonFrame.grid(row = 4, column = 0, padx = 5, pady = 5)
    log_out_button.grid(row = 4, column = 2, padx = 5, pady = 5)
    bankButton.grid(row = 4, column = 3, padx = 5, pady = 5)
    projectButton.grid(row = 4, column = 4, padx = 5, pady = 5)
    task_table_button.grid(row = 4, column = 5, padx = 5, pady = 5)
    
    taskWindow.mainloop()
    return taskWindow #Returns the window

def reset_project_Button():
    project_table.destroy()
    view_project_details()

#Do not run this script yet
def view_project_details():
    global project_table, table, projectName_input, create_project_Var, start_date_input, start_Date_Var, end_date_input, end_Date_Var, project_status_Var, status_entry_input, search_var #Globalises the Variable which is used for a further scope within viewing details as a data table
    projectConnector = sqlite3.connect("project_details.db")
    #The use of the connect method is for creating a database
    #Runs as either in memory (":memory:"), as a file name ("fileName.db") or an empty string

    projectCursor = projectConnector.cursor() #Creates a cursor which is used for manking any commits by creating a database and running such quieries within SQL algorithms and queries
    
    #Types of data used in SQLite3 involves text, integer, real, blob or null *Only write this once to create the table and then either remove or comment it afterwards
    #Creates the Project data table
    # projectCursor.execute("""CREATE TABLE project (
    #                 identification text,
    #                 projectName text,
    #                 startDate text,
    #                 endDate text,
    #                 statusInfo text
    # )""") #Uses a Doc String by surrounding the query with speech marks
    # projectConnector.commit()

    #Deletes all contents of the data table before inserting new ones in
    projectCursor.execute("DELETE from project")
    projectConnector.commit()

    #Inserts the specific queries within the file
    with open(project.practice_project_file, "r") as file:
        reader = csv.reader(file)
        for item in reader: 
            projectCursor.execute("INSERT into project VALUES (?, ?, ?, ?, ?)", (item[0], item[1], item[2], item[3], item[4])) #Iterative approach to insert specific fields into the file, uses ? as place holder and a tuple of values
            projectConnector.commit()
    projectConnector.close()

    #Creates the window and the title
    project_table = Tk()
    project_table.title("Proposed Task Management System - Project Table")

    table = ttk.Treeview(project_table) #Creates the table under a particular frame and identifies the specified columns
    table["columns"] = ("ID", "Project Name", "Start Date", "End Date", "Status")
    columns = ("ID", "Project Name", "Start Date", "End Date", "Status")
    projectData = []

    #Frames used for the table and for separate functions and identities
    project_table_frame = Frame(project_table)
    buttonFrame = Frame(project_table)

    #Wrapper Frames used to wrap other attributes such as labels and entry for a more organised approach when viewing the system
    searchWrapper = LabelFrame(project_table_frame, text = "Searching")
    searchLabel = Label(searchWrapper, text = "Project ID: ")
    search_var = StringVar()
    searchEntry = Entry(searchWrapper, width = 30, textvariable = search_var)
    searchButton = Button(searchWrapper, text = "Search", command = project_searchFunction)

    #Wrapper Frames used to wrap other attributes such as labels and entry for a more organised approach when viewing the system
    functionWrapper = LabelFrame(project_table_frame, text = "Buttons")
    reset_button = Button(functionWrapper, text = "Reset", command = reset_project_Button)

    #Wrapper Frames used to wrap other attributes such as labels and entry for a more organised approach when viewing the system
    buttonWrapper = LabelFrame(project_table_frame, text = "Buttons") 
    select_button = Button(buttonWrapper, text = "Select Field", command = project_select_field) 
    update_button = Button(buttonWrapper, text = "Update Field", command = project_update_field) 
    insert_button = Button(buttonWrapper, text = "Insert Field", command = project_insert_field)
    save_button = Button(buttonWrapper, text = "Save Details", command = save_file)
    load_button = Button(buttonWrapper, text = "Load Details", command = open_file)

    #Wrapper Frames used to wrap other attributes such as labels and entry for a more organised approach when viewing the system
    inputWrapper = LabelFrame(project_table_frame, text = "Inputs")

    #Inputs and Labels defined for changing a record
    projectName = Label(inputWrapper, width = 25, text = "Project Name", font = ("Arial", 10, "bold"))
    create_project_Var = StringVar()
    projectName_input = Entry(inputWrapper, width = 25, textvariable = create_project_Var)

    start_date = Label(inputWrapper, width = 25, text = "Start Date", font = ("Arial", 10, "bold"))
    start_Date_Var = StringVar()
    start_date_input = DateEntry(inputWrapper, width = 25, textvariable = start_Date_Var, date_pattern = "dd/mm/yyyy")

    end_date = Label(inputWrapper, width = 25, text = "End Date", font = ("Arial", 10, "bold"))
    end_Date_Var = StringVar()
    end_date_input = DateEntry(inputWrapper, width = 25, textvariable =  end_Date_Var, date_pattern = "dd/mm/yyyy")

    status = Label(inputWrapper, width = 25, text = "Status", font = ("Arial", 10, "bold"))
    project_status_Var = StringVar()
    status_input = OptionMenu(inputWrapper, project_status_Var, "Completed", "Currently Working", "Incomplete")
    status_entry_input = Entry(inputWrapper, width = 25, textvariable = project_status_Var)

    #Wrapper Frames used to wrap other attributes such as labels and entry for a more organised approach when viewing the system
    transitionWrapper = LabelFrame(buttonFrame, text = "Transitions!")
    project_button = Button(transitionWrapper, text = "Project Page", command = lambda: transfer_screen(project_table, projectPage))

    #Creating and Labelling the columns within the treeview system, this also involves using #0 as a compulsory and main column whcih can be removed
    table.column("#0", width = 0, stretch = NO)
    table.column("ID", width = 100, minwidth = 25, anchor = W)
    table.column("Project Name", width = 100, minwidth = 25, anchor = W)
    table.column("Start Date", width = 100, minwidth = 25, anchor = W)
    table.column("End Date", width = 100, minwidth = 25, anchor = W)
    table.column("Status", width = 100, minwidth = 25, anchor = W)

    #Headings are created and should match with the specified columns wherever necessary
    table.heading("ID", text = "ID")
    table.heading("Project Name", text = "Project Name")
    table.heading("Start Date", text = "Start Date")
    table.heading("End Date", text = "End Date")
    table.heading("Status", text = "Status")

    #Inserting the data
    with open(project.practice_project_file, "r") as file: #Uses a Linear Search to be able to insert each record line by line from the file and insert relevant details wherever necessary
        count = 0
        reader = csv.reader(file)
        for item in reader:
            table.insert(parent = '', index = "end", iid = count, text = "", values = item)
            projectData.append(item)
            count += 1

        for column in columns:
            table.heading(column, text=column, command=lambda c=column: on_sort(c, table)) #Sorts the columns based on the headings that are used to sort the data table

    #Positioning and placing all icons defined earlier with the Grid Function (defines the row and column of the piece)
    table.grid(row = 0, column = 0, padx = 5, pady = 5)
    project_table_frame.grid(row = 1, column = 0, padx = 5, pady = 5)

    searchWrapper.grid(row = 1, column = 0, padx = 5, pady = 5)
    searchLabel.grid(row = 1, column = 0, padx = 5, pady = 5)
    searchEntry.grid(row = 1, column = 1, padx = 5, pady = 5)
    searchButton.grid(row = 1, column = 2, padx = 5, pady = 5)

    functionWrapper.grid(row = 2, column = 0, padx = 5, pady = 5)
    reset_button.grid(row = 2, column = 0, padx = 5, pady = 5)

    inputWrapper.grid(row = 3, column = 0, padx = 5, pady = 5)

    projectName.grid(row = 3, column = 0, padx = 5, pady = 5)
    projectName_input.grid(row = 4, column = 0, padx = 5, pady = 5)

    start_date.grid(row = 3, column = 1, padx = 5, pady = 5)
    start_date_input.grid(row = 4, column = 1, padx = 5, pady = 5)

    end_date.grid(row = 3, column = 2, padx = 5, pady = 5)
    end_date_input.grid(row = 4, column = 2, padx = 5, pady = 5)

    status.grid(row = 3, column = 3, padx = 5, pady = 5)
    status_input.grid(row = 4, column = 3, padx = 5, pady = 5)

    buttonFrame.grid(row = 5, column = 0, padx = 5, pady = 5)
    transitionWrapper.grid(row = 5, column = 0, padx = 5, pady = 5)
    project_button.grid(row = 5, column = 0, padx = 5, pady = 5)

    buttonWrapper.grid(row = 6, column = 0, padx = 5, pady = 5)
    select_button.grid(row = 6, column = 0, padx = 5, pady = 5)
    update_button.grid(row = 6, column = 1, padx = 5, pady = 5)
    insert_button.grid(row = 6, column = 2, padx = 5, pady = 5)
    save_button.grid(row = 6, column = 3, padx = 5, pady = 5)
    load_button.grid(row = 6, column = 4, padx = 5, pady = 5)
    return

#Do Not Run this SQL Script Yet
def project_searchFunction():
    count = 0
    projectConnector = sqlite3.connect('project_details.db')
    projectCursor = projectConnector.cursor()

    if project_status_Var.get() != "":
        projectCursor.execute("SELECT * from project WHERE statusInfo=?", (project_status_Var.get(),))

        items = projectCursor.fetchall() #Fetches all the particular items based on the query and loaded as a data structure

        table.delete(*table.get_children()) #Deletes all the contents before inserting the values

        for item in items:
            table.insert(parent = '', index = "end", iid = count, text = "", values = item)
            count += 1

    if search_var.get() != "":
            projectCursor.execute("SELECT * from project WHERE identification=?", (search_var.get(),))

            items = projectCursor.fetchall() #Fetches all the particular items based on the query and loaded as a data structure

            table.delete(*table.get_children()) #Deletes all the contents before inserting the values

            for item in items:
                table.insert(parent = '', index = "end", iid = count, text = "", values = item)
                count += 1
    
    projectConnector.commit()
    projectConnector.close()

def project_select_field(): 
    global projectID
    projectID = ""

    projectName_input.delete(0, END) 
    start_date_input.delete(0, END) 
    end_date_input.delete(0, END)
    status_entry_input.delete(0, END) 

    #selecting the record number 
    selected = table.focus() 

    #selecting the value 
    values = table.item(selected, 'values') #Passes 2 different parameters for the item to be selected, the number of records and the text 

    if values == "": 
        messagebox.showwarning("Warning", "No record has been selected.") 

    #Outputting the values to the box 
    else:
        projectID = values[0] 
        projectName_input.insert(0, values[1]) 
        start_date_input.insert(0, values[2]) 
        end_date_input.insert(0, values[3])
        status_entry_input.insert(0, values[4])

def project_update_field(): 
    selected = table.focus()
    values = table.item(selected, text = "", values = (projectID, projectName_input.get(), start_date_input.get(), end_date_input.get(), project_status_Var.get())) 

    projectName_input.delete(0, END) 
    start_date_input.delete(0, END) 
    end_date_input.delete(0, END)
    status_entry_input.delete(0, END)  

    with open(project.practice_project_file, "w", newline = "") as project_file:
        writer = csv.writer(project_file)

        for item_id in table.get_children():
            value = table.item(item_id, 'values')
            writer.writerow(value)

def project_insert_field():
    local_count = len(table.get_children())
    project.inputValues()
    project.project_create_checks()

    if project.checkValidity == True:
        project.Identification()

        table.insert(parent = '', index = "end", iid = local_count, text = "", values = (project.create_project_name, project.startDate, project.endDate, project.status))
        local_count += 1

        projectName_input.delete(0, END) 
        start_date_input.delete(0, END) 
        end_date_input.delete(0, END)
        status_entry_input.delete(0, END) 

def addProject():
    found = False

    if create_project_Var.get() == "" and start_Date_Var.get() == "" and end_Date_Var.get() == "":
        messagebox.showerror("Error!", "All Fields must be filled!")
    
    elif (create_project_Var.get() == "" and start_Date_Var.get() != "" and end_Date_Var.get() != "") or (create_project_Var.get() != "" and start_Date_Var.get() == "" and end_Date_Var.get() != "") or (create_project_Var.get() != "" and start_Date_Var.get() != "" and end_Date_Var.get() == ""):
        messagebox.showerror("Error!", "Only 1 of these fields has been filled!")

    elif (create_project_Var.get() != "" and start_Date_Var.get() == "" and end_Date_Var.get() == "") or (create_project_Var.get() == "" and start_Date_Var.get() != "" and end_Date_Var.get() == "") or (create_project_Var.get() == "" and start_Date_Var.get() == "" and end_Date_Var.get() != ""):
        messagebox.showerror("Error!", "Only 2 of these fields has been filled!")
    
    elif project_status_Var.get() == "":
        messagebox.showerror("Error!", "Please fill in the status")
    
    else:
        project.inputValues()
        project.project_create_checks()

        try:
            file = open(project.practice_project_file, "r")
        
        except FileNotFoundError:
            messagebox.showerror("Error!", "Cannot Open File")
        
        else:
            with open(project.practice_project_file, "r") as find_project_file:
                reader = csv.reader(find_project_file)
                sorted_data = sorted(reader, key=lambda x: x[1])  #Sorts by specific columns like an insertion sort and makes a specific number of shifts wherever necessary
                found = prescence_binary_search(sorted_data, create_project_Var.get())
            
        if found != True and project.checkValidity == True:
            project.Identification()
            project.array()
            project.write_to_file()
            project.sort_fields()

            #Uses Symmetric Encryption with 1 key to be able to Encrypt and Decrypt the File
            project.encryptFile()
            project.decryptFile()
    return

def find_project():
    found = False
    count = 0

    if viewProject_Var.get() == "":
        messagebox.showerror("Error!", "Project Name Cannot be blank!")
    
    else:
        project.inputValues()
        project.project_view_checks()

    if project.checkValidity == True:
        try:
            view_project_file = open(project.practice_project_file, "r")

        except FileNotFoundError:
            messagebox.showerror("Error!", "Cannot Open File")
        
        else:
            with open(project.practice_project_file, "r") as view_project_file:
                reader = csv.reader(view_project_file)
                sorted_data = sorted(reader, key=lambda x: x[1])  #Sorts by specific columns like an insertion sort and makes a specific number of shifts wherever necessary
                found = prescence_binary_search(sorted_data, viewProject_Var.get())

            if count != 1 and found == True:
                messagebox.showinfo("Duplicates!", "Found the Project but found" + " " + str(count) + " " + "duplicates of the same Project")
                table_for_project()
            
            elif count == 1 and found == True:
                messagebox.showinfo("Result!", "Found the Project and No Dupliates")
                table_for_project()
            
            else:
                messagebox.showerror("Error!", "Cannot find Project")
    return

def table_for_project():
    projectTable = ttk.Treeview(viewProject)
    projectTable["columns"] = ("ID", "Task Name", "Start Date", "End Date", "Priority", "Status", "Project Name")
    count = 0

    projectTable.column("#0", width = 0, stretch = NO)
    projectTable.column("ID", width = 100, minwidth = 25, anchor = W)
    projectTable.column("Task Name", width = 100, minwidth = 25, anchor = W)
    projectTable.column("Start Date", width = 100, minwidth = 25, anchor = W)
    projectTable.column("End Date", width = 100, minwidth = 25, anchor = W)
    projectTable.column("Priority", width = 100, minwidth = 25, anchor = W)
    projectTable.column("Status", width = 100, minwidth = 25, anchor = W)
    projectTable.column("Project Name", width = 100, minwidth = 25, anchor = W)

    projectTable.heading("ID", text = "ID")
    projectTable.heading("Task Name", text = "Task Name")
    projectTable.heading("Start Date", text = "Start Date")
    projectTable.heading("End Date", text = "End Date")
    projectTable.heading("Priority", text = "Priority")
    projectTable.heading("Status", text = "Status")
    projectTable.heading("Project Name", text = "Project Name")
    
    try:
        file = open(task.task_details, "r")
    
    except (FileNotFoundError, AttributeError):
        messagebox.showerror("Error!", "Cannot Open File")

    else:
        with open(task.task_details, "r") as task_details:
            reader = csv.reader(task_details)
            for item in reader:
                if viewProject_Var.get() == item[-1]:
                    projectTable.insert(parent = '', index = "end", iid = count, text = "", values = item)
                    count += 1
    
    projectTable.grid(row = 4, column = 0, padx = 5, pady = 5)
    return projectTable

def projectPage():
    global currentWindow, projectWindow, viewProject, create_project_Var, start_Date_Var, end_Date_Var, viewProject_Var, project_status_Var
    projectWindow = Tk()
    projectWindow.title("Proposed Task Management System - Project Page")
    currentWindow = projectWindow
    tab = ttk.Notebook(projectWindow)
    tab.grid(row = 0, column = 0)

    buttonFrame = Frame(projectWindow)
    createProject = Frame(tab, background = "Black")
    viewProject = Frame(tab, background = "Black")
    tab.add(createProject, text = "Create Project")
    tab.add(viewProject, text = "View Project")

    projectHeading = Label(createProject, text = "Project Creation Page", background = "Black", foreground = "White", font = ("Arial", 30, "bold", "underline"))

    project_label = Label(createProject, text = "Enter Project: ", background = "Black", foreground = "White", font = ("Arial", 20, "bold"))
    create_project_Var = StringVar()
    project_name_entry = Entry(createProject, background = "White", width = 30, textvariable = create_project_Var)

    start_date_label = Label(createProject, text = "Enter Start Date: ", background = "Black", foreground = "White", font = ("Arial", 20, "bold"))
    start_Date_Var = StringVar()
    start_date_entry = DateEntry(createProject, width = 30, textvariable = start_Date_Var, date_pattern = "dd/mm/yyyy")

    end_date_label = Label(createProject, text = "Enter End Date: ", background = "Black", foreground = "White", font = ("Arial", 20, "bold"))
    end_Date_Var = StringVar()
    end_date_entry = DateEntry(createProject, width = 30, textvariable = end_Date_Var, date_pattern = "dd/mm/yyyy")

    status_label = Label(createProject, text = "Status", background = "Black", foreground = "White", font = ("Arial", 20, "bold"))
    project_status_Var = StringVar()
    status_Entry = OptionMenu(createProject, project_status_Var, "Completed", "Currently Working", "Incomplete")

    add_project = Button(createProject, text = "Add Project", command = addProject)
    log_out_button = Button(buttonFrame, text = "Log Out", command = logOutScreen)
    taskButton = Button(buttonFrame, text = "Task Screen", command = lambda: transfer_screen(projectWindow, createTaskWindow))
    bankButton = Button(buttonFrame, text = "Archivng Bank Transfer System", command = lambda: transfer_screen(projectWindow, bankPage))
    project_table_button = Button(buttonFrame, text = "Project Details (Do not click this button)", command = lambda: transfer_screen(projectWindow, view_project_details))

    if staff.access == "Senior Manager":
        seniorButton = Button(buttonFrame, text = "Senior Manager Page")
        seniorButton.grid(row = 5, column = 4, padx = 5, pady = 5)
    
    if staff.access == "Auditor":
        auditorButton = Button(buttonFrame, text = "Auditor Page", command = lambda: transfer_screen(projectWindow, auditorPage))
        auditorButton.grid(row = 5, column = 4, padx = 5, pady = 5)

    projectHeading.grid(row = 0, column = 0, padx = 5, pady = 5)

    project_label.grid(row = 1, column = 0, padx = 5, pady = 5)
    project_name_entry.grid(row = 2, column = 0, padx = 5, pady = 5)

    start_date_label.grid(row = 1, column = 1, padx = 5, pady = 5)
    start_date_entry.grid(row = 2, column = 1, padx = 5, pady = 5)

    end_date_label.grid(row = 1, column = 2, padx = 5, pady = 5)
    end_date_entry.grid(row = 2, column = 2, padx = 5, pady = 5)

    status_label.grid(row = 1, column = 3, padx = 5, pady = 5)
    status_Entry.grid(row = 2, column = 3, padx = 5, pady = 5)

    add_project.grid(row = 1, column = 4, padx = 5, pady = 5)

    projectHeading = Label(viewProject, text = "View Project Page", background = "Black", foreground = "White", font = ("Arial", 30, "bold", "underline"))

    project_label = Label(viewProject, text = "Enter Project: ", background = "Black", foreground = "White", font = ("Arial", 20, "bold"))
    viewProject_Var = StringVar()
    viewProject_Entry = Entry(viewProject, background = "White", width = 30, textvariable = viewProject_Var)

    find_project_button = Button(viewProject, width = 30, text = "Find Project", command = find_project)
        
    projectHeading.grid(row = 0, column = 0, padx = 5, pady = 5)

    project_label.grid(row = 1, column = 0, padx = 5, pady = 5)
    viewProject_Entry.grid(row = 2, column = 0, padx = 5, pady = 5)
    find_project_button.grid(row = 3, column = 0, padx = 5, pady = 5)

    buttonFrame.grid(row = 5, column = 0)
    log_out_button.grid(row = 5, column = 0, padx = 5, pady = 5)
    taskButton.grid(row = 5, column = 1, padx = 5, pady = 5)
    bankButton.grid(row = 5, column = 2, padx = 5, pady = 5)
    project_table_button.grid(row = 5, column = 3, padx = 5, pady = 5)
    return projectWindow

def transfer_money(): #The function is used here to control the processes involved within the transferral of money between different users
    if sender_firstName_Var.get() == "" and sender_surname_Var.get() == "" and sender_bankName_Var.get() == "" and sender_ID_Var.get() == "" and receiver_firstName_Var.get() == "" and receiver_surname_Var.get() == "" and receiver_bankName_Var.get() == "" and receiver_ID_Var.get() == "" and transfer_entry.get() == "" and time_Var.get() == "": #Used to check if all specified fields of the page are empty
        messagebox.showerror("Error!", "All Fields must be filled!")
    
    else:
        bank.inputValue() #Inherited method used to take and retrieve all the inputs (uses Encapsulation show the implementation of data being sent and also access the data within the object)
    
    if bank.input_check == True: #Boolean for all input checks
        bank.bank_checks() #Used to perform functional Validation and Verification within each inputted check

        if bank.checkValidity == True and bank.referenceValidity == True: #More methods are specifically executed once all Validation and Verification Checks have been used successfully
            bank.array() #Used to update the array and the bank details
            bank.write_to_file() #Used to write to the file and being able to read from it
            bank.sort_fields()

            #Uses Symmetric Encryption with 1 key to be able to Encrypt and Decrypt the File
            bank.encryptFile()
            bank.decryptFile()
    return

#Do not run this script yet
#Used to run the treeview interface that is used to access the data structure table within the interface and contains all relevant information that is under different columns and fields
def view_bank_details():
    global bank_table
    bank_table = Tk()
    bank_table.title("Proposed Task Management System - Bank Table")

    bankConnector = sqlite3.connect("bank_details.db")
    #The use of the connect method is for creating a database
    #Runs as either in memory (":memory:"), as a file name ("fileName.db") or an empty string

    bankCursor = bankConnector.cursor() #Creates a cursor which is used for manking any commits by creating a database and running such quieries within SQL algorithms and queries
    
    #Types of data used in SQLite3 involves text, integer, real, blob or null *Only write this once to create the table and then either remove or comment it afterwards
    #Creates the bank data table
    # bankCursor.execute("""CREATE TABLE bank (
    #                 sender_first_name text,
    #                 sender_receiver_name text,
    #                 sender_bank_name text,
    #                 receiver_first_name text,
    #                 receiver_receiver_name text,
    #                 receiver_bank_name text,
    #                 amount text,
    #                 date_and_time text
    # )""") #Uses a Doc String by surrounding the query with speech marks
    # bankConnector.commit()

    #Deletes all contents of the data table before inserting new ones in
    bankCursor.execute("DELETE from bank")
    bankConnector.commit()

    #Inserts the specific queries within the file
    with open(bank.practice_bank_file, "r") as file:
        reader = csv.reader(file)
        for item in reader: 
            bankCursor.execute("INSERT into bank VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7])) #Iterative approach to insert specific fields into the file, uses ? as place holder and a tuple of values
            bankConnector.commit()
    bankConnector.close()

    table = ttk.Treeview(bank_table)
    table["columns"] = ("Sender First Name", "Sender Surname", "Sender Bank Details", "Receiver First Name", "Receiver Surname", "Receiver Bank Details", "Amount Transferred", "Date and Time")
    columns = ("Sender First Name", "Sender Surname", "Sender Bank Details", "Receiver First Name", "Receiver Surname", "Receiver Bank Details", "Amount Transferred", "Date and Time")
    bankData = []

    #Creates the icons under frames, labels and buttons to be able to display onto the treeview interface
    bank_table_frame = Frame(bank_table)
    buttonFrame = Frame(bank_table)

    transitionWrapper = LabelFrame(buttonFrame, text = "Transitions!")
    bank_button = Button(transitionWrapper, text = "Bank Page", command = lambda: transfer_screen(bank_table, bankPage)) #Used as a button for the user to be able to shift from the bank table page to the bank GUI page

    #Creates and justifies the contents of the columns within the table
    table.column("#0", width = 0, stretch = NO)
    table.column("Sender First Name", width = 100, minwidth = 25, anchor = W)
    table.column("Sender Surname", width = 100, minwidth = 25, anchor = W)
    table.column("Sender Bank Details", width = 100, minwidth = 25, anchor = W)
    table.column("Receiver First Name", width = 100, minwidth = 25, anchor = W)
    table.column("Receiver Surname", width = 100, minwidth = 25, anchor = W)
    table.column("Receiver Bank Details", width = 100, minwidth = 25, anchor = W)
    table.column("Amount Transferred", width = 100, minwidth = 25, anchor = W)
    table.column("Date and Time", width = 100, minwidth = 25, anchor = W)

    #Creates the headings based on the column of teh table
    #table.heading("ID", text = "Transaction ID")
    table.heading("Sender First Name", text = "Sender First Name")
    table.heading("Sender Surname", text = "Sender Surname")
    table.heading("Sender Bank Details", text = "Sender Bank Details")
    table.heading("Receiver First Name", text = "Receiver First Name")
    table.heading("Receiver Surname", text = "Receiver Surname")
    table.heading("Receiver Bank Details", text = "Receiver Bank Details")
    table.heading("Amount Transferred", text = "Amount Transferred")
    table.heading("Date and Time", text = "Date and Time")

    #Exception Handling used to open the file to input and write all the contents of the file into the specified columns and fields of the treeview table
    try:
        file = open(bank.practice_bank_file, "r")
    
    except (FileNotFoundError, AttributeError):
        messagebox.showerror("Error", "Cannot open File")
    
    else:
        with open(bank.practice_bank_file, "r") as file:
            count = 0
            reader = csv.reader(file) #Sets a reader for the CSV File
            for item in reader:
                table.insert(parent = '', index = "end", iid = count, text = "", values = (item[0], item[1], item[2], item[4], item[5], item[6], item[8], item[9])) #Inputs each indexed and specified field into the treeview
                bankData.append(item)
                count += 1

            for column in columns:
                table.heading(column, text=column, command=lambda c=column: on_sort(c, table)) #Sorts the columns based on the headings that are used to sort the data table

    #Places the icons of the GUI interface into a position with grid (specifying the grid rows and columns)
    table.grid(row = 0, column = 0, padx = 10, pady = 10)
    bank_table_frame.grid(row = 1, column = 0, padx = 10, pady = 10)

    transitionWrapper.grid(row = 2, column = 0, padx = 10, pady = 10)
    buttonFrame.grid(row = 2, column = 0, padx = 10, pady = 10)
    bank_button.grid(row = 2, column = 1, padx = 10, pady = 10)
    return bank_table

def bank_binary_search(data, target_sender_ID, target_receiver_ID): #Binary Search used to find the IDs
    start, end = 0, len(data) - 1

    while start <= end:
        mid = (start + end) // 2
        current = data[mid]

        if (target_sender_ID == current[0] or target_sender_ID == "unknown") and (target_receiver_ID == current[0] or target_receiver_ID == "unknown"):
            return True  #finds the access level

        elif target_sender_ID < current[0] or (target_sender_ID == current[0] and target_receiver_ID < current[0]):
            end = mid - 1

        else:
            start = mid + 1

    return False  #Returns when the ID isn't found

def bankPage():
    #Globalised Variables
    global currentWindow, bankWindow, sender_firstName_Var, sender_surname_Var, sender_bankName_Var, sender_ID_Var, receiver_firstName_Var, receiver_surname_Var, receiver_bankName_Var, receiver_ID_Var, transfer_entry, date_Var, time_Var
    bankWindow = Tk() #Creates the window with the Tkinter Module with a specific title
    bankWindow.title("Proposed Task Management System - Archiving Bank Transfer Page")
    currentWindow = bankWindow

    #Creates different frames for the buttons and the interface
    bankFrame = Frame(bankWindow, background = "Black")
    buttonFrame = Frame(bankWindow)

    heading = Label(bankFrame, background = "Black", foreground = "White", text = "Archiving Bank Transfer Page", font = ("Arial", 20, "bold", "underline"))

    #Each label is being created with a string text variable and specific attributes that are provided within the interface
    sender_heading = Label(bankFrame, background = "Black", foreground = "White", text = "Sender Details", font = ("Arial", 20, "bold", "underline"))
    sender_firstName = Label(bankFrame, background = "Black", foreground = "White", text = "First Name: ", font = ("Arial", 20, "bold"))
    sender_firstName_Var = StringVar()
    sender_firstName_entry = Entry(bankFrame, width = 30, textvariable = sender_firstName_Var)

    sender_surname = Label(bankFrame, background = "Black", foreground = "White", text = "Surname: ", font = ("Arial", 20, "bold"))
    sender_surname_Var = StringVar()
    sender_surname_entry = Entry(bankFrame, width = 30, textvariable = sender_surname_Var)

    sender_bank_name = Label(bankFrame, background = "Black", foreground = "White", text = "Enter Bank Name: ", font = ("Arial", 20, "bold"))
    sender_bankName_Var = StringVar()
    sender_bankName_entry = Entry(bankFrame, width = 30, textvariable = sender_bankName_Var)

    sender_ID = Label(bankFrame, background = "Black", foreground = "White", text = "Payment Reference (ID Number): ", font = ("Arial", 20, "bold"))
    sender_ID_Var = StringVar()
    sender_ID_entry = Entry(bankFrame, width = 30, textvariable = sender_ID_Var)

    receiver_heading = Label(bankFrame, background = "Black", foreground = "White", text = "Receiver Details", font = ("Arial", 20, "bold", "underline"))
    
    receiver_firstName = Label(bankFrame, background = "Black", foreground = "White", text = "First Name: ", font = ("Arial", 20, "bold"))
    receiver_firstName_Var = StringVar()
    receiver_firstName_entry = Entry(bankFrame, width = 30, textvariable = receiver_firstName_Var)

    receiver_surname = Label(bankFrame, background = "Black", foreground = "White", text = "Surname: ", font = ("Arial", 20, "bold"))
    receiver_surname_Var = StringVar()
    receiver_surname_entry = Entry(bankFrame, width = 30, textvariable = receiver_surname_Var)

    receiver_bank_name = Label(bankFrame, background = "Black", foreground = "White", text = "Enter Bank Name: ", font = ("Arial", 20, "bold"))
    receiver_bankName_Var = StringVar()
    receiver_bankName_entry = Entry(bankFrame, width = 30, textvariable = receiver_bankName_Var)

    receiver_ID = Label(bankFrame, background = "Black", foreground = "White", text = "Payment Reference (ID Number): ", font = ("Arial", 20, "bold"))
    receiver_ID_Var = StringVar()
    receiver_ID_entry = Entry(bankFrame, width = 30, textvariable = receiver_ID_Var)

    transfer_label = Label(bankFrame, background = "Black", foreground = "White", text = "Transfer Amount: ", font = ("Arial", 20, "bold"))
    transfer_entry = Entry(bankFrame, width = 30)

    date_and_time_label = Label(bankFrame, background = "Black", foreground = "White", text = "Date and Time of Transfer: ", font = ("Arial", 20, "bold"))
    date_Var = StringVar()
    date_entry = DateEntry(bankFrame, width = 30, textvariable = date_Var, date_pattern = "dd/mm/yyyy")

    time_Var = StringVar()
    time_entry = Entry(bankFrame, width = 30, textvariable = time_Var)

    #Buttons that are placed onto the button frame and onto the interface
    transfer_button = Button(bankFrame, background = "Blue", foreground = "Yellow", text = "Transfer", command = transfer_money)
    log_out_button = Button(buttonFrame, text = "Log Out", command = logOutScreen)
    taskButton = Button(buttonFrame,  text = "Task Screen", command = lambda: transfer_screen(bankWindow, createTaskWindow))
    projectButton = Button(buttonFrame, text = "Project Screen", command = lambda: transfer_screen(bankWindow, projectPage))
    bank_table_button = Button(buttonFrame, text = "Bank Details (Do not click this button)", command = lambda: transfer_screen(bankWindow, view_bank_details))

    if staff.access == "Senior Manager":
        seniorButton = Button(buttonFrame, text = "Senior Manager Page")
        seniorButton.grid(row = 10, column = 4, padx = 5, pady = 5)

    if staff.access == "Auditor":
        auditorButton = Button(buttonFrame, text = "Auditor Page", command = lambda: transfer_screen(bankWindow, auditorPage))
        auditorButton.grid(row = 10, column = 4, padx = 5, pady = 5)

    #Places all the icons in its specified position with the use of grid (specifying the grid positions of row and column)
    bankFrame.grid(row = 0, column = 0)
    heading.grid(row = 0, column = 1, padx = 5, pady = 5)

    sender_heading.grid(row = 1, column = 0, padx = 5, pady = 5)
    sender_firstName.grid(row = 2, column = 0, padx = 5, pady = 5)
    sender_firstName_entry.grid(row = 3, column = 0, padx = 5, pady = 5)

    sender_surname.grid(row = 4, column = 0, padx = 5, pady = 5)
    sender_surname_entry.grid(row = 5, column = 0, padx = 5, pady = 5)

    sender_bank_name.grid(row = 6, column = 0, padx = 5, pady = 5)
    sender_bankName_entry.grid(row = 7, column = 0, padx = 5, pady = 5)

    sender_ID.grid(row = 8, column = 0, padx = 5, pady = 5)
    sender_ID_entry.grid(row = 9, column = 0, padx = 5, pady = 5)

    receiver_heading.grid(row = 1, column = 2, padx = 5, pady = 5)
    receiver_firstName.grid(row = 2, column = 2, padx = 5, pady = 5)
    receiver_firstName_entry.grid(row = 3, column = 2, padx = 5, pady = 5)

    receiver_surname.grid(row = 4, column = 2, padx = 5, pady = 5)
    receiver_surname_entry.grid(row = 5, column = 2, padx = 5, pady = 5)

    receiver_bank_name.grid(row = 6, column = 2, padx = 5, pady = 5)
    receiver_bankName_entry.grid(row = 7, column = 2, padx = 5, pady = 5)

    receiver_ID.grid(row = 8, column = 2, padx = 5, pady = 5)
    receiver_ID_entry.grid(row = 9, column = 2, padx = 5, pady = 5)

    transfer_label.grid(row = 3, column = 1, padx = 5, pady = 5)
    transfer_entry.grid(row = 4, column = 1, padx = 5, pady = 5)
    transfer_button.grid(row = 9, column = 1, padx = 5, pady = 5)

    date_and_time_label.grid(row = 6, column = 1, padx = 5, pady = 5)
    date_entry.grid(row = 7, column = 1, padx = 5, pady = 5)
    time_entry.grid(row = 8, column = 1, padx = 5, pady = 5)

    buttonFrame.grid(row = 10, column = 0)
    log_out_button.grid(row = 10, column = 0, padx = 5, pady = 5)
    taskButton.grid(row = 10, column = 1, padx = 5, pady = 5)
    projectButton.grid(row = 10, column = 2, padx = 5, pady = 5)
    bank_table_button.grid(row = 10, column = 3, padx = 5, pady = 5)
    return bankWindow #Returns the window to the user

def seniorManagerPage():
    global seniorWindow, currentWindow

    seniorWindow = Tk()
    seniorWindow.title("Task Management System - Senior Manager Page")
    currentWindow = seniorWindow

    seniorFrame = Frame(seniorWindow, background = "Black")
    buttonFrame = Frame(seniorWindow)
    heading = Label(seniorFrame, text = "Senior Manager Page", background = "Black", foreground = "White", font = ("Arial", 40, "bold", "underline"))
    log_out_button = Button(buttonFrame, text = "Log Out", command = logOutScreen)

    accountLabel = Label(seniorFrame, text = "Click this button to view the account details", font = ("Arial", 10, "bold"))
    accountButton = Button(seniorFrame, text = "View Account Details", command = lambda: transfer_screen(seniorWindow, view_employee_details))
    taskLabel = Label(seniorFrame, text = "Click this button to view the task details", font = ("Arial", 10, "bold"))
    taskButton = Button(seniorFrame, text = "View Task Details", command = lambda: transfer_screen(seniorWindow, view_task_details))

    seniorFrame.grid(row = 0, column = 0)
    heading.grid(row = 0, column = 0)
    accountLabel.grid(row = 1, column = 0)
    accountButton.grid(row = 2, column = 0)
    taskLabel.grid(row = 3, column = 0)
    taskButton.grid(row = 4, column = 0)

    buttonFrame.grid(row = 5, column = 0)
    log_out_button.grid(row = 5, column = 0)

    return seniorWindow

def save():
    global ID_Create

    auditor_firstname = firstnameVar.get()
    auditor_surname = surnameVar.get()

    if auditor_firstname != auditor.firstName and auditor_surname != auditor.surname:
        auditor.firstName = auditor_firstname
        auditor.surname = auditor_surname
    
    else:
        pass

    ID_Create = staff.ID
    auditor.get_variables()
    auditor.text_checks()

    if auditor.check == True:
        with open("auditor.txt", "a") as auditorFile:
            auditorFile.write(ID_Create + " " + auditor_firstname + " " + auditor_surname + " " + text.get("1.0", END))
    return

def clear():
    text.delete("1.0", END)
    return

def auditorPage():
    global text, currentWindow, auditorWindow

    auditorWindow = Tk()
    auditorWindow.title("Task Management System - Auditor Page")
    currentWindow = auditorWindow

    frame = Frame(auditorWindow, background = "Black")
    heading = Label(frame, text = "Auditor Textbox Page", background = "Black", foreground = "White", font = ("Arial", 40, "bold", "underline"))
    message = Label(frame, text = "This is just a textbox for you to practice your writing before submitting.", background = "Black", foreground = "White", font = ("Arial", 10, "bold"))
    save_message = Label(frame, text = "Remember to save all contents in this textbox before closing this screen", background = "Black", foreground = "White", font = ("Arial", 10, "bold"))
    buttonFrame = Frame(auditorWindow)
    text = Text(frame)

    log_out_button = Button(buttonFrame, text = "Log Out", command = logOutScreen)
    saveButton = Button(buttonFrame, text = "Save", command = save)
    save_as_button = Button(buttonFrame, text = "Save As", command = auditor.save_file)
    clearButton = Button(buttonFrame, text = "Clear", command = clear)
    loadButton = Button(buttonFrame, text = "Load", command = auditor.open_file)
    taskButton = Button(buttonFrame, text = "Task Page", command = lambda: transfer_screen(auditorWindow, createTaskWindow))
    bankButton = Button(buttonFrame, text = "Archiving Bank Transfer Page", command = lambda: transfer_screen(auditorWindow, bankPage))
    projectButton = Button(buttonFrame, text = "Project Screen", command = lambda: transfer_screen(auditorWindow, projectPage))

    frame.grid(row = 0, column = 0, padx = 10, pady = 10)
    heading.grid(row = 1, column = 0, padx = 10, pady = 10)
    message.grid(row = 2, column = 0, padx = 10, pady = 10)
    save_message.grid(row = 3, column = 0, padx = 10, pady = 10)
    text.grid(row = 4, column = 0, padx = 10, pady = 10)
    buttonFrame.grid(row = 5, column = 0, padx = 10, pady = 10)
    log_out_button.grid(row = 5, column = 0, padx = 10, pady = 10)
    saveButton.grid(row = 5, column = 1, padx = 10, pady = 10)
    save_as_button.grid(row = 5, column = 2, padx = 10, pady = 10)
    clearButton.grid(row = 5, column = 3, padx = 10, pady = 10)
    loadButton.grid(row = 5, column = 4, padx = 10, pady = 10)
    taskButton.grid(row = 5, column = 5, padx = 10, pady = 10)
    bankButton.grid(row = 5, column = 6, padx = 10, pady = 10)
    projectButton.grid(row = 5, column = 7, padx = 10, pady = 10)
    return auditorWindow

accountWindow = makeAccountwindow()
accountWindow.mainloop()