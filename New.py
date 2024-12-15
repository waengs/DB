import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from tkinter import simpledialog
from datetime import datetime

# Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",       # Replace with your database host
        user="root",            # Replace with your MySQL username
        password="Miao67893",   # Password for MySQL
        database="NEWDB"        # Database name
    )

# Main App Class
class GymManaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GymMana")
        self.root.geometry("1000x800")
        self.username = None
        self.create_welcome_page()

    def create_welcome_page(self):
        """ Creates the welcome page with buttons for different user types """
        self.clear_frame()

        label = tk.Label(self.root, text="Welcome to GymMana", font=("Arial", 16))
        label.pack(pady=20)

        btn_register = tk.Button(self.root, text="Register as New User", command=self.create_register_page)
        btn_register.pack(pady=5)

        btn_sign_in_user = tk.Button(self.root, text="Sign In as User", command=self.create_user_sign_in_page)
        btn_sign_in_user.pack(pady=5)

        btn_sign_in_admin = tk.Button(self.root, text="Sign In as Admin", command=self.create_admin_sign_in_page)
        btn_sign_in_admin.pack(pady=5)

        btn_sign_in_trainer = tk.Button(self.root, text="Sign In as Trainer", command=self.create_trainer_sign_in_page)
        btn_sign_in_trainer.pack(pady=5)

        btn_sign_in_technician = tk.Button(self.root, text="Sign In as Technician", command=self.create_technician_sign_in_page)
        btn_sign_in_technician.pack(pady=5)

    def create_register_page(self):
        """ Creates the registration page for new users """
        self.clear_frame()
        
        label = tk.Label(self.root, text="Let’s Register", font=("Arial", 16))
        label.pack(pady=20)
        
        self.username_entry = self.create_form_field("Username")
        self.password_entry = self.create_form_field("Password")
        self.email_entry = self.create_form_field("Email")
        self.full_name_entry = self.create_form_field("Full Name")
        self.phone_entry = self.create_form_field("Phone Number")

        submit_button = tk.Button(self.root, text="Submit", command=self.submit_registration)
        submit_button.pack(pady=20)

    def create_form_field(self, label_text):
        """ Helper function to create form fields for registration """
        label = tk.Label(self.root, text=label_text)
        label.pack(pady=5)
        entry = tk.Entry(self.root)
        entry.pack(pady=5)
        return entry

    def submit_registration(self):
        """ Handles the registration submission """
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()
        full_name = self.full_name_entry.get()
        phone_number = self.phone_entry.get()

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if username already exists
        cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
        if cursor.fetchone():
            messagebox.showerror("Error", "Username already exists.")
            conn.close()
        else:
            # Insert new user into the database
            cursor.execute("""
                INSERT INTO Users (username, password, email, full_name, phone_number) 
                VALUES (%s, %s, %s, %s, %s)
            """, (username, password, email, full_name, phone_number))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful!")
            conn.close()
            self.create_welcome_page()

    def create_admin_sign_in_page(self):
        """ Create the Admin Sign-In Page """
        self.clear_frame()

        label = tk.Label(self.root, text="Admin Sign-In", font=("Arial", 16))
        label.pack(pady=20)

        username_label = tk.Label(self.root, text="Username")
        username_label.pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack(pady=5)

        password_label = tk.Label(self.root, text="Password")
        password_label.pack()
        password_entry = tk.Entry(self.root, show="*")  # hide password input
        password_entry.pack(pady=5)

        def admin_sign_in():
            username = username_entry.get()
            password = password_entry.get()

            # Validate admin credentials (username and password)
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Admins WHERE username = %s AND password = %s", (username, password))
            admin_data = cursor.fetchone()
            conn.close()

            if admin_data:
                self.admin_id = admin_data[0]  # Store admin ID
                self.create_admin_welcome_page(admin_data)
            else:
                messagebox.showerror("Error", "Invalid username or password.")

        sign_in_button = tk.Button(self.root, text="Sign In", command=admin_sign_in)
        sign_in_button.pack(pady=10)

        back_button = tk.Button(self.root, text="Back", command=self.create_welcome_page)
        back_button.pack(pady=5)

    def create_admin_welcome_page(self, admin_data):
        """ Create the Admin Welcome Page """
        self.clear_frame()

        # Admin Welcome Message
        label = tk.Label(self.root, text=f"Welcome Admin: {admin_data[1]}", font=("Arial", 16))
        label.pack(pady=20)

        # Section for Trainers
        trainers_label = tk.Label(self.root, text="List of Trainers", font=("Arial", 16))
        trainers_label.pack(pady=10)

        trainers_button = tk.Button(self.root, text="Manage Trainers", command=self.manage_trainers)
        trainers_button.pack(pady=5)

        # Section for Technicians
        technicians_label = tk.Label(self.root, text="List of Technicians", font=("Arial", 16))
        technicians_label.pack(pady=10)

        technicians_button = tk.Button(self.root, text="Manage Technicians", command=self.manage_technicians)
        technicians_button.pack(pady=5)

        # Section for Promotions
        promotions_label = tk.Label(self.root, text="List of Promotions", font=("Arial", 16))
        promotions_label.pack(pady=10)

        promotions_button = tk.Button(self.root, text="Manage Promotions", command=self.manage_promotions)
        promotions_button.pack(pady=5)

        # Section for Equipment
        equipment_label = tk.Label(self.root, text="List of Equipment", font=("Arial", 16))
        equipment_label.pack(pady=10)

        equipment_button = tk.Button(self.root, text="Manage Equipment", command=self.manage_equipment)
        equipment_button.pack(pady=5)

        # Log Out Button
        back_button = tk.Button(self.root, text="Log Out", command=self.create_welcome_page)
        back_button.pack(pady=20)

    def manage_trainers(self):
        """ Page to manage trainers (Add, Delete, Edit) """
        self.clear_frame()

        # Fetch all trainers from the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT trainer_id, full_name, year_started, specialty, phone_number, email FROM Trainers")
        trainers = cursor.fetchall()
        conn.close()

        # List of trainers
        label = tk.Label(self.root, text="Manage Trainers", font=("Arial", 16))
        label.pack(pady=20)

        for trainer in trainers:
            trainer_id, full_name, year_started, specialty, phone_number, email = trainer

            trainer_frame = tk.Frame(self.root)
            trainer_frame.pack(pady=5, fill="x")

            trainer_label = tk.Label(trainer_frame, text=f"{full_name} ({email}, {specialty}, {year_started})", font=("Arial", 12))
            trainer_label.pack(side="left", padx=10)

            # Add/Delete Buttons
            delete_button = tk.Button(trainer_frame, text="Delete", command=lambda t_id=trainer_id: self.delete_trainer(t_id))
            delete_button.pack(side="left", padx=5)

        add_trainer_button = tk.Button(self.root, text="Add New Trainer", command=self.add_trainer)
        add_trainer_button.pack(pady=10)

       # Create a back button to navigate to the admin welcome page
        back_button = tk.Button(self.root, text="Back", command=self.create_welcome_page)  # Do not call the function here
        back_button.pack(pady=5)


    def add_trainer(self):
        """ Page to add a new trainer """
        self.clear_frame()

        label = tk.Label(self.root, text="Add New Trainer", font=("Arial", 16))
        label.pack(pady=20)

        # Trainer details fields
        full_name_label = tk.Label(self.root, text="Full Name")
        full_name_label.pack()
        full_name_entry = tk.Entry(self.root)
        full_name_entry.pack(pady=5)

        year_started_label = tk.Label(self.root, text="Year Started")
        year_started_label.pack()
        year_started_entry = tk.Entry(self.root)
        year_started_entry.pack(pady=5)

        specialty_label = tk.Label(self.root, text="Specialty")
        specialty_label.pack()
        specialty_entry = tk.Entry(self.root)
        specialty_entry.pack(pady=5)

        phone_number_label = tk.Label(self.root, text="Phone Number")
        phone_number_label.pack()
        phone_number_entry = tk.Entry(self.root)
        phone_number_entry.pack(pady=5)

        email_label = tk.Label(self.root, text="Email")
        email_label.pack()
        email_entry = tk.Entry(self.root)
        email_entry.pack(pady=5)

        def save_trainer():
            full_name = full_name_entry.get()
            year_started = year_started_entry.get()
            specialty = specialty_entry.get()
            phone_number = phone_number_entry.get()
            email = email_entry.get()

            # Insert trainer into the database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Trainers (full_name, year_started, specialty, phone_number, email) 
                VALUES (%s, %s, %s, %s, %s)
            """, (full_name, year_started, specialty, phone_number, email))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Trainer added successfully!")
            self.manage_trainers()

        save_button = tk.Button(self.root, text="Save", command=save_trainer)
        save_button.pack(pady=10)

        cancel_button = tk.Button(self.root, text="Cancel", command=self.manage_trainers)
        cancel_button.pack(pady=5)

    def delete_trainer(self, trainer_id):
        """ Delete a trainer """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Trainers WHERE trainer_id = %s", (trainer_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Trainer deleted successfully!")
        self.manage_trainers()

    def manage_technicians(self):
        """ Page to manage technicians (Add, Delete, Edit) """
        self.clear_frame()

        # Fetch all technicians from the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT technician_id, full_name, specialty, phone_number, email FROM Technicians")
        technicians = cursor.fetchall()
        conn.close()

        # List of technicians
        label = tk.Label(self.root, text="Manage Technicians", font=("Arial", 16))
        label.pack(pady=20)

        for technician in technicians:
            technician_id, full_name, specialty, phone_number, email = technician

            technician_frame = tk.Frame(self.root)
            technician_frame.pack(pady=5, fill="x")

            technician_label = tk.Label(technician_frame, text=f"{full_name} ({email}, {specialty})", font=("Arial", 12))
            technician_label.pack(side="left", padx=10)

            # Add/Delete Buttons
            delete_button = tk.Button(technician_frame, text="Delete", command=lambda t_id=technician_id: self.delete_technician(t_id))
            delete_button.pack(side="left", padx=5)

        add_technician_button = tk.Button(self.root, text="Add New Technician", command=self.add_technician)
        add_technician_button.pack(pady=10)

        back_button = tk.Button(self.root, text="Back", command=self.create_welcome_page)  # Do not call the function here
        back_button.pack(pady=5)

    def add_technician(self):
        """ Page to add a new technician """
        self.clear_frame()

        label = tk.Label(self.root, text="Add New Technician", font=("Arial", 16))
        label.pack(pady=20)

        # Technician details fields
        full_name_label = tk.Label(self.root, text="Full Name")
        full_name_label.pack()
        full_name_entry = tk.Entry(self.root)
        full_name_entry.pack(pady=5)

        specialty_label = tk.Label(self.root, text="Specialty")
        specialty_label.pack()
        specialty_entry = tk.Entry(self.root)
        specialty_entry.pack(pady=5)

        phone_number_label = tk.Label(self.root, text="Phone Number")
        phone_number_label.pack()
        phone_number_entry = tk.Entry(self.root)
        phone_number_entry.pack(pady=5)

        email_label = tk.Label(self.root, text="Email")
        email_label.pack()
        email_entry = tk.Entry(self.root)
        email_entry.pack(pady=5)

        def save_technician():
            full_name = full_name_entry.get()
            specialty = specialty_entry.get()
            phone_number = phone_number_entry.get()
            email = email_entry.get()

            # Insert technician into the database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Technicians (full_name, specialty, phone_number, email) 
                VALUES (%s, %s, %s, %s)
            """, (full_name, specialty, phone_number, email))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Technician added successfully!")
            self.manage_technicians()

        save_button = tk.Button(self.root, text="Save", command=save_technician)
        save_button.pack(pady=10)

        cancel_button = tk.Button(self.root, text="Cancel", command=self.manage_technicians)
        cancel_button.pack(pady=5)

    def delete_technician(self, technician_id):
        """ Delete a technician """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Technicians WHERE technician_id = %s", (technician_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Technician deleted successfully!")
        self.manage_technicians()

    def manage_promotions(self):
        """ Page to manage promotions (Add, Delete, Edit) """
        self.clear_frame()

        # Fetch all promotions from the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT promo_id, promo_code, discount_percentage, start_date, end_date, is_active FROM Promotions")
        promotions = cursor.fetchall()
        conn.close()

        # List of promotions
        label = tk.Label(self.root, text="Manage Promotions", font=("Arial", 16))
        label.pack(pady=20)

        for promo in promotions:
            promo_id, promo_code, discount_percentage, start_date, end_date, is_active = promo

            promo_frame = tk.Frame(self.root)
            promo_frame.pack(pady=5, fill="x")

            promo_label = tk.Label(promo_frame, text=f"{promo_code} ({discount_percentage}% off, {start_date} to {end_date})", font=("Arial", 12))
            promo_label.pack(side="left", padx=10)

            # Edit and Delete Buttons
            delete_button = tk.Button(promo_frame, text="Delete", command=lambda p_id=promo_id: self.delete_promotion(p_id))
            delete_button.pack(side="left", padx=5)

        add_promo_button = tk.Button(self.root, text="Add New Promotion", command=self.add_promotion)
        add_promo_button.pack(pady=10)

        back_button = tk.Button(self.root, text="Back", command=self.create_welcome_page)  # Do not call the function here
        back_button.pack(pady=5)

    def add_promotion(self):
        """ Page to add a new promotion """
        self.clear_frame()

        label = tk.Label(self.root, text="Add New Promotion", font=("Arial", 16))
        label.pack(pady=20)

        # Promotion details fields
        promo_code_label = tk.Label(self.root, text="Promo Code")
        promo_code_label.pack()
        promo_code_entry = tk.Entry(self.root)
        promo_code_entry.pack(pady=5)

        discount_percentage_label = tk.Label(self.root, text="Discount Percentage")
        discount_percentage_label.pack()
        discount_percentage_entry = tk.Entry(self.root)
        discount_percentage_entry.pack(pady=5)

        start_date_label = tk.Label(self.root, text="Start Date (YYYY-MM-DD)")
        start_date_label.pack()
        start_date_entry = tk.Entry(self.root)
        start_date_entry.pack(pady=5)

        end_date_label = tk.Label(self.root, text="End Date (YYYY-MM-DD)")
        end_date_label.pack()
        end_date_entry = tk.Entry(self.root)
        end_date_entry.pack(pady=5)

        def save_promotion():
            promo_code = promo_code_entry.get()
            discount_percentage = discount_percentage_entry.get()
            start_date = start_date_entry.get()
            end_date = end_date_entry.get()

            # Insert promotion into the database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Promotions (promo_code, discount_percentage, start_date, end_date) 
                VALUES (%s, %s, %s, %s)
            """, (promo_code, discount_percentage, start_date, end_date))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Promotion added successfully!")
            self.manage_promotions()

        save_button = tk.Button(self.root, text="Save", command=save_promotion)
        save_button.pack(pady=10)

        cancel_button = tk.Button(self.root, text="Cancel", command=self.manage_promotions)
        cancel_button.pack(pady=5)

    def delete_promotion(self, promo_id):
        """ Delete a promotion """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Promotions WHERE promo_id = %s", (promo_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Promotion deleted successfully!")
        self.manage_promotions()

    def manage_equipment(self):
        """ Page to manage equipment (Add, View) """
        self.clear_frame()

        # Fetch all equipment from the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT equipment_id, equipment_name, equipment_status, purchase_date FROM Equipment")
        equipment_list = cursor.fetchall()
        conn.close()

        # Page Title
        label = tk.Label(self.root, text="Manage Equipment", font=("Arial", 16))
        label.pack(pady=20)

        # Display equipment details
        if equipment_list:
            for equipment in equipment_list:
                equipment_id, equipment_name, equipment_status, purchase_date = equipment

                equipment_frame = tk.Frame(self.root)
                equipment_frame.pack(pady=5, fill="x")

                equipment_label = tk.Label(equipment_frame, text=f"{equipment_name} ({equipment_status}) - Purchased on {purchase_date}", font=("Arial", 12))
                equipment_label.pack(side="left", padx=10)

                delete_button = tk.Button(equipment_frame, text="Delete", bg="red", fg="white",
                                        command=lambda e_id=equipment_id: self.delete_equipment(e_id))
                delete_button.pack(side="right", padx=10)
        else:
            no_equipment_label = tk.Label(self.root, text="No equipment found.", font=("Arial", 12))
            no_equipment_label.pack(pady=10)

        # Add Equipment Button
        add_button = tk.Button(self.root, text="Add New Equipment", command=self.add_equipment)
        add_button.pack(pady=20)

        back_button = tk.Button(self.root, text="Back", command=self.create_welcome_page)  # Do not call the function here
        back_button.pack(pady=5)


    def add_equipment(self):
        """ Page to add new equipment """
        self.clear_frame()

        # Page Title
        label = tk.Label(self.root, text="Add New Equipment", font=("Arial", 16))
        label.pack(pady=20)

        # Equipment Details Fields
        name_label = tk.Label(self.root, text="Equipment Name")
        name_label.pack()
        name_entry = tk.Entry(self.root)
        name_entry.pack(pady=5)

        status_label = tk.Label(self.root, text="Equipment Status")
        status_label.pack()
        status_options = ["Available", "In Use", "Under Maintenance"]
        status_var = tk.StringVar(self.root)
        status_var.set(status_options[0])  # Default value
        status_menu = tk.OptionMenu(self.root, status_var, *status_options)
        status_menu.pack(pady=5)

        purchase_date_label = tk.Label(self.root, text="Purchase Date (YYYY-MM-DD)")
        purchase_date_label.pack()
        purchase_date_entry = tk.Entry(self.root)
        purchase_date_entry.pack(pady=5)

        # Save Equipment Button
        def save_equipment():
            equipment_name = name_entry.get()
            equipment_status = status_var.get()
            purchase_date = purchase_date_entry.get()

            # Insert equipment into the database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Equipment (equipment_name, equipment_status, purchase_date)
                VALUES (%s, %s, %s)
            """, (equipment_name, equipment_status, purchase_date))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Equipment added successfully!")
            self.manage_equipment()

        save_button = tk.Button(self.root, text="Save Equipment", command=save_equipment)
        save_button.pack(pady=10)

        # Cancel Button
        cancel_button = tk.Button(self.root, text="Cancel", command=self.manage_equipment)
        cancel_button.pack(pady=5)


    def delete_equipment(self, equipment_id):
        """ Delete an equipment """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Equipment WHERE equipment_id = %s", (equipment_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Equipment deleted successfully!")
        self.manage_equipment()


    def create_technician_sign_in_page(self):
        self.clear_frame()

        label = tk.Label(self.root, text="Technician Sign-In", font=("Arial", 16))
        label.pack(pady=20)

        full_name_label = tk.Label(self.root, text="Full Name")
        full_name_label.pack()
        full_name_entry = tk.Entry(self.root)
        full_name_entry.pack(pady=5)

        email_label = tk.Label(self.root, text="Email")
        email_label.pack()
        email_entry = tk.Entry(self.root)
        email_entry.pack(pady=5)

        def technician_sign_in():
            full_name = full_name_entry.get()
            email = email_entry.get()

            # Validate technician credentials
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT technician_id, full_name, email, phone_number FROM Technicians WHERE full_name = %s AND email = %s", (full_name, email))
            technician_data = cursor.fetchone()
            conn.close()

            if technician_data:
                self.technician_id = technician_data[0]  # Store technician ID (first column returned)
                self.create_technician_welcome_page(technician_data)
            else:
                messagebox.showerror("Error", "Invalid full name or email.")

        sign_in_button = tk.Button(self.root, text="Sign In", command=technician_sign_in)
        sign_in_button.pack(pady=10)

        back_button = tk.Button(self.root, text="Back", command=self.create_welcome_page)
        back_button.pack(pady=5)

    def create_technician_welcome_page(self, technician_data):
        if technician_data is None:
            messagebox.showerror("Error", "Technician data not found.")
            return

        # Fetch technician details (if needed for further use)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Technicians WHERE full_name = %s AND email = %s", (technician_data[1], technician_data[2]))
        technician_data = cursor.fetchone()
        conn.close()

        self.clear_frame()

        # Welcome message
        label = tk.Label(self.root, text=f"Welcome {technician_data[1]}", font=("Arial", 16))
        label.pack(pady=20)

        # Equipment Section
        equipment_label = tk.Label(self.root, text="Available Equipment", font=("Arial", 16))
        equipment_label.pack(pady=10)

        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch all available equipment
        cursor.execute("SELECT * FROM Equipment WHERE equipment_status = 'available'")
        equipment_list = cursor.fetchall()
        conn.close()

        # Display equipment list and buttons for each equipment
        for equipment in equipment_list:
            equipment_id, equipment_name, equipment_status, purchase_date = equipment

            frame = tk.Frame(self.root)
            frame.pack(pady=10, fill="x")

            # Display equipment details
            equipment_label = tk.Label(frame, text=f"{equipment_name} (Status: {equipment_status}, Purchased on: {purchase_date})", font=("Arial", 12))
            equipment_label.pack(side="left", padx=10)

            # Edit Status Button
            edit_button = tk.Button(frame, text="Edit Status", command=lambda e_id=equipment_id: self.edit_equipment_status(e_id, technician_data))
            edit_button.pack(side="left", padx=10)

            # Add Maintenance Log Button
            log_button = tk.Button(frame, text="Add Maintenance Log", command=lambda e_id=equipment_id: self.add_maintenance_log(e_id, technician_data))
            log_button.pack(side="right", padx=10)

        # Technician Details Section
        details_label = tk.Label(self.root, text="Technician Details", font=("Arial", 16))
        details_label.pack(pady=10)

        details = [
            ("Full Name", technician_data[1]),  # full_name
            ("Specialty", technician_data[2]),  # specialty
            ("Phone Number", technician_data[3]),  # phone_number
            ("Email", technician_data[4])  # email
        ]

        for field_label, value in details:
            frame = tk.Frame(self.root)
            frame.pack(pady=5, fill="x")

            label = tk.Label(frame, text=f"{field_label}: {value}", font=("Arial", 12))
            label.pack(side="left", padx=10)

            # Edit button to modify technician details
            edit_button = tk.Button(frame, text="Edit", command=lambda field=field_label, value=value: self.edit_technician_info(field, value, technician_data))
            edit_button.pack(side="right", padx=10)

        # Display Technician's Maintenance Logs
        log_label = tk.Label(self.root, text="Your Maintenance Logs", font=("Arial", 16))
        log_label.pack(pady=10)

        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch all maintenance logs by the technician
        cursor.execute("SELECT * FROM Maintenance_Logs WHERE performed_by = %s", (technician_data[0],))
        maintenance_logs = cursor.fetchall()
        conn.close()

        # Display the logs
        if maintenance_logs:
            for log in maintenance_logs:
                log_id, equipment_id, maintenance_date, description, performed_by = log

                log_frame = tk.Frame(self.root)
                log_frame.pack(pady=5, fill="x")

                log_details = f"Equipment ID: {equipment_id}, Date: {maintenance_date}, Description: {description}"

                log_label = tk.Label(log_frame, text=log_details, font=("Arial", 12))
                log_label.pack(side="left", padx=10)
        else:
            messagebox.showinfo("No Logs", "You haven't logged any maintenance yet.")

        # Log Out button
        back_button = tk.Button(self.root, text="Log Out", command=self.create_welcome_page)
        back_button.pack(pady=20)

    def edit_technician_info(self, field, value, technician_data):
        """ Edit technician details """
        def save_edited_info():
            new_value = entry.get()  # Get new value from entry
            if new_value:
                conn = get_db_connection()
                cursor = conn.cursor()

                # Update the specific field in the database
                cursor.execute(f"UPDATE Technicians SET {field.lower().replace(' ', '_')} = %s WHERE technician_id = %s", (new_value, technician_data[0]))
                conn.commit()
                conn.close()

                # Refresh the page with the updated info
                messagebox.showinfo("Success", f"{field} updated successfully.")
                self.create_technician_welcome_page(technician_data)

        # Create a window to edit the specific field
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Edit {field}")

        label = tk.Label(edit_window, text=f"Edit {field}:")
        label.pack(pady=10)

        entry = tk.Entry(edit_window)
        entry.insert(0, value)  # Pre-fill the entry field with the current value
        entry.pack(pady=5)

        save_button = tk.Button(edit_window, text="Save", command=save_edited_info)
        save_button.pack(pady=10)

        cancel_button = tk.Button(edit_window, text="Cancel", command=edit_window.destroy)
        cancel_button.pack(pady=5)


    def edit_equipment_status(self, equipment_id, technician_data):
        """ Edit the status of the equipment """
        self.clear_frame()

        label = tk.Label(self.root, text="Edit Equipment Status", font=("Arial", 16))
        label.pack(pady=20)

        status_label = tk.Label(self.root, text="Enter new status (e.g., 'In Use', 'Available'):")
        status_label.pack()

        status_entry = tk.Entry(self.root)
        status_entry.pack(pady=10)

        def save_status():
            new_status = status_entry.get()

            if not new_status:
                tk.messagebox.showerror("Error", "Status cannot be empty!")
                return

            # Update the equipment status in the database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE Equipment SET equipment_status = %s WHERE equipment_id = %s", (new_status, equipment_id))
            conn.commit()
            conn.close()

            tk.messagebox.showinfo("Success", "Equipment status updated successfully!")
            self.create_technician_welcome_page(technician_data)  # Refresh the technician welcome page

        save_button = tk.Button(self.root, text="Save", command=save_status)
        save_button.pack(pady=10)

        back_button = tk.Button(self.root, text="Back", command=lambda: self.create_technician_welcome_page(technician_data))
        back_button.pack(pady=5)

    def add_maintenance_log(self, equipment_id, technician_data):
        """ Add maintenance log for the selected equipment """
        
        # Don't clear the frame immediately, it may cause the window to turn blank
        # self.clear_frame() 

        label = tk.Label(self.root, text="Add Maintenance Log", font=("Arial", 16))
        label.pack(pady=20)

        log_label = tk.Label(self.root, text="Enter maintenance details:")
        log_label.pack()

        log_entry = tk.Text(self.root, height=5, width=40)
        log_entry.pack(pady=10)

        # Fetch available equipment names from the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT equipment_name FROM Equipment WHERE equipment_status = 'available'")
        equipment_list = cursor.fetchall()
        conn.close()

        # Create a list of equipment names
        equipment_names = [equipment[0] for equipment in equipment_list]

        # Create a Combobox widget
        equipment_combobox = ttk.Combobox(self.root, values=equipment_names)
        equipment_combobox.pack(pady=10)

        def save_log():
            # Fetch selected equipment from Combobox
            selected_equipment = equipment_combobox.get()

            if not selected_equipment:
                messagebox.showerror("Error", "Please select the equipment for maintenance!")
                return

            # Fetch equipment ID based on selected equipment name
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT equipment_id FROM Equipment WHERE equipment_name = %s", (selected_equipment,))
            equipment_id = cursor.fetchone()[0]  # Fetching the equipment_id of selected equipment
            conn.close()

            log_details = log_entry.get("1.0", tk.END).strip()

            if not log_details:
                messagebox.showerror("Error", "Maintenance log cannot be empty!")
                return

            # Get the current date for the maintenance date
            maintenance_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Insert maintenance log into the database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(""" 
                INSERT INTO Maintenance_Logs (equipment_id, maintenance_date, maintenance_description, performed_by) 
                VALUES (%s, %s, %s, %s)
            """, (equipment_id, maintenance_date, log_details, technician_data[0]))  # Use technician_id instead of name for "performed_by"
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Maintenance log added successfully!")

            # After successful submission, clear frame and refresh technician welcome page
             # Clear frame to display technician's updated info
            self.create_technician_welcome_page(technician_data)  # Refresh the technician welcome page

        save_button = tk.Button(self.root, text="Save", command=save_log)
        save_button.pack(pady=10)

        back_button = tk.Button(self.root, text="Back", command=lambda: self.create_technician_welcome_page(technician_data))
        back_button.pack(pady=5)


    def create_trainer_sign_in_page(self):
        """ Creates the Trainer Sign-In page """
        self.clear_frame()

        label = tk.Label(self.root, text="Trainer Sign-In", font=("Arial", 16))
        label.pack(pady=20)

        full_name_label = tk.Label(self.root, text="Full Name")
        full_name_label.pack()
        full_name_entry = tk.Entry(self.root)
        full_name_entry.pack(pady=5)

        email_label = tk.Label(self.root, text="Email")
        email_label.pack()
        email_entry = tk.Entry(self.root)
        email_entry.pack(pady=5)

        def trainer_sign_in():
            full_name = full_name_entry.get()
            email = email_entry.get()

            # Validate trainer credentials
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Trainers WHERE full_name = %s AND email = %s", (full_name, email))
            trainer_data = cursor.fetchone()
            conn.close()

            if trainer_data:
                self.trainer_id = trainer_data[0]  # Store trainer ID
                self.create_trainer_welcome_page(trainer_data)
            else:
                messagebox.showerror("Error", "Invalid full name or email.")

        sign_in_button = tk.Button(self.root, text="Sign In", command=trainer_sign_in)
        sign_in_button.pack(pady=10)

        back_button = tk.Button(self.root, text="Back", command=self.create_welcome_page)
        back_button.pack(pady=5)

    def create_trainer_welcome_page(self, trainer_data):
        """Creates the trainer welcome page after sign-in."""
        self.clear_frame()

        # Welcome message
        label = tk.Label(self.root, text=f"Welcome {trainer_data[1]}", font=("Arial", 16))  # trainer_data[1] is full_name
        label.pack(pady=20)

        # Classes with details of who joined
        classes_label = tk.Label(self.root, text="Classes and Enrollments", font=("Arial", 16))
        classes_label.pack(pady=10)

        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch classes taught by this trainer
        cursor.execute("""
            SELECT C.class_id, C.class_name, C.class_date, C.class_time,
                (SELECT COUNT(*) FROM Class_Enrollments CE WHERE CE.class_id = C.class_id) AS enrolled_count
            FROM Classes C
            WHERE C.trainer_id = %s
        """, (self.trainer_id,))
        classes = cursor.fetchall()

        for class_id, class_name, class_date, class_time, enrolled_count in classes:
            class_details = f"{class_name} on {class_date} at {class_time} ({enrolled_count} enrolled)"
            class_frame = tk.Frame(self.root)
            class_frame.pack(pady=5, fill="x")

            class_label = tk.Label(class_frame, text=class_details, font=("Arial", 12))
            class_label.pack(side="left", padx=10)

            view_button = tk.Button(class_frame, text="View Enrollments", command=lambda c_id=class_id: self.view_enrollments(c_id))
            view_button.pack(side="right", padx=5)

            edit_button = tk.Button(class_frame, text="Edit Class", command=lambda c_id=class_id: self.edit_class(c_id))
            edit_button.pack(side="right", padx=5)

            delete_button = tk.Button(class_frame, text="Delete Class", command=lambda c_id=class_id: self.delete_class(c_id))
            delete_button.pack(side="right", padx=5)

        # Add new class button
        add_class_button = tk.Button(self.root, text="Add New Class", command=lambda: self.add_new_class(trainer_data))
        add_class_button.pack(pady=20)

        # Trainer details section
        details_label = tk.Label(self.root, text="Trainer Details", font=("Arial", 16))
        details_label.pack(pady=10)

        details = [
            ("Full Name", trainer_data[1]),  # full_name
            ("Year Started", trainer_data[2]),  # year_started
            ("Specialty", trainer_data[3]),  # specialty
            ("Phone Number", trainer_data[4]),  # phone_number
            ("Email", trainer_data[5]),  # email
        ]

        for field_label, value in details:
            frame = tk.Frame(self.root)
            frame.pack(pady=5, fill="x")

            label = tk.Label(frame, text=f"{field_label}: {value}", font=("Arial", 12))
            label.pack(side="left", padx=10)

            edit_button = tk.Button(frame, text="Edit", command=lambda field=field_label: self.edit_trainer_info(field))
            edit_button.pack(side="right", padx=10)

        # Back button
        back_button = tk.Button(self.root, text="Log Out", command=self.create_welcome_page)
        back_button.pack(pady=20)

        conn.close()

    def view_enrollments(self, class_id):
        """Displays the names of people who joined a specific class."""
        self.clear_frame()

        # Title
        label = tk.Label(self.root, text="Class Enrollments", font=("Arial", 16))
        label.pack(pady=20)

        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch the class name and list of enrolled users
        cursor.execute("SELECT class_name FROM Classes WHERE class_id = %s", (class_id,))
        class_name = cursor.fetchone()[0]

        class_label = tk.Label(self.root, text=f"Class: {class_name}", font=("Arial", 14))
        class_label.pack(pady=10)

        cursor.execute("""
            SELECT U.full_name, U.email
            FROM Class_Enrollments CE
            JOIN Users U ON CE.user_id = U.user_id
            WHERE CE.class_id = %s
        """, (class_id,))
        enrollments = cursor.fetchall()

        if enrollments:
            for full_name, email in enrollments:
                enrollment_label = tk.Label(self.root, text=f"{full_name} ({email})", font=("Arial", 12))
                enrollment_label.pack(pady=2)
        else:
            no_enrollments_label = tk.Label(self.root, text="No enrollments for this class yet.", font=("Arial", 12))
            no_enrollments_label.pack(pady=10)

        back_button = tk.Button(self.root, text="Back", command=lambda: self.create_trainer_welcome_page(self.get_trainer_data()))
        back_button.pack(pady=20)

        conn.close()


    def add_new_class(self, trainer_data):
        """ Opens a form to add a new class """
        self.clear_frame()

        label = tk.Label(self.root, text="Add New Class", font=("Arial", 16))
        label.pack(pady=20)

        class_name_label = tk.Label(self.root, text="Class Name")
        class_name_label.pack()
        class_name_entry = tk.Entry(self.root)
        class_name_entry.pack(pady=5)

        class_date_label = tk.Label(self.root, text="Class Date (YYYY-MM-DD)")
        class_date_label.pack()
        class_date_entry = tk.Entry(self.root)
        class_date_entry.pack(pady=5)

        class_time_label = tk.Label(self.root, text="Class Time (HH:MM:SS)")
        class_time_label.pack()
        class_time_entry = tk.Entry(self.root)
        class_time_entry.pack(pady=5)

        max_participants_label = tk.Label(self.root, text="Max Participants")
        max_participants_label.pack()
        max_participants_entry = tk.Entry(self.root)
        max_participants_entry.pack(pady=5)

        def save_new_class():
            class_name = class_name_entry.get()
            class_date = class_date_entry.get()
            class_time = class_time_entry.get()
            max_participants = int(max_participants_entry.get())

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Classes (trainer_id, class_name, class_date, class_time, max_participants)
                VALUES (%s, %s, %s, %s, %s)
            """, (trainer_data[0], class_name, class_date, class_time, max_participants))  # Use trainer_data[0] for trainer_id
            conn.commit()
            conn.close()

            self.create_trainer_welcome_page(trainer_data)  # Pass trainer_data back to welcome page

        save_button = tk.Button(self.root, text="Save", command=save_new_class)
        save_button.pack(pady=10)

        back_button = tk.Button(self.root, text="Back", command=lambda: self.create_trainer_welcome_page(trainer_data))
        back_button.pack(pady=5)


    def edit_class(self, class_id):
        """ Allows the trainer to edit the class details """
        self.clear_frame()

        # Fetch class details from the database
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Classes WHERE class_id = %s", (class_id,))
        class_data = cursor.fetchone()
        conn.close()

        if not class_data:
            messagebox.showerror("Error", "Class not found!")
            return

        # Unpack the class data
        class_name, class_date, class_time, max_participants, trainer_id = class_data[1], class_data[2], class_data[3], class_data[4], class_data[5]

        # Title and fields to edit
        label = tk.Label(self.root, text="Edit Class", font=("Arial", 16))
        label.pack(pady=20)

        # Class Name Field
        class_name_label = tk.Label(self.root, text="Class Name")
        class_name_label.pack()
        class_name_entry = tk.Entry(self.root)
        class_name_entry.pack(pady=5)

        # Class Date Field
        class_date_label = tk.Label(self.root, text="Class Date (YYYY-MM-DD)")
        class_date_label.pack()
        class_date_entry = tk.Entry(self.root)
        class_date_entry.pack(pady=5)

        # Class Time Field
        class_time_label = tk.Label(self.root, text="Class Time (HH:MM:SS)")
        class_time_label.pack()
        class_time_entry = tk.Entry(self.root)
        class_time_entry.pack(pady=5)

        # Max Participants Field
        max_participants_label = tk.Label(self.root, text="Max Participants")
        max_participants_label.pack()
        max_participants_entry = tk.Entry(self.root)
        max_participants_entry.pack(pady=5)

        def save_class_edit():
            """ Saves the edited class information to the database """
            new_class_name = class_name_entry.get()
            new_class_date = class_date_entry.get()
            new_class_time = class_time_entry.get()
            new_max_participants = max_participants_entry.get()

            # Check for empty fields
            if not new_class_name or not new_class_date or not new_class_time or not new_max_participants:
                messagebox.showerror("Error", "All fields must be filled!")
                return

            try:
                new_max_participants = int(new_max_participants)
            except ValueError:
                messagebox.showerror("Error", "Max Participants must be a number!")
                return

            # Update the class data in the database
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE Classes
                SET class_name = %s, class_date = %s, class_time = %s, max_participants = %s
                WHERE class_id = %s
            """, (new_class_name, new_class_date, new_class_time, new_max_participants, class_id))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Class details updated successfully!")
            self.create_trainer_welcome_page(self.get_trainer_data())  # Reload trainer's welcome page

        # Save Button
        save_button = tk.Button(self.root, text="Save", command=save_class_edit)
        save_button.pack(pady=10)

        # Back Button
        back_button = tk.Button(self.root, text="Back", command=lambda: self.create_trainer_welcome_page(self.get_trainer_data()))
        back_button.pack(pady=5)


    
    def delete_class(self, class_id):
        """Deletes a class created by the trainer after confirmation."""
        answer = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this class?")
        if answer:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM Classes WHERE class_id = %s", (class_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Class deleted successfully!")
            self.create_trainer_welcome_page(self.get_trainer_data())  # Reload trainer's welcome page


    def edit_trainer_info(self, field):
        """ Allows the trainer to edit their information """
        self.clear_frame()

        label = tk.Label(self.root, text=f"Edit {field}", font=("Arial", 16))
        label.pack(pady=20)

        entry_label = tk.Label(self.root, text=f"Enter new {field}:")
        entry_label.pack()
        entry_box = tk.Entry(self.root)
        entry_box.pack(pady=10)

        def save_update():
            new_value = entry_box.get()

            if not new_value:
                tk.messagebox.showerror("Error", f"{field} cannot be empty!")
                return

            conn = get_db_connection()
            cursor = conn.cursor()

            # Map field to database column
            db_field = {
                "Full Name": "full_name",
                "Email": "email",
                "Specialty": "specialty"
            }.get(field)

            # Update the trainer's details in the database
            cursor.execute(f"UPDATE Trainers SET {db_field} = %s WHERE trainer_id = %s", (new_value, self.trainer_id))
            conn.commit()
            conn.close()

            tk.messagebox.showinfo("Success", f"{field} updated successfully!")
            trainer_data = self.get_trainer_data()
            self.create_trainer_welcome_page(trainer_data)

        save_button = tk.Button(self.root, text="Save", command=save_update)
        save_button.pack(pady=10)

        back_button = tk.Button(self.root, text="Back", command=lambda: self.create_trainer_welcome_page(self.get_trainer_data()))
        back_button.pack(pady=5)

    def get_trainer_data(self):
        """ Fetches the trainer's data from the database """
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Trainers WHERE trainer_id = %s", (self.trainer_id,))
        trainer_data = cursor.fetchone()

        conn.close()
        return trainer_data


    def create_user_sign_in_page(self):
        """ Creates the user sign-in page """
        self.clear_frame()
        
        label = tk.Label(self.root, text="User Sign In", font=("Arial", 16))
        label.pack(pady=20)

        self.sign_in_username = self.create_form_field("Username")
        self.sign_in_password = self.create_form_field("Password")
        
        sign_in_button = tk.Button(self.root, text="Sign In", command=self.user_sign_in)
        sign_in_button.pack(pady=20)

    def user_sign_in(self):
        """ Handles user sign-in """
        username = self.sign_in_username.get()
        password = self.sign_in_password.get()

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Users WHERE username = %s AND password = %s", (username, password))
        user_data = cursor.fetchone()
        
        if user_data:
            self.username = username
            self.create_user_welcome_page()
        else:
            messagebox.showerror("Error", "Invalid credentials.")
        
        conn.close()

    def create_user_welcome_page(self):
        """ Creates the user welcome page after sign-in """
        self.clear_frame()

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch user data
        cursor.execute("SELECT * FROM Users WHERE username = %s", (self.username,))
        user_data = cursor.fetchone()

        # Welcome label
        label = tk.Label(self.root, text=f"Welcome {user_data[1]}", font=("Arial", 16))  # user_data[1] is full_name
        label.pack(pady=20)

        # Get user membership
        cursor.execute("SELECT * FROM Memberships WHERE membership_id = %s", (user_data[6],))  # user_data[6] is membership_id
        membership_data = cursor.fetchone()

        if membership_data:
            membership_name, price, max_classes_per_week = membership_data[1:4]
            membership_label = tk.Label(self.root, text=f"Your membership: {membership_name}")
        else:
            membership_name, price, max_classes_per_week = "None", 0, 0
            membership_label = tk.Label(self.root, text="You don't have a membership yet.")
        membership_label.pack(pady=5)

        show_memberships_button = tk.Button(self.root, text="Show Available Memberships", command=self.show_memberships)
        show_memberships_button.pack(pady=5)

        if membership_data:
            change_membership_button = tk.Button(self.root, text="Change Membership", command=self.change_membership)
            change_membership_button.pack(pady=5)
        else:
            buy_membership_button = tk.Button(self.root, text="Buy Membership", command=self.buy_membership)
            buy_membership_button.pack(pady=5)

        # Section: Classes Signed Up
        signed_up_label = tk.Label(self.root, text="Classes Signed Up", font=("Arial", 16))
        signed_up_label.pack(pady=10)

        cursor.execute("""
            SELECT C.class_id, C.class_name, C.class_date, C.class_time
            FROM Class_Enrollments CE
            INNER JOIN Classes C ON CE.class_id = C.class_id
            WHERE CE.user_id = (SELECT user_id FROM Users WHERE username = %s)
        """, (self.username,))
        signed_up_classes = cursor.fetchall()

        if signed_up_classes:
            for class_id, class_name, class_date, class_time in signed_up_classes:
                class_frame = tk.Frame(self.root)
                class_frame.pack(pady=5, fill="x")

                class_label = tk.Label(class_frame, text=f"{class_name} - {class_date} at {class_time}", font=("Arial", 12))
                class_label.pack(side="left", padx=10)

                drop_button = tk.Button(class_frame, text="Drop", bg="red", fg="white",
                                        command=lambda c_id=class_id: self.drop_class(c_id))
                drop_button.pack(side="right", padx=10)
        else:
            no_classes_label = tk.Label(self.root, text="You have not signed up for any classes.", font=("Arial", 12))
            no_classes_label.pack(pady=5)


        # Section: List of Classes
        classes_label = tk.Label(self.root, text="Available Classes", font=("Arial", 16))
        classes_label.pack(pady=10)

        cursor.execute("""
            SELECT class_id, class_name, class_date, class_time
            FROM Classes
            WHERE class_id NOT IN (
                SELECT class_id
                FROM Class_Enrollments
                WHERE user_id = (SELECT user_id FROM Users WHERE username = %s)
            )
        """, (self.username,))
        available_classes = cursor.fetchall()

        # Check if the user has reached the maximum number of classes
        cursor.execute("""
            SELECT COUNT(*)
            FROM Class_Enrollments
            WHERE user_id = (SELECT user_id FROM Users WHERE username = %s)
        """, (self.username,))
        signed_up_count = cursor.fetchone()[0]

        if signed_up_count < max_classes_per_week:
            if available_classes:
                for class_id, class_name, class_date, class_time in available_classes:
                    class_button = tk.Button(self.root, text=f"{class_name} - {class_date} at {class_time}",
                                            command=lambda c_id=class_id: self.sign_up_for_class(c_id))
                    class_button.pack(pady=5)
            else:
                no_classes_label = tk.Label(self.root, text="No more available classes to sign up.", font=("Arial", 12))
                no_classes_label.pack(pady=5)
        else:
            max_classes_label = tk.Label(self.root, text="You have reached the maximum number of classes for your membership.", font=("Arial", 12), fg="red")
            max_classes_label.pack(pady=5)

        # User details and delete user info
        user_details_button = tk.Button(self.root, text="User Details", command=self.edit_user_details)
        user_details_button.pack(pady=5)

        delete_user_button = tk.Button(self.root, text="Delete User Info", bg="red", fg="white", command=self.delete_user_info)
        delete_user_button.pack(pady=20)

        # Logout button
        logout_button = tk.Button(self.root, text="Log Out", command=self.create_welcome_page)
        logout_button.pack(pady=20)

        conn.close()


    def sign_up_for_class(self, class_id):
        """ Signs the user up for a class and refreshes the page """
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get user_id from the username
        cursor.execute("SELECT user_id FROM Users WHERE username = %s", (self.username,))
        user_id = cursor.fetchone()[0]

        # Insert into Class_Enrollments
        cursor.execute("INSERT INTO Class_Enrollments (class_id, user_id, enrollment_date) VALUES (%s, %s, CURDATE())", (class_id, user_id))
        conn.commit()
        conn.close()

        # Refresh the page
        self.create_user_welcome_page()
    
    def drop_class(self, class_id):
        """ Drops a class that the user has signed up for """
        conn = get_db_connection()
        cursor = conn.cursor()

        # Delete the class enrollment for the user
        cursor.execute("""
            DELETE FROM Class_Enrollments
            WHERE user_id = (SELECT user_id FROM Users WHERE username = %s) AND class_id = %s
        """, (self.username, class_id))
        conn.commit()
        conn.close()

        # Refresh the user welcome page
        self.create_user_welcome_page()

    
    def show_memberships(self):
        """ Shows available memberships from the database """
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT membership_name, price, max_classes_per_week FROM Memberships")
        memberships_data = cursor.fetchall()
        conn.close()

        membership_list = "\n".join([f"{m[0]}: ${m[1]} (Max Classes: {m[2]})" for m in memberships_data])
        messagebox.showinfo("Memberships", membership_list)

    def buy_membership(self):
        """ Allows the user to buy a membership and apply any available promotions """
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch all memberships
        cursor.execute("SELECT * FROM Memberships")
        memberships = cursor.fetchall()

        # Fetch available promotions
        cursor.execute("""
            SELECT promo_id, promo_code, discount_percentage 
            FROM Promotions 
            WHERE is_active = 1 AND CURDATE() BETWEEN start_date AND end_date
        """)
        active_promotions = cursor.fetchall()
        conn.close()

        # Display available memberships
        label = tk.Label(self.root, text="Choose a membership", font=("Arial", 16))
        label.pack(pady=20)

        # Create a button for each membership
        for membership in memberships:
            membership_name = membership[1]
            price = membership[2]
            max_classes = membership[3]

            # Create a button for each membership
            button = tk.Button(self.root, text=f"{membership_name} - ${price} | Max classes: {max_classes}", 
                            command=lambda m_id=membership[0], price=price, membership_name=membership_name: 
                            self.select_membership_with_promotion(m_id, price, membership_name, active_promotions))
            button.pack(pady=10)

        # Back to user welcome page
        back_button = tk.Button(self.root, text="Back", command=self.create_user_welcome_page)
        back_button.pack(pady=20)

    def select_membership_with_promotion(self, membership_id, price, membership_name, active_promotions):
        """ Update the user's membership and apply promotion if selected """
        promo_id = None  # Default promo_id to None
        discounted_price = price  # Default discounted_price to the original price

        # Show the user available promotions to choose from
        if active_promotions:
            promo_list = "\n".join([f"{promo[1]}: {promo[2]}% off" for promo in active_promotions])
            promotion_choice = messagebox.askquestion("Apply Promotion", f"Available promotions:\n{promo_list}\nDo you want to apply a promotion?")
            
            if promotion_choice == 'yes':
                promo_code = simpledialog.askstring("Enter Promo Code", "Enter the promo code you want to use:")
                for promo in active_promotions:
                    if promo_code and promo_code.lower() == promo[1].lower():  # Match promo code
                        promo_id = promo[0]
                        discount_percentage = promo[2]
                        discounted_price = price * (1 - discount_percentage / 100)
                        messagebox.showinfo("Promo Applied", f"Promo applied! Your new price is: ${discounted_price:.2f}")
                        break
                else:
                    messagebox.showinfo("Promo Error", "Invalid promo code. No discount applied.")
        else:
            messagebox.showinfo("No Promotions", "No active promotions are available.")

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Log the transaction with the applied promotion
            cursor.execute("""
                INSERT INTO Transactions (user_id, transaction_date, amount, transaction_type, promo_id)
                SELECT user_id, CURDATE(), %s, 'purchase', %s
                FROM Users WHERE username = %s
            """, (discounted_price, promo_id, self.username))

            # Update the user's membership
            cursor.execute("UPDATE Users SET membership_id = %s WHERE username = %s", (membership_id, self.username))
            conn.commit()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update membership: {e}")
        finally:
            conn.close()

        # Show confirmation and refresh page
        messagebox.showinfo("Success", f"Your membership has been updated to {membership_name} with a price of ${discounted_price:.2f}")
        self.create_user_welcome_page()



    def change_membership(self):
        """ Allows the user to choose a new membership and apply any available promotions """
        self.clear_frame()

        # Connect to the database to fetch all memberships and active promotions
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Memberships")  # Get all memberships
        memberships = cursor.fetchall()

        cursor.execute("""
            SELECT promo_id, promo_code, discount_percentage 
            FROM Promotions 
            WHERE is_active = 1 AND CURDATE() BETWEEN start_date AND end_date
        """)
        active_promotions = cursor.fetchall()
        conn.close()

        # Display available memberships for the user to choose
        label = tk.Label(self.root, text="Choose a new membership", font=("Arial", 16))
        label.pack(pady=20)

        # Create a button for each membership
        for membership in memberships:
            membership_name = membership[1]
            price = membership[2]
            max_classes = membership[3]

            button = tk.Button(self.root, text=f"{membership_name} - ${price} | Max classes: {max_classes}", 
                            command=lambda m_id=membership[0], price=price, membership_name=membership_name: 
                            self.select_membership_with_promotion(m_id, price, membership_name, active_promotions))
            button.pack(pady=10)

        # Back to user welcome page
        back_button = tk.Button(self.root, text="Back", command=self.create_user_welcome_page)
        back_button.pack(pady=20)


    def select_membership(self, membership_id, price, membership_name):
        """ Update the user's membership in the database and log the transaction """
        conn = get_db_connection()
        cursor = conn.cursor()

        # Log the transaction in the Transactions table (membership change)
        cursor.execute("""
            INSERT INTO Transactions (user_id, transaction_date, amount, transaction_type, promo_id)
            SELECT user_id, CURDATE(), %s, 'membership_change', NULL
            FROM Users WHERE username = %s
        """, (price, self.username))

        # Update the user's membership in the Users table
        cursor.execute("UPDATE Users SET membership_id = %s WHERE username = %s", (membership_id, self.username))
        conn.commit()
        conn.close()

        # Show a confirmation message
        messagebox.showinfo("Success", f"Your membership has been updated.")

        # Refresh the user welcome page to reflect the new membership
        self.create_user_welcome_page()


    def view_transactions(self):
        """ Show transaction history (Dummy for now) """
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Transactions WHERE user_id = (SELECT user_id FROM Users WHERE username = %s)", (self.username,))
        transactions = cursor.fetchall()
        conn.close()

        if transactions:
            transaction_history = "\n".join([f"Transaction: {t[2]} - ${t[3]}" for t in transactions])
            messagebox.showinfo("Transactions", transaction_history)
        else:
            messagebox.showinfo("Transactions", "No transactions yet.")

    def delete_user_info(self):
        """ Prompt the user to confirm deletion of their account """
        # Display a warning message
        confirmation = messagebox.askyesno("Warning", "Are you sure you want to delete your account? This action cannot be undone.")

        if confirmation:
            # Connect to the database to delete the user
            conn = get_db_connection()
            cursor = conn.cursor()

            # Delete user from Users table
            cursor.execute("DELETE FROM Users WHERE username = %s", (self.username,))
            conn.commit()
            conn.close()

            # Show a success message and logout the user
            messagebox.showinfo("Success", "Your account has been deleted successfully.")

            # Redirect to the login or welcome page
            self.create_welcome_page()  # Assuming create_welcome_page() is for the login page

    
    def edit_user_details(self):
        """ Edit user details with buttons beside each field to update information """
        self.clear_frame()

        # Connect to the database to fetch user details
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get user data from the Users table
        cursor.execute("SELECT username, password, email, full_name, phone_number FROM Users WHERE username = %s", (self.username,))
        user_data = cursor.fetchone()
        conn.close()

        # Display user details with edit buttons
        label = tk.Label(self.root, text="Edit User Details", font=("Arial", 16))
        label.pack(pady=20)

        # Display username with edit button (Username is not editable)
        username_label = tk.Label(self.root, text=f"Username: {user_data[0]}")
        username_label.pack(pady=5)

        # Display password with edit button
        password_label = tk.Label(self.root, text=f"Password: {user_data[1]}")
        password_label.pack(pady=5)
        edit_password_button = tk.Button(self.root, text="Edit", command=lambda: self.edit_field("password", password_label, user_data[1]))
        edit_password_button.pack(pady=5)

        # Display email with edit button
        email_label = tk.Label(self.root, text=f"Email: {user_data[2]}")
        email_label.pack(pady=5)
        edit_email_button = tk.Button(self.root, text="Edit", command=lambda: self.edit_field("email", email_label, user_data[2]))
        edit_email_button.pack(pady=5)

        # Display full_name with edit button
        full_name_label = tk.Label(self.root, text=f"Full Name: {user_data[3]}")
        full_name_label.pack(pady=5)
        edit_full_name_button = tk.Button(self.root, text="Edit", command=lambda: self.edit_field("full_name", full_name_label, user_data[3]))
        edit_full_name_button.pack(pady=5)

        # Display phone_number with edit button
        phone_number_label = tk.Label(self.root, text=f"Phone Number: {user_data[4]}")
        phone_number_label.pack(pady=5)
        edit_phone_button = tk.Button(self.root, text="Edit", command=lambda: self.edit_field("phone_number", phone_number_label, user_data[4]))
        edit_phone_button.pack(pady=5)

        # Back to user welcome page
        back_button = tk.Button(self.root, text="Back", command=self.create_user_welcome_page)
        back_button.pack(pady=20)

    def edit_field(self, field, label, current_value):
        """ Create input field to update the specific field and save changes """
        self.clear_frame()

        # Label to explain which field is being edited
        label = tk.Label(self.root, text=f"Edit {field.replace('_', ' ').title()}")
        label.pack(pady=20)

        # Create an entry field with current value
        entry = tk.Entry(self.root)
        entry.insert(0, current_value)
        entry.pack(pady=10)

        # Submit button to update the field
        submit_button = tk.Button(self.root, text="Submit", command=lambda: self.submit_edit(field, entry, label))
        submit_button.pack(pady=20)

        # Back button
        back_button = tk.Button(self.root, text="Back", command=self.create_user_welcome_page)
        back_button.pack(pady=5)

    def submit_edit(self, field, entry, label):
        """ Submit the changes to user details in the database """
        new_value = entry.get()

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        if field == "password":
            cursor.execute("UPDATE Users SET password = %s WHERE username = %s", (new_value, self.username))
        elif field == "email":
            cursor.execute("UPDATE Users SET email = %s WHERE username = %s", (new_value, self.username))
        elif field == "full_name":
            cursor.execute("UPDATE Users SET full_name = %s WHERE username = %s", (new_value, self.username))
        elif field == "phone_number":
            cursor.execute("UPDATE Users SET phone_number = %s WHERE username = %s", (new_value, self.username))

        conn.commit()
        conn.close()

        # Update the label with new value
        label.config(text=f"{field.replace('_', ' ').title()}: {new_value}")

        # Go back to user details page
        self.create_user_welcome_page()


    def clear_frame(self):
        """ Clears the current frame """
        for widget in self.root.winfo_children():
            widget.destroy()


# Run the application
root = tk.Tk()
app = GymManaApp(root)
root.mainloop()
