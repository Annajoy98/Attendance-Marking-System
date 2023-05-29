import mysql.connector as m
import tkinter as tk
from tkinter import ttk


mydatabase = m.connect(host="localhost", user="root", password="enter mysql password", database="Attendance")
cursor = mydatabase.cursor()

# Fetches student data from the database
def fetch_student_data():
    cursor.execute("Select roll_number, name FROM students")
    return cursor.fetchall()

# Save attendance and display absentees
def save_attendance():
    absentees = []
    for student in students:
        if student[2].get() == 0:  
            absentees.append(student[1])

    
    create_absentees_table()

 
    display_absentees(absentees)

   
    save_absentees(absentees)


# Create absentees table for the specific date
def create_absentees_table():
    table_name = "abs_" + str(batch_name.get())+"_"+str(selected_date.get()).replace("-", "_")
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS `{table_name}` (
        student_RollNumber VARCHAR(50) primary key
    )
    """
    cursor.execute(create_table_query)


# Display absentees on a new page
def display_absentees(absentees):
    abs_window = tk.Toplevel(tkWindow)
    abs_window.title("Absentees")
    abs_window.geometry("300x200")

    absentees_label = tk.Label(abs_window, text="Absentees List:")
    absentees_label.grid()

    absentees_text = tk.Text(abs_window, height=10, width=30)
    absentees_text.grid()

    for student in absentees:
        absentees_text.insert(tk.END, f"{student}\n")


# Save absentees to the new table in the database for the specific date
def save_absentees(absentees):
    table_name = "abs_" + str(batch_name.get())+"_"+str(selected_date.get()).replace("-", "_")

    insert_query = f"INSERT INTO `{table_name}` (student_RollNumber) VALUES (%s)"
    for student in absentees:
        cursor.execute(insert_query, (student,))

    mydatabase.commit()

# Close the application
def close_app():
    mydatabase.close()
    tkWindow.destroy()

# Create the Tkinter GUI
tkWindow = tk.Tk()
tkWindow.title("Attendance Marking System")

# Create a date entry widget


date_label = tk.Label(tkWindow, text="Enter Date (dd-mm-yyyy):",bg="light blue")
date_label.grid(row=1, column=0, padx=10, pady=10)

selected_date = tk.StringVar()
date_entry = tk.Entry(tkWindow, textvariable=selected_date)
date_entry.grid(row=1, column=1, padx=15, pady=15)

batch_label = tk.Label(tkWindow, text="Enter course:",bg="light blue")
batch_label.grid(row=1, column=2, padx=10, pady=10)

batch_name = tk.StringVar()
batch_entry = tk.Entry(tkWindow, textvariable=batch_name)
batch_entry.grid(row=1, column=3, padx=15, pady=15)



# Fetch student data from the database
students = fetch_student_data()

# Create a label for the Listbox heading
listbox_label = tk.Label(tkWindow, text="Student List",bg="light blue")
listbox_label.grid(row=4, column=1, columnspan=2, pady=10)

student_listbox = tk.Listbox(tkWindow, selectmode=tk.MULTIPLE, height=15, fg="red", bg='white', width=60,
                             highlightthickness=0, bd=0, selectbackground='blue')
student_listbox.grid(row=5, column=1, columnspan=2, padx=10, pady=5)

# Create checkboxes
for i, student in enumerate(students):
    roll_number = student[0]
    name = student[1]
    checkbox_var = tk.IntVar()
    checkbox = tk.Checkbutton(student_listbox, text=f"{roll_number} - {name}", variable=checkbox_var)
    checkbox.grid(row=i, column=0, sticky=tk.W)
    students[i] = (student, roll_number, checkbox_var)


save_button = tk.Button(tkWindow, text="Save Attendance", command=save_attendance)
save_button.grid(row=7, column=1, columnspan=2, pady=10)


close_button = tk.Button(tkWindow, text="Close", command=close_app)
close_button.grid(row=8, column=1, columnspan=2, pady=10)

College_label = tk.Label(tkWindow, text="RV College of Arts and Science", font=("Helvetica", 18), justify="center", bg="light blue")
College_label.grid(row=0, column=1, columnspan=2, padx=10, pady=10)

tkWindow.geometry("750x600")
tkWindow.configure(bg='light blue')
tkWindow.mainloop()