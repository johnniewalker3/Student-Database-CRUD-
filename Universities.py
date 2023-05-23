from Members import UniversityMember, Student
from Subjects import Subject
from datetime import *
from decimal import *
from dbtools import *


# takes as argument a list and an id and return the index where is located the record with that id
def list_index(arr, id):
    pos = -1
    for i in range(len(arr)):
        if arr[i].id == id:
            pos = i
            break
    return pos


class University:
    def __init__(self):
        self.students = []
        self.subjects = []
        self.connector = open_connection()

    # view student information with a specific id
    def view_student_details(self, id):
        student_index = list_index(self.students, id)
        if student_index != -1:
            print(self.students[student_index])
        else:
            print(f"Invalid student id.")

    # view subject information with a specific id
    def view_subject_information(self, id):
        subject_index = list_index(self.subjects, id)
        if subject_index == -1:
            print("Invalid id")
            return
        print(self.subjects[subject_index])

    # view all the subjects that exist in the database of the university
    def view_available_subjects(self):
        print("=" * 30)
        for subject1 in self.subjects:
            print(subject1)

    # delete a student from the student's database
    def delete_member(self, id):
        student_index = list_index(self.students, id)
        if student_index != -1:
            query = """DELETE FROM Students 
                WHERE id = """ + str(self.students[student_index].id)
            self.students.pop(student_index)
            try:
                delete_from_table(self.connector, query)
                self.connector.commit()
                print("Student deleted")
            except MYSQL.Error as e:
                print(e)
        else:
            print(f"Invalid student id.")

    # insert a student in the student's database
    def insert_member(self, member):
        student_index = list_index(self.students, member.id)
        if student_index == -1:
            list_args = [member.birth_date, member.first_name, member.last_name, member.fathers_name,
                         member.mothers_name, member.country, member.city]
            query = "INSERT INTO Students (birth_date, first_name, last_name, fathers_name, mothers_name, country, city, "
            if member.email is not None:
                query += "email, register_date) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                list_args.append(member.email)
                list_args.append(member.register_date)
            else:
                query += "register_date) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
                list_args.append(member.register_date)
            tuple_args = tuple(list_args)
            self.students.append(member)
            try:
                id = insert_at_table(self.connector, query, tuple_args)
                print("Student inserted")
                self.connector.commit()
                return id
            except MYSQL.Error as e:
                print(e)
        else:
            print(f"The student with id {member.id} already exists.")

    # insert a subject in the subject database
    def insert_subject(self, subject):
        subject_index = list_index(self.subjects, subject.id)
        if subject_index == -1:
            query = "INSERT INTO Subjects (subject_name, professor_fullname, lesson_type) VALUES (%s, %s, %s)"
            tuple_args = (subject.subject_name, subject.professor_fullname, subject.lesson_type)
            self.subjects.append(subject)
            try:
                id = insert_at_table(self.connector, query, tuple_args)
                print("Subject inserted")
                self.connector.commit()
            except MYSQL.Error as e:
                print(e)
        else:
            print(f"The subject with id {subject.id} already exists")

    # update the information of a subject
    def update_subject(self, id, **kwargs):
        if len(kwargs) == 0:
            return
        subject_index = list_index(self.subjects, id)
        if subject_index != -1:
            if "subject_name" in kwargs.keys():
                self.subjects[subject_index].subject_name = kwargs["subject_name"]
            if "professor_fullname" in kwargs.keys():
                self.subjects[subject_index].professor_fullname = kwargs["professor_fullname"]
            if "lesson_type" in kwargs.keys():
                self.subjects[subject_index].lesson_type = kwargs["lesson_type"]
            query = """UPDATE Subjects
                    SET subject_name = '""" + self.subjects[
                subject_index].subject_name + """', professor_fullname = '""" + self.subjects[
                        subject_index].professor_fullname + """', lesson_type = """ + str(
                self.subjects[subject_index].lesson_type) \
                    + """ WHERE id = """ + str(id)
            try:
                update_table(self.connector, query)
                self.connector.commit()
                print("Subject updated")
            except MYSQL.Error as e:
                print(e)
        else:
            print(f"The subject with id {id} does not exist.")

    # cut the grade of a student in a subject he has passed
    def cut_transferable_grade(self, student_id, subject_id):
        student_index = list_index(self.students, student_id)
        if student_index == -1:
            print("Invalid student id.")
            return
        subject_index = list_index(self.subjects, subject_id)
        if subject_index == -1:
            print("Invalid subject id.")
            return
        if self.students[student_index].grades[subject_id] is not None and self.students[student_index].grades[
            subject_id] >= 5:
            self.students[student_index].grades[subject_id] = Decimal('2.0')
            query = """UPDATE grades
                    SET grade = """ + str(
                Decimal('2.0')) + """, modified_grade_date = '""" + str(
                datetime.now().date()) + """' WHERE student_id = """ + str(
                student_id) + """ AND subject_id = """ + str(subject_id)
            try:
                update_table(self.connector, query)
                print("Grade was cut")
                self.connector.commit()
            except MYSQL.Error as e:
                print(e)

    # register a new grade in a subject for a specific student
    def register_grade_on_subject(self, student_id, subject_id, grade):
        student_index = list_index(self.students, student_id)
        if student_index == -1:
            print("Invalid student id.")
            return
        subject_index = list_index(self.subjects, subject_id)
        if subject_index == -1:
            print("Invalid subject id.")
            return
        self.students[student_index].grades[subject_id] = grade
        query = """UPDATE grades
                SET grade = """ + str(grade) + """, modified_grade_date = '""" + str(
            datetime.now().date()) + """' WHERE student_id = """ + str(
            student_id) + """ AND subject_id = """ + str(subject_id)
        try:
            update_table(self.connector, query)
            print("Grade updated")
            self.connector.commit()
        except MYSQL.Error as e:
            print(e)

    # remove a subject from the subject list a specific student attends
    def remove_requested_subject(self, student_id, subject_id):
        student_index = list_index(self.students, student_id)
        if student_index == -1:
            print("Invalid student id.")
            return
        subject_index = list_index(self.subjects, subject_id)
        if subject_index == -1:
            print("Invalid subject id.")
            return
        query = """DELETE
                FROM grades
                WHERE student_id = """ + str(student_id) + """ AND subject_id = """ + str(subject_id)
        self.students[student_index].grades[subject_id] = None
        self.students[student_index].delete_subject(subject_id)

        try:
            delete_from_table(self.connector, query)
            print("Subject was deleted from student list")
            self.connector.commit()
        except MYSQL.Error as e:
            print(e)
