import datetime
from typing import Union, List, Dict
from collections import namedtuple
from datetime import date
import os.path
import json
import csv


LAB_WORK_SESSION_KEYS = ("presence", "lab_work_n", "lab_work_mark", "date")
STUDENT_KEYS = ("unique_id", "name", "surname", "group", "subgroup", "lab_works_sessions")


class LabWorkSession(namedtuple('LabWorkSession', 'presence, lab_work_number, lab_work_mark, lab_work_date')):
    """
    Информация о лабораторном занятии, которое могло или не могло быть посещено студентом
    """
    def __new__(cls, presence: bool, lab_work_number: int, lab_work_mark: int, lab_work_date: date) -> object:
        """
            param: presence: присутствие студента на л.р.(bool)
            param: lab_work_number: номер л.р.(int)
            param: lab_work_mark: оценка за л.р.(int)
            param: lab_work_date: дата л.р.(date)
        """
        if not LabWorkSession._validate_session(presence, lab_work_number, lab_work_mark, lab_work_date):
            raise ValueError(f"LabWorkSession ::"
                             f"incorrect args :\n"
                             f"presence       : {presence},\n"
                             f"lab_work_number: {lab_work_number},\n"
                             f"lab_work_mark  : {lab_work_mark},\n"
                             f"lab_work_date  : {lab_work_date}")

        return  super(LabWorkSession, cls).__new__(cls, presence, lab_work_number, lab_work_mark, lab_work_date)

    @staticmethod
    def _validate_session(presence: bool, lab_work_number: int, lab_work_mark: int, lab_work_date: date) -> bool:
        """
            param: presence: присутствие студента на л.р.(bool)
            param: lab_work_number: номер л.р.(int)
            param: lab_work_mark: оценка за л.р.(int)
            param: lab_work_date: дата л.р.(date)
        """
        if not presence and lab_work_number >= -1:
            return False
        if not lab_work_mark != -1 and lab_work_number == 1:
            return False
        if presence and lab_work_date is None:
            return False

        return True

    def __str__(self) -> str:
        return f'{{\n' \
               f'    "presence":      {1 if self.presence else 0},\n' \
               f'    "lab_work_n":    {self.lab_work_number},\n' \
               f'    "lab_work_mark": {self.lab_work_mark},\n' \
               f'    "date":          "{self.lab_work_date.strftime("%d:%m:%y")}"\n' \
               f'}}'

    # @property
    # def presence(self) -> int:
    #     return self._presence
    #
    # @property
    # def lab_work_n(self) -> int:
    #     return self._lab_work_number
    #
    # @property
    # def lab_work_mark(self) -> int:
    #     return self._lab_work_mark
    #
    # @property
    # def lab_work_date(self) -> date:
    #     return self._lab_work_date

class Student:
    __slots__ = ('_unique_id', '_name', '_surname', '_group', '_subgroup', '_lab_work_sessions')

    def __init__(self, unique_id: int, name: str, surname: str, group: int, subgroup: int):
        """
            param: unique_id: уникальный идентификатор студента (int)
            param: name: имя студента (str)
            param: surname: фамилия студента (str)
            param: group: номер группы в которой студент обучается (int)
            param: subgroup: номер подгруппы (int)
        """
        self._unique_id = unique_id
        self._name = name
        self._surname = surname
        self._group = group
        self._subgroup = subgroup
        self._lab_work_sessions = []

        if not self._build_student(unique_id, name, surname, group, subgroup):
            raise ValueError(f"LabWorkSession ::"
                             f"incorrect args :\n"
                             f"presence       : {unique_id},\n"
                             f"lab_work_number: {name},\n"
                             f"lab_work_mark  : {surname},\n"
                             f"lab_work_date  : {group}\n"
                             f"subgroup      :  {subgroup}\n")

    def _build_student(self, unique_id: int, name: str, surname: str, group: int, subgroup: int) -> bool:
        """
            param: unique_id: уникальный идентификатор студента (int)
            param: name: имя студента (str)
            param: surname: фамилия студента (str)
            param: group: номер группы в которой студент обучается (int)
            param: subgroup: номер подгруппы (int)
        """
        if not isinstance(unique_id, int):
            return False
        if not isinstance(name, str) and not isinstance(surname, str):
            return False
        if len(name) == 0 or len(surname) == 0:
            return False
        if not isinstance(group, int):
            return False
        if not isinstance(subgroup, int):
            return False
        if subgroup <= 0 and group <= 0:
            return False
        return True

    def __str__(self) -> str:
        """
        Строковое представление Student
        Пример:
        {
                "unique_id":          26,
                "name":               "Щукарев",
                "surname":            "Даниил",
                "group":              6408,
                "subgroup":           2,
                "lab_works_sessions": [
                    {
                        "presence":      1,
                        "lab_work_n":    1,
                        "lab_work_mark": 4,
                        "date":          "15:9:23"
                    },
                    {
                        "presence":      1,
                        "lab_work_n":    2,
                        "lab_work_mark": 4,
                        "date":          "15:10:23"
                    },
                    {
                        "presence":      1,
                        "lab_work_n":    3,
                        "lab_work_mark": 4,
                        "date":          "15:11:23"
                    },
                    {
                        "presence":      1,
                        "lab_work_n":    4,
                        "lab_work_mark": 3,
                        "date":          "15:12:23"
                    }]
        }
        """

        lab_sessions_str = ',\n'.join([str(session) for session in self._lab_work_sessions])

        return f'{{\n' \
               f'    "unique_id":          {self._unique_id},\n' \
               f'    "name":               "{self._name}",\n' \
               f'    "surname":            "{self._surname}",\n' \
               f'    "group":              {self._group},\n' \
               f'    "subgroup":           {self._subgroup},\n' \
               f'    "lab_works_sessions": [\n' \
               f'{lab_sessions_str}\n' \
               f'    ]\n' \
               f'}}'

    @property
    def unique_id(self) -> int:
        """
        Метод доступа для unique_id
        """
        return self._unique_id

    @property
    def group(self) -> int:
        """
        Метод доступа для номера группы
        """
        return self._group

    @property
    def subgroup(self) -> int:
        """
        Метод доступа для номера подгруппы
        """
        return self._subgroup

    @property
    def name(self) -> str:
        """
        Метод доступа для имени студента
        """
        return self._name

    @property
    def surname(self) -> str:
        """
        Метод доступа для фамилии студента
        """
        return self._surname

    @name.setter
    def name(self, val: str) -> None:
        """
        Метод для изменения значения имени студента
        """
        if not isinstance(val, str):
            raise ValueError(f'Name setter received incorrectly variable')
        self._name = val

    @surname.setter
    def surname(self, val: str) -> None:
        """
        Метод для изменения значения фамилии студента
        """
        if not isinstance(val, str):
            raise ValueError(f'Surname setter received incorrectly variable')
        self._surname = val

    @property
    def lab_work_sessions(self):
        """
        Метод доступа для списка лабораторных работ, которые студент посетил или не посетил
        """
        for session in self._lab_work_sessions:
            yield session

    def append_lab_work_session(self, session: LabWorkSession):
        """
        Метод для регистрации нового лабораторного занятия
        """
        if not isinstance(session, LabWorkSession):
            raise TypeError('incorrect value type in appending LabWorkSession')
        self._lab_work_sessions.append(session)

    @lab_work_sessions.setter
    def lab_work_sessions(self, value):
        self._lab_work_sessions = value


def _load_lab_work_session(json_node) -> object:
    """
        Создание из под-дерева json-файла экземпляра класса LabWorkSession.
        hint: чтобы прочитать дату из формата строки, указанного в json используйте
        date(*tuple(map(int, json_node['date'].split(':'))))
    """

    for key in LAB_WORK_SESSION_KEYS:
        if key not in json_node:
            raise KeyError(f"load_lab_work_session:: key \"{key}\" not present in json_node")
    return LabWorkSession(presence=True if json_node['presence'] == 1 else False,
                          lab_work_number=int(json_node['lab_work_n']),
                          lab_work_mark=int(json_node['lab_work_mark']),
                          lab_work_date=datetime.datetime.strptime(json_node['date'], '%d:%m:%y').date())


def _load_student(json_node) -> Student:
    """
        Создание из под-дерева json-файла экземпляра класса Student.
        Если в процессе создания LabWorkSession у студента случается ошибка,
        создание самого студента ломаться не должно.
    """
    for key in STUDENT_KEYS:
        if key not in json_node:
            raise KeyError(f"_load_student:: key \"{key}\"not present in json_node")
    student = Student(json_node['unique_id'],
                      json_node['name'],
                      json_node['surname'],
                      int(json_node['group']),
                      int(json_node['subgroup']))
    for session in json_node['lab_works_sessions']:
        try:
            student.append_lab_work_session(_load_lab_work_session(session))
        except ValueError as e:
            print(e)
            continue
        except KeyError as e:
            print(e)
            continue
        except Exception as e:
            print(e)
            continue
    return student


# csv header
#     0    |   1  |   2   |   3  |    4    |  5  |    6    |        7       |       8     |
# unique_id; name; surname; group; subgroup; date; presence; lab_work_number; lab_work_mark
UNIQUE_ID = 0
STUD_NAME = 1
STUD_SURNAME = 2
STUD_GROUP = 3
STUD_SUBGROUP = 4
LAB_WORK_DATE = 5
STUD_PRESENCE = 6
LAB_WORK_NUMBER = 7
LAB_WORK_MARK = 8

def load_students_csv(file_path: str) -> Union[List[Student], None]:
    """
    Загрузка списка студентов из csv-файла.
    Ошибка создания экземпляра класса Student не должна приводить к поломке всего чтения.
    """
    assert isinstance(file_path, str)
    if not os.path.exists(file_path):
        return None

    students_raw: Dict[int, Student] = {}

    with open(file_path, 'r', encoding='utf-8') as input_file:
        csv_reader = csv.reader(input_file, delimiter=';')
        next(csv_reader)

        for line in csv_reader:
            try:
                unique_id = int(line[0])
                name = line[1]
                surname = line[2]
                group = int(line[3])
                subgroup = int(line[4])
                presence = True if int(line[6]) == 1 else False
                lab_work_number = int(line[7])
                lab_work_mark = int(line[8])
                lab_work_date = datetime.datetime.strptime(line[5].strip('"'), '%d:%m:%y').date()

                if unique_id not in students_raw:
                    students_raw[unique_id] = Student(unique_id, name, surname, group, subgroup)


                session = LabWorkSession(presence, lab_work_number, lab_work_mark, lab_work_date)
                students_raw[unique_id].append_lab_work_session(session)
            except Exception as ex:
                print(f"Ошибка при обработке строки: {ex}")
                continue
    return list(students_raw.values())


def load_students_json(file_path: str) -> Union[List[Student], None]:
    """
    Загрузка списка студентов из json-файла.
    Ошибка создания экземпляра класса Student не должна приводить к поломке всего чтения.
    """
    assert isinstance(file_path, str)
    if not os.path.exists(file_path):
        return None

    with open(file_path, "r", encoding="utf-8") as file:
        students = []
        data = json.load(file)
        for student in data['students']:
            students.append(_load_student(student))
    return students


def save_students_json(file_path: str, students: List[Student]):
    """
    Запись списка студентов в json файл
    """
    student_data = []
    for student in students:
        lab_works_sessions = []
        if student._lab_work_sessions is not None:
            for session in student._lab_work_sessions:
                session_dict = {
                    "date": session.lab_work_date.strftime("%d:%m:%y"),
                    "presence":  1 if session.presence else 0,
                    "lab_work_n": session.lab_work_number,
                    "lab_work_mark": session.lab_work_mark
                }
                lab_works_sessions.append(session_dict)

        student_dict = {
            "unique_id": student.unique_id,
            "name": student._name,
            "surname": student._surname,
            "group": student._group,
            "subgroup": student._subgroup,
            "lab_works_sessions": lab_works_sessions
        }


        student_data.append(student_dict)
    data_for_save = {
        "students": student_data
    }
    with open(file_path, 'w', encoding="utf-8") as json_file:
        json.dump(data_for_save, json_file, ensure_ascii=False, indent=4)


def save_students_csv(file_path: str, students: List[Student]):
    """
       Запись списка студентов в csv файл
       """
    ...
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:

        fieldnames = ["unique_id", "name", "surname", "group", "subgroup", "date", "presence", "lab_work_number", "lab_work_mark"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

        writer.writeheader()

        for student in students:
            if student._lab_work_sessions is not None:
                for session in student._lab_work_sessions:
                    writer.writerow({
                        "unique_id": student._unique_id,
                        "name": student._name,
                        "surname": student._surname,
                        "group": student._group,
                        "subgroup": student._subgroup,
                        "date": session.lab_work_date.strftime("%d:%m:%y"),
                        "presence": 1 if session.presence else 0,
                        "lab_work_number": session.lab_work_number,
                        "lab_work_mark": session.lab_work_mark
                    })