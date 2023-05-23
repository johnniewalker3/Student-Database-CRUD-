


class Subject:
    def __init__(self, subject_id, subject_name, professor_fullname, lesson_type):
        # id is the primary key for a subject
        self.id = subject_id
        self.subject_name = subject_name
        self.professor_fullname = professor_fullname
        # lesson can be optional or obligatory
        self.lesson_type = lesson_type

    def __str__(self):
        return f"Subject id: {self.id}\n" \
        f"Subject name: {self.subject_name}\n" \
        f"Professor fullname: {self.professor_fullname}\n" \
        f"Lesson type: {self.lesson_type}\n"



