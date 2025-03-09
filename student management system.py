import json
import sqlite3
import pyttsx3 #pip install pyttsx3
import datetime

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def db_to_json(db_file, json_file):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        db_data = {}
        
        # Loop through each table and fetch its data
        for table_name in tables:
            table_name = table_name[0]  # Extract table name from tuple
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            # Get column names
            column_names = [description[0] for description in cursor.description]
            
            # Convert rows to a list of dictionaries
            table_data = [dict(zip(column_names, row)) for row in rows]
            
            # Add table data to the database data
            db_data[table_name] = table_data
        
        # Write the database data to a JSON file
        with open(json_file, 'w', encoding='utf-8') as json_f:
            json.dump(db_data, json_f, indent=4)
        
        print(f"Database successfully converted to {json_file}")
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the connection
        if conn:
            conn.close()

# Usage example

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
        print("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   
        print("Good Afternoon!") 

    else:
        speak("Good Evening!")  
        print("Good Evening!")

    speak("Please tell me how may I help you")  
    print("Please tell me how may I help you")     


# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('student_management.db')
cursor = conn.cursor()

# Create the student table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_no INTEGER NOT NULL UNIQUE,
    class TEXT NOT NULL
)
''')

# Function to add a student
def add_student(name, roll_no, student_class):
    try:
        cursor.execute('''
        INSERT INTO students (name, roll_no, class) 
        VALUES (?, ?, ?)
        ''', (name, roll_no, student_class))
        conn.commit()
        print("Student added successfully.")
    except sqlite3.IntegrityError:
        print("Error: Roll number already exists.")

# Function to delete a student by roll number
def delete_student(roll_no):
    cursor.execute('''
    DELETE FROM students WHERE roll_no = ?
    ''', (roll_no,))
    conn.commit()
    if cursor.rowcount > 0:
        print(f"Student with roll number {roll_no} deleted successfully.")
    else:
        print(f"No student found with roll number {roll_no}.")

# Function to update student's roll number
def update_student_roll_no(old_roll_no, new_roll_no):
    try:
        cursor.execute('''
        UPDATE students 
        SET roll_no = ? 
        WHERE roll_no = ?
        ''', (new_roll_no, old_roll_no))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Student's roll number updated from {old_roll_no} to {new_roll_no}.")
        else:
            print(f"No student found with roll number {old_roll_no}.")
    except sqlite3.IntegrityError:
        print("Error: New roll number already exists.")

# Function to view all students
def view_students():
    cursor.execute('''
    SELECT * FROM students
    ''')
    students = cursor.fetchall()
    if students:
        print("\nAll Students:")
        print("ID\tName\t\tRoll No\tClass")
        print("-"*40)
        for student in students:
            print(f"{student[0]}\t{student[1]}\t\t{student[2]}\t{student[3]}")
    else:
        print("No students found.")

# Function to view students by class
def view_students_by_class(student_class):
    cursor.execute('''
    SELECT * FROM students WHERE class = ?
    ''', (student_class,))
    students = cursor.fetchall()
    if students:
        print(f"\nStudents in class {student_class}:")
        print("ID\tName\t\tRoll No\tClass")
        print("-"*40)
        for student in students:
            print(f"{student[0]}\t{student[1]}\t\t{student[2]}\t{student[3]}")
    else:
        print(f"No students found in class {student_class}.")

# Simple user interface to interact with the system
def main():
    while True:
        print("\nPathfinder Global School")
        print("1. Add Student")
        print("2. Delete Student")
        print("3. Update Student Roll No")
        print("4. View All Students")
        print("5. View Students by Class")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter student's name: ")
            roll_no = int(input("Enter student's roll number: "))
            student_class = input("Enter student's class: ")
            add_student(name, roll_no, student_class)
        
        elif choice == '2':
            roll_no = int(input("Enter student's roll number to delete: "))
            delete_student(roll_no)
        
        elif choice == '3':
            old_roll_no = int(input("Enter student's current roll number: "))
            new_roll_no = int(input("Enter student's new roll number: "))
            update_student_roll_no(old_roll_no, new_roll_no)
        
        elif choice == '4':
            view_students()
        
        elif choice == '5':
            student_class = input("Enter the class to view students: ")
            view_students_by_class(student_class)
        
        elif choice == '6':
            print("Exiting the system.")
            break
        
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    wishMe()
    main()

db_file_path = "student_management.db"  # Path to your .db file
json_file_path = "student_management.json"  # Path for the output JSON file
db_to_json(db_file_path, json_file_path)
# Close the database connection
conn.close()
