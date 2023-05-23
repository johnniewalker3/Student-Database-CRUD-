from dbtools import *
from validation_data import *
from Subjects import *
from Universities import *
from Members import *


# it is used when we ask the user if he desires to enter a specific value to a field via keyboard
# if he give '1' then he can continue and can read this value for the field else if he gives '0' system continues
# ignoring the value we wanted to give to the field
def read_system_choice(message):
    choice1 = input(message)
    while choice1 not in ('0', '1'):
        choice1 = input(message)
    return choice1


# in the start we have to load all the stored students from the database together with their information
def load_all_students(connection):
    global university
    max_id = 0
    try:
        query = "SELECT * FROM Students"
        rows = query_full_results(connection, query)
        if rows is None:
            return max_id
        for row in rows:
            university.students.append(Student(**row))
            if row["id"] > max_id:
                max_id = row["id"]
    except MYSQL.Error as e:
        print(e)

    return max_id


# in the beginning we have to load all the subject that university has
def load_all_subjects(connection):
    max_id = 0
    try:
        query = "SELECT * FROM Subjects"
        rows = query_full_results(connection, query)
        if rows is None:
            print(max_id)
            return max_id
        for row in rows:
            university.subjects.append(
                Subject(row["id"], row["subject_name"], row["professor_fullname"], row["lesson_type"]))
            if row["id"] > max_id:
                max_id = row["id"]
    except MYSQL.Error as e:
        print(e)
    return max_id


# in the beginning we have to load to each student all the subjects he attends
def load_subjects_for_every_student(connection):
    try:
        for i in range(len(university.students)):
            for subject in university.subjects:
                query = "SELECT * FROM grades WHERE student_id = " + str(
                    university.students[i].id) + " AND subject_id = " + str(subject.id)
                row = query_full_results(connection, query)
                if len(row) == 0:
                    continue
                if row[0]["student_id"] is not None:
                    university.students[i].add_subject(subject)
                    if row[0]["grade"] is not None:
                        university.students[i].grades[subject.id] = row[0]["grade"]
    except MYSQL.Error as e:
        print(e)


# select one choice from the menu
def print_menu():
    print("=" * 30)
    print("1.Add a Student in students database.")
    print("2.Add a Subject in the international subject database.")
    print("3.Update student information.")
    print("4.Update subject information.")
    print("5.Delete a student.")
    print("6.Delete subject from a student.")
    print("7.Add subject to a student list.")
    print("8.View grade subject from a student.")
    print("9.View all grades from a student.")
    print("10.Delete subject from student under request.")
    print("11.View student information.")
    print("12.View subject information")
    print("13.View all the available subjects")
    print("14.View available subjects from a student.")
    print("15.Cut a transferable grade from student.")
    print("16.Register grade in a student at specific subject.")
    print("17.Save student state.")
    print("18.Calculate the average grade of a student.")
    print("19.Exit")
    print("=" * 30)


# construction of the university object
university = University()
# we establish a connection with the database
connector = open_connection()

# id that every student has will be auto increment
student_id = load_all_students(connector)

# if the student's table is empty, then autoincrement student id is set to 1
query = "ALTER TABLE Students AUTO_INCREMENT = " + str(student_id + 1)
alter_at_table(connector, query)
connector.commit()

# subject id that every subject has will be auto increment
subject_id = load_all_subjects(connector)

# if it goes false, then the loop below stops
active = True

# load to each student has subject has
load_subjects_for_every_student(connector)

print(student_id)

query = "SELECT id  FROM Students"
row = query_full_results(connector, query)
print(row)




while active:
    print_menu()
    choice = read_choice()
    match choice:
        case 1:
            # we increase automatically student id.As we said is auto increment
            # when a row is deleted, and we want to add a new record then we take the id
            # of the last record, and the next last record will have id = prev_last_row_id + 1.
            # If the table is empty, then we set auto increment = 1, and after we set student_id = 1
            query = "SELECT MAX(id) as max_id  FROM Students"
            row = query_full_results(connector, query)
            print(row)
            if len(row) > 0 and row[0]['max_id'] is not None:
                student_id = row[0]['max_id'] + 1
            else:
                query2 = "ALTER TABLE Students AUTO_INCREMENT = 1"
                alter_at_table(connector, query2)
                connector.commit()
                student_id = 1
            print(student_id)
            # read the first name of the student
            first_name = validate_input(1, 'student')
            # read the last name of the student
            last_name = validate_input(2, 'student')
            # read the father name of the student
            fathers_name = validate_input(3, 'student')
            # read the last name of the student
            mothers_name = validate_input(4, 'student')
            # read country of the student
            country = validate_input(5, 'student')
            # read city of the student
            city = validate_input(6, 'student')
            # read birthdate of the student
            birth_date = validate_birth_date()
            # read email of the student

            has_email = read_system_choice("Has the student email?(1-Yes, 0-No): ")
            if has_email == '1':
                email = validate_email('student')
            else:
                email = None
            # construct the Student with the appropriate information i gave on you
            student = Student(id=student_id, first_name=first_name, last_name=last_name, fathers_name=fathers_name,
                              mothers_name=mothers_name, country=country, city=city, birth_date=birth_date, email=email,
                              register_date=datetime.now())
            # register a student in the database
            last_row_id = university.insert_member(student)
            query = "ALTER TABLE Students AUTO_INCREMENT = " + str(last_row_id + 1)
            alter_at_table(connector, query)
            connector.commit()
        case 2:
            # we increase automatically subject id.As we said is auto increment
            subject_id += 1
            # read subject name
            subject_name = validate_subject_name()
            # read the name of the professor that teaches this subject
            professor_name = validate_professor_name()

            # 1 indicates that the lesson is obligatory - 0 indicates that the lesson is optional
            lesson_type = read_lesson_type()
            subject = Subject(subject_id, subject_name, professor_name, lesson_type)
            university.insert_subject(subject)
        case 3:
            # we check if the student exists by searching him in the university students directory and
            # if we find the student then we return its position in the student list
            # otherwise is return to us -1
            id = int(input("Give student's id: "))
            student_index = list_index(university.students, id)
            if student_index == -1:
                print("Invalid id")
                continue
            #
            dict_args = {}
            # we prompt the user if he desires to update the first name of the student
            choice_for_first_name = read_system_choice(
                "Do you want to update the first name of the student?(1-Yes, 0-No): ")
            if choice_for_first_name == '1':
                first_name = validate_input(1, 'student')
                dict_args["first_name"] = first_name

            # we prompt the user if he desires to update the last name of the student
            choice_for_last_name = read_system_choice(
                "Do you want to update the last name of the student?(1-Yes, 0-No): ")
            if choice_for_last_name == '1':
                last_name = validate_input(2, 'student')
                dict_args["last_name"] = last_name

            # we prompt the user if he desires to update the father name of the student
            choice_for_fathers_name = read_system_choice(
                "Do you want to update the father name of the student?(1-Yes, 0-No): ")
            if choice_for_fathers_name == '1':
                fathers_name = validate_input(3, 'student')
                dict_args["fathers_name"] = fathers_name

            # we prompt the user if he desires to update the mother name of the student
            choice_for_mothers_name = read_system_choice(
                "Do you want to update the mother name of the student?(1-Yes, 0-No): ")
            if choice_for_mothers_name == '1':
                mothers_name = validate_input(4, 'student')
                dict_args["mothers_name"] = mothers_name

            # we prompt the user if he desires to update the country of the student
            choice_for_country = read_system_choice(
                "Do you want to update the country where  student was born?(1-Yes, 0-No): ")
            if choice_for_country == '1':
                country = validate_input(5, 'student')
                dict_args["country"] = country

            # we prompt the user if he desires to update the city of the student
            choice_for_city = read_system_choice("Do you want to update the city that student lives?(1-Yes, 0-No): ")
            if choice_for_city == '1':
                city = validate_input(6, 'student')
                dict_args["city"] = city

            # we prompt the user if he desires to update the email of the student
            choice_for_email = read_system_choice("Do you want to update the email of the student?(1-Yes, 0-No): ")
            if choice_for_email == '1':
                email = validate_email('student')
                dict_args["email"] = email
            university.students[student_index].update_details(**dict_args)
        case 4:
            # check if the subject exist.If exist then in the subject database then we can update its
            # attributes.Otherwise, if it is not present in the subject list then we take -1 as subject
            # index

            sub_id = int(input("Read the id of the subject: "))
            subject_pos = list_index(university.subjects, sub_id)
            if subject_pos == -1:
                print("Invalid id")
                continue
            dict_args = {}
            # we prompt the user if he desires to change the name of the subject
            choice_for_subject_name = read_system_choice("Do you want to update the subject name?(1-Yes,0-No): ")
            if choice_for_subject_name == '1':
                subject_name = validate_subject_name()
                dict_args["subject_name"] = subject_name

            # we prompt the user if he desires to change the professor name of the subject
            choice_for_professor = read_system_choice("Do you want to update the professor name?(1-Yes,0-No): ")
            if choice_for_professor == '1':
                professor_fullname = validate_professor_name()
                dict_args["professor_fullname"] = professor_fullname

            # we prompt the user if he desires to change the type of the lesson
            choice_for_lesson_type = read_system_choice("Do you want to update the lesson type?(1-Yes,0-No): ")
            if choice_for_lesson_type == '1':
                lesson_type = read_lesson_type()
                dict_args["lesson_type"] = lesson_type

            university.update_subject(sub_id, **dict_args)
        case 5:
            # reads a student id, and if he exists in the student's table, his record is deleted
            stud_id = int(input("Read student id: "))
            university.delete_member(stud_id)
            max_id = 0
            for i in range(len(university.students)):
                max_id = max(max_id, university.students[i].id)
            print(f"max_id = {max_id}")
            query = "ALTER TABLE Students AUTO_INCREMENT = " + str(max_id + 1)
            alter_at_table(connector, query)
            connector.commit()
        case 6:
            # delete a record that includes a subject a specific student attends
            stud_id = int(input("Read student id: "))
            sub_id = int(input("Read subject_id: "))
            student_index = list_index(university.students, stud_id)
            university.students[student_index].delete_subject(sub_id)
        case 7:
            # add a subject in the subject list of a specific student
            stud_id = int(input("Read student_id: "))
            sub_id = int(input("Read subject_id: "))
            subject_index = list_index(university.subjects, sub_id)
            if subject_index == -1:
                print("Invalid subject id")
                continue
            student_index = list_index(university.students, stud_id)
            if student_index == -1:
                print("Invalid student id")
                continue
            university.students[student_index].add_subject(university.subjects[subject_index])
        case 8:
            # view grade of a specific subject from a specific student
            stud_id = int(input("Read a student id: "))
            sub_id = int(input("Read a subject id: "))
            student_index = list_index(university.students, stud_id)
            if student_index == -1:
                print("Invalid student id")
                continue
            university.students[student_index].view_subject_grade(sub_id)
        case 9:
            # view grades from all subjects a specific student attends
            stud_id = int(input("Read a student id: "))
            student_index = list_index(university.students, stud_id)
            if student_index == -1:
                print("Invalid student id")
                continue
            university.students[student_index].view_all_grades()
        case 10:
            # delete a subject from a student under request
            stud_id = int(input("Read a student id: "))
            sub_id = int(input("Read a subject id: "))
            university.remove_requested_subject(stud_id, sub_id)
        case 11:
            # reads information of a specific student
            stud_id = int(input("Read a student id: "))
            university.view_student_details(stud_id)
        case 12:
            # reads information of a specific subject
            sub_id = int(input("Read a subject_id: "))
            university.view_subject_information(sub_id)
        case 13:
            university.view_available_subjects()
        case 14:
            # view all subjects a specific student attends
            stud_id = int(input("Read a student id: "))
            student_index = list_index(university.students, stud_id)
            if student_index == -1:
                print("Invalid student id")
                continue
            university.students[student_index].view_all_subjects()
        case 15:
            # cut the grade of a subject that a specific student has passed
            stud_id = int(input("Read a student id: "))
            sub_id = int(input("Read a subject id: "))
            university.cut_transferable_grade(stud_id, sub_id)
        case 16:
            # register a grade in a subject that a specific student attends
            stud_id = int(input("Read a student id: "))
            sub_id = int(input("Read a subject id: "))
            grade = Decimal(input('Read student\'s grade: '))
            university.register_grade_on_subject(stud_id, sub_id, grade)
        case 17:
            # save information of a student
            stud_id = int(input("Read a student id: "))
            student_index = list_index(university.students, stud_id)
            if student_index == -1:
                print("Invalid student id.")
                continue
            university.students[student_index].save_details()
        case 18:
            # calculate and print the average grade of a student in the subjects he has passed
            stud_id = int(input("Read a student id: "))
            student_index = list_index(university.students, stud_id)
            if student_index == -1:
                print("Invalid student id.")
                continue
            print(
                f"The average grade of the student with id {stud_id} is: {university.students[student_index].grades_avg()}")
        case 19:
            # exit the program
            active = False

university.connector.close()
connector.close()
for i in range(len(university.students)):
    university.students[i].connector.close()