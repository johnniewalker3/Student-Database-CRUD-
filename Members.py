from datetime import datetime
from typing import Dict, Any

from Subjects import Subject
from dbtools import *
from decimal import Decimal


def subject_indexes(subjects, id):
    pos = -1
    for i in range(len(subjects)):
        if subjects[i].id == id:
            pos = i
    return pos


class UniversityMember:
    def __init__(self, **kwargs):
        # kwargs includes id, first_name, last_name, fathers_name, mothers_name, country, city, email,
        # register_date, history operations, connector, member_state(Student or Professor)
        self.member_property = 'Student'
        # id is the primary key each student
        self.id = kwargs["id"]
        self.birth_date = kwargs["birth_date"]
        self.first_name = kwargs["first_name"]
        self.last_name = kwargs["last_name"]
        self.fathers_name = kwargs["fathers_name"]
        self.mothers_name = kwargs["mothers_name"]
        self.country = kwargs["country"]
        self.city = kwargs["city"]
        self.email = kwargs["email"]
        self.register_date = datetime.now()
        # operation history
        # last time acting one of those operations
        self.history = {"update_state_date": datetime.now(), "save_state_date": datetime.now()}
        # Connector in order to execute queries
        self.connector = open_connection()

    # update student information
    def update_details(self, **kwargs):
        if len(kwargs) == 0:
            return
        # if birthdate is included in the fields we want to update, then update it
        if "birth_date" in kwargs.keys():
            self.birth_date = kwargs["birth_date"]

        # if first_name is included in the fields we want to update, then update it
        if "first_name" in kwargs.keys():
            self.first_name = kwargs["first_name"]

        # if last_name is included in the fields we want to update, then update it
        if "last_name" in kwargs.keys():
            self.last_name = kwargs["last_name"]

        # if fathers_name is included in the fields we want to update, then update it
        if "fathers_name" in kwargs.keys():
            self.fathers_name = kwargs["fathers_name"]

        # if mothers_name is included in the fields we want to update, then update it
        if "mothers_name" in kwargs.keys():
            self.mothers_name = kwargs["mothers_name"]

        # if a country is included in the fields we want to update, then update it
        if "country" in kwargs.keys():
            self.country = kwargs["country"]

        # if city is included in the fields we want to update, then update it
        if "city" in kwargs.keys():
            self.city = kwargs["city"]

        # if email is included in the fields we want to update, then update it
        if "email" in kwargs.keys():
            self.email = kwargs["email"]

        kwargs["update_state_date"] = datetime.now()
        self.history["update_state_date"] = kwargs["update_state_date"]

        # create the query
        query = """UPDATE Students 
                SET """ + ",".join(
            key + " = '" + str(val) + "'" for key, val in kwargs.items()) \
                + """ WHERE id = """ + str(self.id)

        # execute the insert query
        try:
            update_table(self.connector, query)
            print("Row inserted")
            self.connector.commit()
        except MYSQL.Error as e:
            print(e)

    # save student information
    def save_details(self):
        # store all the attributes of a student inside a dictionary
        member_informations = {}
        member_informations["first_name"] = self.first_name
        member_informations["last_name"] = self.last_name
        member_informations["fathers_name"] = self.fathers_name
        member_informations["mothers_name"] = self.mothers_name
        member_informations["country"] = self.country
        member_informations["city"] = self.city
        member_informations["email"] = self.email
        member_informations["register_date"] = self.register_date
        member_informations['birth_date'] = self.birth_date
        self.history["save_state_date"] = datetime.now()
        member_informations["save_state_date"] = str(datetime.now())

        # create the query
        query = """UPDATE Students
                SET """ + ",".join(
            key + " = '" + str(val) + "'" for key, val in member_informations.items()) \
                + """ WHERE id = """ + str(self.id)

        # execute the insert query
        try:
            update_table(self.connector, query)
            print("Student information were saved!")
            self.connector.commit()
        except MYSQL.Error as e:
            print(e)


class Student(UniversityMember):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # all the subjects that student attends
        self.subjects = []
        # the grades of the student in the courses he attends
        self.grades = {}

        # map with the id of the subject and the name of the subject
        self.subject_id_name = {}
        # map with the name of the subject and the id of the subject
        self.subject_name_id = {}

    def __str__(self):
        print("=" * 30)
        return f"Student's id: {self.id}\n" \
        f"Student's First Name: {self.first_name}\n" \
        f"Student's Last Name: {self.last_name}\n" \
        f"Student's Birth Date: {self.birth_date}\n" \
        f"Student's Fathers Name: {self.fathers_name}\n" \
        f"Student's Mothers Name: {self.mothers_name}\n" \
        f"Student's Country: {self.country}\n" \
        f"Student's City: {self.city}\n" \
        f"Student's email: {self.email}\n" \
        f"Student's Register Date: {self.register_date}\n" \

    def add_subject(self, subject):
        # add a subject to the subject list that the specific student attends
        subject_pos = subject_indexes(self.subjects, subject.id)
        # if it is not in the subject table, add it
        if subject_pos == -1:
            self.subjects.append(subject)
            self.grades[subject.id] = None
            self.subject_id_name[subject.id] = subject.subject_name
            self.subject_name_id[subject.subject_name] = subject.id

            # in the beginning, when we load for each student the subjects he attends,
            # we don't want to add those subjects again in the database
            try:
                query2 = "SELECT * FROM grades WHERE student_id = " + str(self.id) + " AND subject_id = " + str(subject.id)
                rows = query_full_results(self.connector, query2)
                if len(rows) > 0:
                    return
                query = """INSERT INTO grades (student_id, subject_id) VALUES(""" + str(self.id) + """, """ + str(subject.id) + """)"""
                last_row_id = insert_at_table(self.connector, query, None)
                self.connector.commit()
                if last_row_id is not None:
                    print("Added successfully")
            except MYSQL.Error as e:
                print(e)
        else:
            print(f"The subject {subject.subject_name} is already in the subject list.")

    def delete_subject(self, id):
        # search for a subject with a specific id.
        # if exists then check if the grade in this subject is None
        # if it is None then delete the record of this subject from the subjects a student attends
        subject_pos = subject_indexes(self.subjects, id)
        if subject_pos != -1 and self.grades[id] is None:
            subject_name = self.subject_id_name[id]
            self.subjects.pop(subject_pos)
            self.subject_name_id.pop(self.subject_id_name[id])
            self.subject_id_name.pop(id)
            self.grades.pop(id)
            try:
                query = """DELETE
                        FROM grades
                        WHERE student_id = """ + str(self.id) + """ AND subject_id = """ + str(id)

                delete_from_table(self.connector, query)
                self.connector.commit()
                print("Removed successfully!")
            except MYSQL.Error as e:
                print(e)
            return 1
        else:
            if subject_pos == -1:
                print(f"The subject with id {id} does not belong in the subject list")
            else:
                print(f"The subject with name {self.subject_id_name[id]} has a grade in its field and can not be deleted. ")
        return 0

    def view_subject_grade(self, id):
        # searches for a subject with a specific id and if exists then it prints its grade
        subject_pos = subject_indexes(self.subjects, id)
        if subject_pos != -1:
            print(f"The grade in subject {self.subject_id_name[id]} is {self.grades[id]}")
        else:
            print(f"The subject with id {id} does not belong in the subject list.")

    def grades_avg(self):
        # calculate the average grade of a student in all subjects and return it
        sum = 0
        count_subjects = 0
        for grade in self.grades.values():
            if grade is not None and grade >= 5:
                sum += grade
                count_subjects += 1
        if count_subjects > 0:
            return round(sum / count_subjects, 2)
        return None

    def view_all_subjects(self):
        # view all the subjects a student attends
        for subject in self.subjects:
            print(subject)

    def view_all_grades(self):
        print("=" * 30)
        for sub_id, grade in self.grades.items():
            query = "SELECT modified_grade_date FROM grades WHERE student_id = " + str(self.id) + " AND subject_id = " + str(sub_id)
            subject_pos = subject_indexes(self.subjects, sub_id)
            row = query_full_results(self.connector, query)
            # create a query that takes the modified date student passed the lesson
            print(f"{self.subject_id_name[sub_id]} : {self.grades[sub_id]}-{row[0]['modified_grade_date']}")


