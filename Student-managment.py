student_list = []

def add_student():
    try:
        student_id = int(input("Enter student id: "))
        name = input("Enter student name: ")
        age = int(input("Enter student age: "))
        course = input("Enter student course: ")

        for student in student_list:
            if student['id'] == student_id:
                print(f"Entered student id {student_id} already exist")
                return

        new_student = {'id':student_id,'name':name,'age':age,'course':course}
        student_list.append(new_student)
        print("Student added succesfully")

    except ValueError:
        print("Invalid data for student ID and age")

    except Exception as e:
        print(f"An unexpected error occured: {e}")

def view_student():
    if not student_list:
        print("NO student data found.")
        return
    for student in student_list:
        print(f"ID: {student['id']}, 'Name':{student['name']}, 'Age':{student['age']}, 'Course':{student:['cousrse']}")
        
