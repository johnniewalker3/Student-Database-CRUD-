import re
from datetime import *


# validates the attributes a student has
# those attributes include his first name, last name,his father name, his mother name, his country, his city
def validate_input(choice, member_property):
    your_input = ""
    match choice:
        case 1:
            your_input = input("Read the first name of the " + member_property + ": ")
        case 2:
            your_input = input("Read the last name of the " + member_property + ": ")
        case 3:
            your_input = input("Read the fathers name of the " + member_property + ": ")
        case 4:
            your_input = input("Read the mothers name of the " + member_property + ": ")
        case 5:
            your_input = input("Read the country of the " + member_property + ": ")
        case 6:
            your_input = input("Read the city of the " + member_property + ": ")
        case default:
            print("Wrong input")
    pattern = re.compile(r"[a-zA-Z]{4,20}")
    matcher = pattern.fullmatch(your_input)
    while matcher is None:
        match choice:
            case 1:
                your_input = input("Read the first name of the " + member_property + ": ")
            case 2:
                your_input = input("Read the last name of the " + member_property + ": ")
            case 3:
                your_input = input("Read the fathers name of the " + member_property + ": ")
            case 4:
                your_input = input("Read the mothers name of the " + member_property + ": ")
            case 5:
                your_input = input("Read the country of the " + member_property + ": ")
            case 6:
                your_input = input("Read the city of the " + member_property + ": ")
            case default:
                print("Wrong input")
        matcher = pattern.fullmatch(your_input)
    return your_input


# read a valid email
def validate_email(member_property):
    pattern = re.compile(r"[a-zA-Z0-9_]{8,16}@((gmail)|(yahoo)|(hotmail))\.com")
    email = input("Read the email of the " + member_property + ": ")
    matcher = pattern.fullmatch(email)
    while matcher is None:
        email = input("Read the email of the " + member_property + ": ")
        matcher = pattern.fullmatch(email)
    return email


# reads subject name
def validate_subject_name():
    subject_name = input("Give the name of the subject: ")
    pattern = re.compile(r"[a-zA-Z]{4,30} [a-zA-Z0-9]{0,3}")
    matcher = pattern.fullmatch(subject_name)
    while matcher is None:
        subject_name = input("Give the name of the subject: ")
        matcher = pattern.fullmatch(subject_name)
    return subject_name


# read the professor name
def validate_professor_name():
    professor_fullname = input("Give the fullname of the professor: ")
    pattern = re.compile(r"[a-zA-Z]{4,15} [a-zA-Z]{4,15}")
    matcher = pattern.fullmatch(professor_fullname)
    while matcher is None:
        professor_fullname = input("Give the fullname of the professor: ")
        matcher = pattern.fullmatch(professor_fullname)
    return professor_fullname


# read the birthdate of a student
def validate_birth_date():
    pattern = re.compile(r"[1-2][1-9]{3}-[0-1][1-2]-[0-3][0-9]")
    your_input = input("Read the birth date of the student: ")
    matcher = pattern.fullmatch(your_input)
    while matcher is None and datetime.strptime('1972-01-01', '%Y-%m-%d').date() > datetime.strptime(your_input,
                                                                                                     '%Y-%m-%d').date() or datetime.strptime(
        your_input, '%Y-%m-%d').date() > datetime.strptime(
        '2005-12-31', '%Y-%m-%d').date():
        your_input = input("Read the birth date of the student: ")
        matcher = pattern.fullmatch(your_input)

    date1 = datetime.strptime(your_input, '%Y-%m-%d').date()
    return date1


# read if the lesson is optional or obligatory
def read_lesson_type():
    pattern = re.compile(r"[0-1]")
    lesson_type = input("Read the lesson type: ")
    matcher = pattern.fullmatch(lesson_type)
    while matcher is None:
        lesson_type = input("Read the lesson type: ")
        matcher = pattern.fullmatch(lesson_type)
    return int(lesson_type)


def read_choice():
    pattern = re.compile(r"[0-9][0-9]?")
    choice = input("Read a number in the range [1,19]: ")
    matcher = pattern.fullmatch(choice)
    while matcher is None:
        choice = input("Read a number in the range [1,19]: ")
        matcher = pattern.fullmatch(choice)
    return int(choice)
