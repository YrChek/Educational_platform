class Student:
    list_grades = {}
    average_grade = {}

    def __init__(self, surname, name, patronymic=None):
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self.finished_courses = []
        self.courses_in_progress = []
        self.full_name = f'{surname} {name} {patronymic}'
        self.list_grades[self.full_name] = {}
        self.average_grade[self.full_name] = []

    def add_courses(self, course_name):
        """Добавление законченного курса"""
        self.finished_courses.append(course_name)

    def add_grades(self, lecturer, course, grade):
        """Выставление оценок лекторам"""
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached \
                and course in self.courses_in_progress:
            if course not in lecturer.list_grades[lecturer.full_name]:
                lecturer.list_grades[lecturer.full_name][course] = []
                lecturer.list_grades[lecturer.full_name][course] += [grade]
                print(f'Лектору {lecturer.name} {lecturer.surname} за лекцию на курсе {course}'
                      f' поставлена оценка {grade}')
            else:
                lecturer.list_grades[lecturer.full_name][course] += [grade]
                print(f'Лектору {lecturer.name} {lecturer.surname} за лекцию на курсе {course}'
                      f' поставлена оценка {grade}')
        else:
            print('Ошибка при оценке лектора')

    def averaging(self):
        """расчет среднего балла у студента"""
        summa = 0
        length = 0
        if len(self.list_grades[self.full_name]) > 0:
            for k, v in self.list_grades[self.full_name].items():
                summa += sum(v)
                length += len(v)
            if length == 0:
                res = 0
            else:
                res = round(summa / length, 1)
        else:
            res = 0
        self.average_grade[self.full_name] = [res]
        return res

    def __str__(self):
        """Перегрузка метода __str__"""
        average = self.averaging()
        my_list = ', '.join(self.courses_in_progress)
        my_list_2 = ', '.join(self.finished_courses)
        res = f"\nИмя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за домашние задания: {average}\n" \
              f"Курсы в процессе изучения: {my_list}\nЗавершенные курсы: {my_list_2}\n"
        return res

    def comparison(self, student):
        """Сравнение студентов по средней оценке"""
        self.averaging()
        student.averaging()
        if self.averaging() > student.averaging():
            print(f'Средний балл за домашние работы у студента {self.full_name} выше, чем у студента '
                  f'{student.full_name}')
        elif self.averaging() < student.averaging():
            print(f'Средний балл за домашние работы у студента {student.full_name} выше, чем у {self.full_name}')
        else:
            print(f'У студента {self.full_name} и студента {student.full_name} одинаковый средний балл за домашние'
                  f' работы')


class Mentor:
    list_grades = {}
    average_grade = {}

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def add_grades(self, student, course, grade):
        """Выставление оценок студентам"""
        if isinstance(student, Student) and course in student.courses_in_progress \
                and course in self.courses_attached:
            if course not in student.list_grades[student.full_name]:
                student.list_grades[student.full_name][course] = []
                student.list_grades[student.full_name][course] += [grade]
                print(f'Судент {student.full_name}, за домашние задание по курсу {course},'
                      f' получил оценку {grade}')
            else:
                student.list_grades[student.full_name][course] += [grade]
                print(f'Судент {student.full_name}, за домашние задание по курсу {course},'
                      f' получил оценку {grade}')
        else:
            print('Ошибка при оценке студента')


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.full_name = f'{name} {surname}'
        self.list_grades[self.full_name] = {}
        self.average_grade[self.full_name] = {}

    def averaging(self):
        """расчет среднего балла у лектора"""
        summa = 0
        length = 0
        if len(self.list_grades[self.full_name]) > 0:
            for k, v in self.list_grades[self.full_name].items():
                summa += sum(v)
                length += len(v)
            if length == 0:
                res = 0
            else:
                res = round(summa / length, 1)
        else:
            res = 0
        self.average_grade[self.full_name] = [res]
        return res

    def __str__(self):
        """Перегрузка метода __str__"""
        average = self.averaging()
        res = f"\nИмя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {average}\n"
        return res

    def comparison(self, lecturer):
        """Сравнение лекторов по средней оценке"""
        self.averaging()
        lecturer.averaging()
        if self.averaging() > lecturer.averaging():
            print(f'Средний балл за лекции у лектора {self.full_name} выше, чем у лектора {lecturer.full_name}')
        elif self.averaging() < lecturer.averaging():
            print(f'Средний балл за лекции у лектора {lecturer.full_name} выше, чем у лектора {self.full_name}')
        else:
            print(f'Средний балл за лекции у лектора {lecturer.full_name} равен среднему баллу лектора'
                  f' {self.full_name}')


class Reviewer(Mentor):
    def add_grades(self, student, course, grade):
        """Выставление экспертом оценки студенту"""
        if course in student.courses_in_progress:
            self.courses_attached = [course]
            super().add_grades(student, course, grade)
        else:
            print('Ошибка при оценке студента')

    def __str__(self):
        """Перегрузка метода __str__"""
        res = f"\nИмя: {self.name}\nФамилия: {self.surname}"
        return res


def grade_in_course(*my_list):
    """Функция подсчета средней оценки за домашние работы"""
    summa = 0
    length = 0
    for i in my_list:
        if i in Student.list_grades:
            if my_list[-1] in Student.list_grades[i]:
                summa += sum(Student.list_grades[i][my_list[-1]])/len(Student.list_grades[i][my_list[-1]])
                length += 1
    if length != 0:
        res = round(summa/length, 1)
    else:
        res = 0
    print(f'Средний балл всех студентов за домашние задания по курсу {my_list[-1]} равен {res}')


def grade_in_lecture(*my_list):
    """Функция подсчета средней оценки за лекции"""
    summa = 0
    length = 0
    for i in my_list:
        if i in Mentor.list_grades:
            if my_list[-1] in Mentor.list_grades[i]:
                summa += sum(Mentor.list_grades[i][my_list[-1]])/len(Mentor.list_grades[i][my_list[-1]])
                length += 1
    if length != 0:
        res = round(summa/length, 1)
    else:
        res = 0
    print(f'Средний балл всех лекторов за лекции по курсу {my_list[-1]} равен {res}')


student_1 = Student('Пупкин', 'Василий', 'Алибабаевич')
student_1.courses_in_progress += ['Git', 'Python']
student_1.finished_courses += ['Введение в програмирование']
student_2 = Student('Климова', 'Маруся', 'Прокофьевна')
student_2.courses_in_progress += ['Git', 'Python']
student_2.finished_courses += ['Введение в програмирование']

lecturer_1 = Lecturer('Козьма', 'Прутков')
lecturer_1.courses_attached += ['Git', 'Python']
lecturer_2 = Lecturer('Васса', 'Железнова')
lecturer_2.courses_attached += ['Python', 'Git']

reviewer_1 = Reviewer('Иван', 'Грозный')
reviewer_2 = Reviewer('Илья', 'Обломов')

reviewer_1.add_grades(student_1, 'Git', 9)
reviewer_1.add_grades(student_1, 'Python', 7)
reviewer_2.add_grades(student_2, 'Git', 10)
reviewer_2.add_grades(student_2, 'Python', 9)

student_1.add_grades(lecturer_1, 'Git', 9)
student_1.add_grades(lecturer_1, 'Python', 10)
student_2.add_grades(lecturer_2, 'Git', 10)
student_2.add_grades(lecturer_2, 'Python', 9)

student_1.comparison(student_2)
lecturer_1.comparison(lecturer_2)

grade_in_course('Пупкин Василий Алибабаевич', 'Климова Маруся Прокофьевна', 'Git')
grade_in_lecture('Козьма Прутков', 'Васса Железнова', 'Git')

print(student_1)
print(student_2)

print(lecturer_1)
print(lecturer_2)

print(reviewer_1)
print(reviewer_2)
